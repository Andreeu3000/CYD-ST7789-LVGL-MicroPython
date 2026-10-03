CYD ST7789 MicroPython + LVGL

Firmware personalizado de MicroPython con LVGL para la placa ESP32-2432S028 con pantalla ST7789 de 2.8" y resolución 240×320.

El objetivo de este proyecto es proporcionar un firmware precompilado y configurado específicamente para esta variante de la Cheap Yellow Display (CYD), facilitando su uso con MicroPython y LVGL sin tener que compilar el firmware desde cero.

«⚠️ IMPORTANTE: Este firmware está diseñado para la variante con pantalla ST7789. No debe instalarse en una CYD con otro controlador de pantalla sin comprobar primero la compatibilidad.»

Hardware compatible

ESP32-2432S028

- MCU: ESP32
- Pantalla: ST7789
- Resolución: 240×320
- Touch: XPT2046
- Interfaz de pantalla: SPI
- MicroPython + LVGL

Pines utilizados

Pantalla

Función| GPIO
MOSI| 13
MISO| 12
SCK| 14
CS| 15
DC| 2
Backlight| 21

Touch

Función| GPIO
MOSI| 32
MISO| 39
SCK| 25
CS| 33

¿Por qué existe este firmware?

Existen diferentes variantes de la Cheap Yellow Display y no todas utilizan el mismo controlador de pantalla.

Este proyecto está orientado específicamente a una variante ST7789, proporcionando una configuración preparada para utilizar:

- MicroPython
- LVGL
- Pantalla ST7789
- Touch XPT2046
- Wi-Fi
- Aplicaciones gráficas para ESP32

La intención es evitar que el usuario tenga que configurar manualmente todos los controladores y parámetros necesarios para utilizar LVGL en esta variante de la CYD.

Instalación

1. Descargar el firmware

Los archivos ".bin" precompilados se encuentran en la sección Releases de este repositorio.

2. Flashear el ESP32

Utiliza una herramienta compatible con ESP32, como "esptool".

Ejemplo:

esptool.py --port PUERTO write_flash 0x0 firmware.bin

«La dirección de flasheo puede variar dependiendo de cómo se haya generado el firmware. Consulta las instrucciones de la versión correspondiente antes de instalarlo.»

3. Iniciar MicroPython

Después de instalar el firmware, conecta la CYD mediante USB y accede a la consola de MicroPython.

Estado del proyecto

🚧 Proyecto en desarrollo.

El firmware se utiliza principalmente para desarrollar aplicaciones gráficas con LVGL y MicroPython en la CYD ST7789.

Compatibilidad

Hardware| Compatibilidad
ESP32-2432S028 ST7789| ✅ Probado
ESP32-2432S028 ILI9341| ❌ No destinado a esta variante
Otras CYD| ⚠️ No garantizado

Aviso

Este proyecto no es un firmware oficial de Sunton, Espressif, MicroPython ni LVGL.

La compatibilidad está basada en el hardware utilizado durante el desarrollo y las pruebas del proyecto.

Licencia

El código original desarrollado para este proyecto se distribuye bajo la licencia MIT.

Las partes procedentes de otros proyectos mantienen sus respectivas licencias y derechos de autor.
