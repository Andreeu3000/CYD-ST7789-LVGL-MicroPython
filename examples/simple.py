import lvgl as lv
import lcd_bus
import machine
import st7789
import task_handler
import xpt2046
import time
import gc



# =========================================================
# RGB
# =========================================================

def rgb_hex(r, g, b):
    return (r << 16) | (g << 8) | b

# =========================================================
# BACKLIGHT
# =========================================================

backlight = machine.PWM(machine.Pin(21), freq=5000, duty_u16=65535)
def set_brightness(value):
    value = max(0, min(100, value))
    backlight.duty_u16(value * 65535 // 100)

set_brightness(0)

# =========================================================
# CONFIGURACION
# =========================================================

WIDTH = 240
HEIGHT = 320


# =========================================================
# LCD
# =========================================================

print("1. LCD SPI")

lcd_spi = machine.SPI.Bus(
    host=2,
    mosi=13,
    miso=12,
    sck=14
)


print("2. LCD BUS")

display_bus = lcd_bus.SPIBus(
    spi_bus=lcd_spi,
    freq=40000000,
    dc=2,
    cs=15
)


# =========================================================
# FRAMEBUFFER PARCIAL
# =========================================================

_BUFFER_SIZE = WIDTH * HEIGHT * 2 // 10

#print("Framebuffer parcial:")
#print("Bytes:", _BUFFER_SIZE)

fb1 = display_bus.allocate_framebuffer(
    _BUFFER_SIZE,
    lcd_bus.MEMORY_INTERNAL | lcd_bus.MEMORY_DMA
)

fb2 = None


print("3. DISPLAY")

display = st7789.ST7789(
    data_bus=display_bus,

    display_width=WIDTH,
    display_height=HEIGHT,

    frame_buffer1=fb1,
    frame_buffer2=fb2,

    color_space=lv.COLOR_FORMAT.RGB565,

    color_byte_order=st7789.BYTE_ORDER_BGR,

    rgb565_byte_swap=True
)


print("4. DISPLAY INIT")

display.init()

display.set_color_inversion(False)

set_brightness(100)


# =========================================================
# LVGL
# =========================================================

print("5. LVGL INIT")

lv.init()


# =========================================================
# TOUCH
# =========================================================

print("6. TOUCH SPI")

touch_spi = machine.SPI.Bus(
    host=1,
    mosi=32,
    miso=39,
    sck=25
)


print("7. TOUCH DEVICE")

touch_dev = machine.SPI.Device(
    spi_bus=touch_spi,
    freq=2500000,
    cs=33
)


print("8. XPT2046")

indev = xpt2046.XPT2046(
    touch_dev,
    #startup_rotation=lv.DISPLAY_ROTATION._90,
    debug=False
)


#indev._cal.mirrorX = True
#indev._cal.mirrorY = True


# =========================================================
# ROTACION
# =========================================================

#display.set_rotation(lv.DISPLAY_ROTATION._90)


print("TOUCH CALIBRATED:", indev.is_calibrated)


# =========================================================
# TASK HANDLER
# =========================================================

print("9. TASK HANDLER")

th = task_handler.TaskHandler()


# =========================================================
# PANTALLAS
# =========================================================

print("10. CREANDO VENTANAS")


# =========================================================
# BUFFERS DE IMAGEN
# =========================================================

image_buffers = []
image_descriptors = []


def load_bin_image(filepath, width, height): #Cargar imágenes .bin CF_TRUE_COLOR

    pixels = width * height
    expected = pixels * 2

    with open(filepath, "rb") as f:

        header = f.read(4)

        if len(header) != 4:
            raise ValueError("Header corrupto")

        h = (
            header[0]
            | (header[1] << 8)
            | (header[2] << 16)
            | (header[3] << 24)
        )

        hw = (h >> 10) & 0x7FF
        hh = (h >> 21) & 0x7FF

        if hw != width or hh != height:
            raise ValueError(
                "Dimensiones incorrectas"
            )

        data = bytearray(expected)

        CHUNK = 256
        temp = bytearray(CHUNK)

        pos = 0

        while pos < expected:

            size = min(
                CHUNK,
                expected - pos
            )

            n = f.readinto(temp, size)

            if n != size:
                raise ValueError(
                    "RGB565 incompleto"
                )

            data[pos:pos + n] = temp[:n]

            pos += n

    temp = None

    dsc = lv.image_dsc_t()

    dsc.header.magic = lv.IMAGE_HEADER_MAGIC
    dsc.header.cf = lv.COLOR_FORMAT.RGB565
    dsc.header.w = width
    dsc.header.h = height
    dsc.header.stride = width * 2

    dsc.data_size = len(data)
    dsc.data = data

    image_buffers.append(data)
    image_descriptors.append(dsc)

    return dsc


def load_bin_image_alpha(filepath, width, height): #Cargar imágenes CF_TRUE_COLOR_ALPHA

    pixels = width * height
    expected = pixels * 3

    # ---------------------------------------------
    # Buffer FINAL
    # RGB565 + A8
    # ---------------------------------------------

    out = bytearray(expected)

    # ---------------------------------------------
    # Leer header directamente desde Flash
    # ---------------------------------------------

    with open(filepath, "rb") as f:

        header = f.read(4)

        if len(header) != 4:
            raise ValueError(
                "Archivo pequeño: " + filepath
            )

        h = (
            header[0]
            | (header[1] << 8)
            | (header[2] << 16)
            | (header[3] << 24)
        )

        cf = h & 0x3FF
        hw = (h >> 10) & 0x7FF
        hh = (h >> 21) & 0x7FF

        if cf != 5:
            raise ValueError(
                "No es TRUE_COLOR_ALPHA: "
                + filepath
            )

        if hw != width or hh != height:
            raise ValueError(
                "Dimensiones: "
                + str(hw) + "x" + str(hh)
            )

        # -----------------------------------------
        # Buffer pequeño de lectura
        # -----------------------------------------

        CHUNK_PIXELS = 64
        CHUNK_BYTES = CHUNK_PIXELS * 3

        chunk = bytearray(CHUNK_BYTES)

        alpha_offset = pixels * 2

        processed = 0

        # -----------------------------------------
        # Conversión streaming
        # -----------------------------------------

        while processed < pixels:

            count = min(
                CHUNK_PIXELS,
                pixels - processed
            )

            size = count * 3

            n = f.readinto(
                chunk,
                size
            )

            if n != size:
                raise ValueError(
                    "Archivo incompleto: "
                    + filepath
                )

            for p in range(count):

                src = p * 3
                dst = processed + p

                # RGB565
                out[dst * 2] = chunk[src]
                out[dst * 2 + 1] = chunk[src + 1]

                # Alpha
                out[alpha_offset + dst] = chunk[src + 2]

            processed += count

    # ---------------------------------------------
    # Liberar buffer temporal
    # ---------------------------------------------

    chunk = None

    # ---------------------------------------------
    # Descriptor LVGL
    # ---------------------------------------------

    dsc = lv.image_dsc_t()

    dsc.header.magic = lv.IMAGE_HEADER_MAGIC
    dsc.header.cf = lv.COLOR_FORMAT.RGB565A8
    dsc.header.w = width
    dsc.header.h = height
    dsc.header.stride = width * 2

    dsc.data_size = len(out)
    dsc.data = out

    # Mantener referencias vivas
    image_buffers.append(out)
    image_descriptors.append(dsc)

    return dsc





def clear_image(img, dsc):
    img.set_src(None)

    try:
        image_buffers.remove(dsc.data)
    except ValueError:
        pass

    try:
        image_descriptors.remove(dsc)
    except ValueError:
        pass

    del dsc

    gc.collect()



# ======== LVGL LOGICA ========

screen1 = lv.obj()
screen1.set_style_bg_color(lv.color_hex(0x101820), 0)
screen1.set_style_bg_opa(lv.OPA.COVER, 0)




title1 = lv.label(screen1)
title1.set_text("Hola mundo")
title1.center()
title1.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

# Ejemplo de carga de imagen 
# Se recomienda esta pagina para la conversión de imagen: https://lvgl.io/tools/imageconverter?hl=es-US
#dsc = load_bin_image_alpha("test.bin", 60, 60) # Nombre de la imagen previamente convertida y subida a la placa junto a las dimensiones correspondientes de la imagen 
#img = lv.image(screen1)
#img.set_src(dsc)
#img.align(lv.ALIGN.CENTER, 0, 60)





lv.screen_load(screen1)


print("")
print("==============================")
print("LVGL SCREEN LISTO")
print("==============================")
print("")




while True:

    time.sleep_ms(50)
