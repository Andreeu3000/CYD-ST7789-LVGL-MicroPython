# CYD ST7789 MicroPython + LVGL

Firmware de MicroPython con LVGL preparado para la **ESP32-2432S028** con pantalla **ST7789 de 240×320**.

Lo hice para tener una versión de MicroPython + LVGL que ya venga configurada para esta CYD y poder usarla directamente para mis proyectos.

## ⚠️ Importante

Este firmware es **específico para la versión con ST7789**.

No lo flashees en una CYD con ILI9341 u otro controlador de pantalla.

Antes de instalarlo, asegúrate de que tu placa sea compatible.

## Hardware

**Placa:** ESP32-2432S028  
**Pantalla:** ST7789  
**Resolución:** 240×320  
**Touch:** XPT2046

### Pantalla

| Función | GPIO |
|---|---:|
| MOSI | 13 |
| MISO | 12 |
| SCK | 14 |
| CS | 15 |
| DC | 2 |
| Backlight | 21 |

### Touch

| Función | GPIO |
|---|---:|
| MOSI | 32 |
| MISO | 39 |
| SCK | 25 |
| CS | 33 |

## ¿Para qué sirve?

La idea es simplemente tener un firmware listo para empezar a hacer cosas con la CYD usando:

- MicroPython
- LVGL
- ST7789
- XPT2046

Sin tener que compilar y configurar todo desde cero cada vez.

## 📦 Firmware

Las versiones compiladas estarán disponibles en **Releases**.

Cada release tendrá su propio archivo `.bin` y la información necesaria para instalarlo.

## 🧪 Estado

Proyecto en desarrollo.

El firmware se va probando directamente en una **ESP32-2432S028 con ST7789**, así que otras variantes de CYD pueden no funcionar.

## Créditos

Este proyecto utiliza:

- MicroPython
- LVGL

No es un firmware oficial de MicroPython, LVGL, Espressif ni Sunton.

## 🐍 Ejemplo rápido

En `examples/simple.py` hay un ejemplo mínimo para comprobar que el firmware funciona correctamente.

Ejecuta el archivo `simple.py` en la placa.

Si todo está funcionando, aparecerá:

**Hola mundo**

---

Hecho por **Andreeu3000**.
