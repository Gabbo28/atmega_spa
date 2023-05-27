# atmega_spa
Password recovery via SPA on atmega328p, using a Rigol DS1102Z-E.

![ATmega328P Pinout](./imgs/atmega328-pinout.png "ATmega328P Pinout")

The hardware setup and the code runing on the MCU (src/spa.ino) are taken from "The Hardware Hacking Handbook, Breaking Embedded Security with Hardware Attacks" by Colin O'Flynn and Jasper van Woudenberg.

Library used for comunicating with the oscilloscope (instruments.py) is forked from https://github.com/nathankjer/instruments, with some minor changes.
