# Temperature Log

The BCM2835 System on a Chip of the Raspberry Pi has a temperature sensor that can be used to measure its temperature simply from the command line, giving information on how much heat the chip has generated because of its operation, and - in more extreme cases - giving some information about the temperature of the environment. This project's aim is to create a simple shell script that can run automatically as you boot up your Raspberry Pi, take measurements from the temperature sensor at given intervals and write them into log files that can be viewed later.

![](images/bcm2835.jpg)

## Requirements

### Hardware

- 1 x Raspberry Pi
- 1 x USB keyboard

### Extras

- 1 x Real Time Clock (e.g [RasClock from ModMyPi](https://www.modmypi.com/rasclock-raspberry-pi-real-time-clock-module)) *for creating logs with accurate timestamps*

## Steps

1. Setting up your Raspberry Pi, *and optionally your Real Time Clock*
1. Create the shell script that records the temperature
1. Make your shell script run automatically at startup

## Worksheet & included files

- [The worksheet](WORKSHEET.md)
- (Optional) Final version of the shell script: [temperature_log.sh](temperature_log.sh)
    - Download to your Pi with `wget http://goo.gl/vV2SF5 -O temperature_log.sh --no-check-certificate`

## Licence

Unless otherwise specified, everything in this repository is covered by the following licence:

[![Creative Commons Attribution 4.0 International Licence](http://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

***Temperature Log*** by the [Raspberry Pi Foundation](http://www.raspberrypi.org) is licensed under a [Creative Commons Attribution 4.0 International Licence](http://creativecommons.org/licenses/by-sa/4.0/).

Based on a work at https://github.com/raspberrypilearning/temperature-log
