import pytest
import argparse
from unittest.mock import patch, MagicMock
import numpy as np

from sinewave.sinewave import parse_frequency, generate_sine_wave, main

# ==========================================
# 1. TESTS FOR parse_frequency()
# ==========================================

@pytest.mark.parametrize("input_str, expected", [
    ("440", 440.0),
    ("440hz", 440.0),
    ("440 Hz", 440.0),
    ("1.4k", 1400.0),
    ("1.4khz", 1400.0),
    ("1.4 kHZ", 1400.0),
    ("22kHz", 22000.0),
    ("  440  ", 440.0),
])
def test_parse_frequency_valid(input_str, expected):
    """Test that valid strings are converted into correct float Hz values."""
    assert parse_frequency(input_str) == expected


@pytest.mark.parametrize("invalid_str", [
    ("flooblesnark"),
    ("440khz123"),
    ("k440"),
    (""),
    ("1.4.4k"),
])
def test_parse_frequency_invalid(invalid_str):
    """Test that invalid formats trigger an argparse ArgumentTypeError."""
    with pytest.raises(argparse.ArgumentTypeError):
        parse_frequency(invalid_str)


# ==========================================
# 2. TESTS FOR generate_sine_wave()
# ==========================================

@patch("os.path.exists")
@patch("soundfile.write")
def test_generate_sine_wave_success(mock_sf_write, mock_exists, capsys):
    """Test standard generation with fades and verbose logs."""
    mock_exists.return_value = False

    generate_sine_wave(
        frequency=440.0,
        duration=2.0,
        sample_rate=44100,
        fade_in=0.5,
        fade_out=0.5,
        output_file="test.wav",
        force=False,
        verbose=True
    )

    mock_sf_write.assert_called_once()
    args, _ = mock_sf_write.call_args
    assert args[0] == "test.wav"
    assert isinstance(args[1], np.ndarray)
    assert args[2] == 44100

    captured = capsys.readouterr()
    assert "Configuring audio" in captured.out
    assert "Applying fades" in captured.out
    assert "Success: Saved" in captured.out


@patch("os.path.exists")
def test_file_exists_no_force(mock_exists, capsys):
    """Test that execution halts if the file exists and --force is omitted."""
    mock_exists.return_value = True

    generate_sine_wave(440.0, 2.0, 44100, 0.0, 0.0, "exists.wav", force=False, verbose=False)

    captured = capsys.readouterr()
    assert "Error: File 'exists.wav' already exists" in captured.out


@patch("os.path.exists")
@patch("soundfile.write")
def test_file_exists_with_force(mock_sf_write, mock_exists, capsys):
    """Test that execution proceeds despite file existence if --force is active."""
    mock_exists.return_value = True

    generate_sine_wave(440.0, 2.0, 44100, 0.0, 0.0, "exists.wav", force=True, verbose=False)
    mock_sf_write.assert_called_once()


@pytest.mark.parametrize("freq, sr", [
    (10.0, 44100),
    (25000.0, 44100),
    (23000.0, 44100),
])
@patch("os.path.exists")
def test_frequency_out_of_bounds(mock_exists, freq, sr, capsys):
    """Test standard bound validations."""
    mock_exists.return_value = False
    generate_sine_wave(freq, 2.0, sr, 0.0, 0.0, "out.wav", force=False, verbose=False)

    captured = capsys.readouterr()
    assert "Error:" in captured.out


@patch("os.path.exists")
@patch("soundfile.write")
def test_soundfile_write_exception(mock_sf_write, mock_exists, capsys):
    """Test catching SoundFile write issues gracefully."""
    mock_exists.return_value = False
    mock_sf_write.side_effect = ValueError("Unsupported extension format simulation.")

    generate_sine_wave(440.0, 1.0, 44100, 0.0, 0.0, "bad.xyz", force=False, verbose=True)

    captured = capsys.readouterr()
    assert "Error: Could not infer format" in captured.out


# ==========================================
# 3. TESTS FOR THE CLI/MAIN PARSER INTERFACE
# ==========================================

@patch("sys.argv", ["sinewave", "440", "5", "--fade-in", "3", "--fade-out", "3"])
def test_main_fades_exceed_duration():
    """Test that CLI errors out if cumulative fades exceed file length."""
    with pytest.raises(SystemExit):
        main()


@patch("sys.argv", ["sinewave", "440", "5"])
@patch("sinewave.sinewave.generate_sine_wave")
def test_main_successful_parse(mock_gen):
    """Verify standard argument combinations transfer perfectly from CLI to main loop."""
    main()
    mock_gen.assert_called_once_with(
        frequency=440.0,
        duration=5.0,
        sample_rate=44100,
        fade_in=0.0,
        fade_out=0.0,
        output_file="sine_wave.wav",
        force=False,
        verbose=False
    )
