# mksinewave

`mksinewave` is a Python command-line utility for generating pure sine wave audio tones with customizable configurations, smooth attenuation fades, and automatic audio container inference.

[![PyPI Version](https://img.shields.io/pypi/v/mksinewave)](https://pypi.org/project/mksinewave)
[![MIT License](https://img.shields.io/github/license/djstompzone/mksinewave)](https://opensource.org/licenses/MIT)
![PyPI Python Version](https://img.shields.io/pypi/pyversions/mksinewave)

## Features

- **Flexible Frequency Formats:** Accepts standard numbers (`440`), human-friendly shortcuts (`1.4k`), or explicit units (`22kHz`).
- **Smart Fades:** Prevent harsh audio pops and clicks with customizable linear head and tail attenuation (fade-in/fade-out).
- **FFmpeg-Style Extension Inference:** Saves directly to `.wav`, `.flac`, `.ogg`, or `.aiff` by automatically detecting the format from your output filename.
- **Safety Proofed:** Includes built-in human hearing range guards (20 Hz - 22 kHz) and Nyquist frequency anti-aliasing checks.
- **Safe Overwriting:** Protects existing files unless explicitly overridden with the `-f / --force` flag.

## Installation

Clone the repository and install it locally using `pip`:

```bash
pip install mksinewave
```

For active local development, install using the `[dev]` optional dependency group in editable mode:

```bash
pip install -e "mksinewave[dev]"
```

## Usage

Once installed, the global `mksinewave` command is available anywhere on your system.

### Basic Syntax

```bash
mksinewave <frequency> <duration> [options]
```

### Examples

**1. Generate a standard A4 tone (440Hz) for 3 seconds:**

```bash
mksinewave 440 3
```

**2. Generate a 1.5 khz tone for 5 seconds as a compressed FLAC file with a smooth fade-in and fade-out:**

```bash
mksinewave 1.5k 5 --fade-in 0.5 --fade-out 1.0 -o output.flac -v
```

**3. Force overwrite an existing file using a specific sample rate:**

```bash
mksinewave "2.2 kHz" 2.5 -s 48000 -o alert.ogg -f
```

### Available Command-Line Flags

- `--fade-in`: Length of head attenuation fade-in in seconds (Default: 0.0).
- `--fade-out`: Length of tail attenuation fade-out in" seconds (Default: 0.0).
- `-s`, `--sample-rate`: Audio sampling rate in hertz (Default: 44100).
- `-o`, `--output`: Output file path inferred via extension (Default: sine_wave.wav).
- `-f`, `--force`: Overwrite the target file if it already exists.
- `-v`, `--verbose`: Enable logging output detailing the generation process.
- `frequency` (Positional): Target frequency. Supports formats like 440, 1.4k, 22kHz.
- `duration` (Positional): Total length of the audio track in seconds.

## Development & Testing

This project maintains rigorous test coverage using `pytest` and `pytest-cov`.

If you installed the development dependencies, you can execute the test suite globally from the project root directory:

```bash
test-mksinewave
```

## License

This project is licensed under the MIT License.
See the [LICENSE](https://github.com/DJStompZone/mksinewave/blob/main/LICENSE) file for details.
