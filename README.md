# TREZOR Core

![TREZOR Core](docs/trezor_core.png)

[![Build Status](https://travis-ci.org/trezor/trezor-core.svg?branch=master)](https://travis-ci.org/trezor/trezor-core) [![gitter](https://badges.gitter.im/trezor/community.svg)](https://gitter.im/trezor/community)

This is the core of the upcoming TREZOR v2.

## Documentation

* [Documentation](docs/)

## Build instructions for emulator

### Linux

#### Debian/Ubuntu

```sh
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install libsdl2-dev:i386 libsdl2-image-dev:i386
make build_unix
```

#### Fedora

```sh
sudo yum install SDL2-devel.i686 SDL2_image-devel.i686
make build_unix
```

#### openSUSE

```sh
sudo zypper install libSDL2-devel-32bit libSDL2_image-devel-32bit
make build_unix
```

### OS X

```sh
brew install --universal sdl2 sdl2_image
make build_unix
```

### Windows

Not supported yet ...

## Build instructions for ARM

### Linux

For flashing firmware to blank device (without bootloader) by `make flash`,
please install [stlink](https://github.com/texane/stlink).

#### Debian/Ubuntu

```sh
sudo apt-get install gcc-arm-none-eabi libnewlib-arm-none-eabi
make build_trezorhal
```

### OS X

1. Download [gcc-arm-none-eabi](https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q3-update/)
2. Follow the [install instructions](https://launchpadlibrarian.net/287100883/readme.txt)
3. To install stlink, run `brew install stlink`
