import argparse
import os
import re

import numpy as np
import soundfile as sf


def parse_frequency(value_str):
    """Custom argparse type parser to handle strings like 440, 1.4k, 22kHz, etc."""
    s = value_str.strip().lower()

    match = re.match(r'^(\d*\.?\d+)\s*(k)?(?:hz)?$', s)
    if not match:
        raise argparse.ArgumentTypeError(
            f"Invalid frequency format: '{value_str}'. Use numbers like '440', '1.4k', or '22kHz'."
        )

    number_part, k_modifier = match.groups()
    freq = float(number_part)

    if k_modifier:
        freq *= 1000

    return freq


def generate_sine_wave(frequency, duration, sample_rate, fade_in, fade_out, output_file, force, verbose):
    if os.path.exists(output_file) and not force:
        print(f"Error: File '{output_file}' already exists. Use -f or --force to overwrite it.")
        return

    if not (20.0 <= frequency <= 22000.0):
        print(f"Error: Frequency ({frequency:g} Hz) out of bounds. Must be between 20 Hz and 22,000 Hz.")
        return

    if frequency >= (sample_rate / 2):
        print(f"Error: Frequency ({frequency:g} Hz) must be less than half the sample rate ({sample_rate / 2} Hz) to avoid aliasing.")
        return

    if verbose:
        print(f"Configuring audio: {frequency:g}Hz for {duration}s at {sample_rate}Hz sample rate.")
        if fade_in > 0 or fade_out > 0:
            print(f"Applying fades: Fade-in = {fade_in}s, Fade-out = {fade_out}s")

    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, endpoint=False)

    audio = np.sin(2 * np.pi * frequency * t)

    envelope = np.ones(total_samples)

    if fade_in > 0:
        fade_in_samples = min(int(sample_rate * fade_in), total_samples)
        envelope[:fade_in_samples] = np.linspace(0.0, 1.0, fade_in_samples)

    if fade_out > 0:
        fade_out_samples = min(int(sample_rate * fade_out), total_samples)
        envelope[-fade_out_samples:] = np.linspace(1.0, 0.0, fade_out_samples)

    audio_signals = audio * envelope
    if verbose:
        print(f"Writing data to '{output_file}' (inferring container format from extension)...")
    try:
        sf.write(output_file, audio_signals, sample_rate)
        print(f"Success: Saved '{output_file}'")
    except ValueError as e:
        print(f"Error: Could not infer format or write file. {e}")
        print("Supported extensions include: .wav, .flac, .ogg, .aiff")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a sine wave audio file with flexible frequency inputs.")
    parser.add_argument("frequency", type=parse_frequency, help="Frequency (e.g., 440, 1.4k, 22kHz)")
    parser.add_argument("duration", type=float, help="Total duration of the audio in seconds")
    parser.add_argument("--fade-in", type=float, default=0.0, help="Fade-in duration in seconds (default: 0.0)")
    parser.add_argument("--fade-out", type=float, default=0.0, help="Fade-out duration in seconds (default: 0.0)")
    parser.add_argument("-s", "--sample-rate", type=int, default=44100, help="Sample rate in Hz (default: 44100)")
    parser.add_argument("-o", "--output", type=str, default="sine_wave.wav", help="Output filename with extension (default: sine_wave.wav)")

    parser.add_argument("-f", "--force", action="store_true", help="Overwrite the output file if it already exists")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    if args.fade_in + args.fade_out > args.duration:
        parser.error("Combined fade-in and fade-out durations cannot exceed the total file duration.")

    return args


def main():
    args = parse_args()

    generate_sine_wave(
        frequency=args.frequency,
        duration=args.duration,
        sample_rate=args.sample_rate,
        fade_in=args.fade_in,
        fade_out=args.fade_out,
        output_file=args.output,
        force=args.force,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
