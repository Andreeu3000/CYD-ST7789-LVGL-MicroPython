# CYD ST7789 MicroPython + LVGL

Firmware personalizado de **MicroPython + LVGL** para la placa **ESP32-2432S028** con pantalla **ST7789 de 2.8 pulgadas y resolución 240×320**.

Este firmware está configurado específicamente para esta variante de la **Cheap Yellow Display (CYD)** y está pensado para ejecutar aplicaciones gráficas desarrolladas con LVGL y MicroPython.

> ⚠️ **IMPORTANTE:** Este firmware está diseñado para la variante de CYD que utiliza el controlador **ST7789**. No lo instales en una CYD con otro controlador de pantalla sin comprobar primero la compatibilidad.

---

## 📟 Hardware compatible

### ESP32-2432S028

- **Microcontrolador:** ESP32
- **Pantalla:** ST7789
- **Resolución:** 240×320
- **Tamaño:** 2.8"
- **Touch:** XPT2046
- **Interfaz:** SPI
- **Firmware:** MicroPython + LVGL

---

## 🖥️ Configuración de la pantalla

| Función | GPIO |
|---|---:|
| MOSI | 13 |
| MISO | 12 |
| SCK | 14 |
| CS | 15 |
| DC | 2 |
| Backlight | 21 |

## 👆 Configuración del touch

| Función | GPIO |
|---|---:|
| MOSI | 32 |
| MISO | 39 |
| SCK | 25 |
| CS | 33 |

---

## 🚀 ¿Qué es este proyecto?

El objetivo de este proyecto es proporcionar un firmware de **MicroPython + LVGL precompilado y configurado específicamente para la CYD ESP32-2432S028 con pantalla ST7789**.

La idea es evitar que sea necesario compilar y configurar manualmente MicroPython, LVGL y los controladores necesarios para comenzar a desarrollar aplicaciones gráficas en esta placa.

---

## ✨ Características

- MicroPython
- LVGL
- Controlador ST7789
- Pantalla de 240×320
- Touch XPT2046
- Wi-Fi
- Configuración específica para ESP32-2432S028
- Firmware precompilado
- Diseñado para aplicaciones gráficas y proyectos con LVGL

---

## 📦 Instalación

Los archivos `.bin` del firmware se encuentran en la sección **Releases** de este repositorio.

Descarga la versión correspondiente a tu placa y sigue las instrucciones de instalación indicadas en la publicación de la versión.

### ⚠️ Antes de instalar

Comprueba que tu placa utiliza:

```text
ESP32-2432S028
ST7789
240×320
