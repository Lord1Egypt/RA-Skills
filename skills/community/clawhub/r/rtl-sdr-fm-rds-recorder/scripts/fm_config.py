#!/usr/bin/env python3
"""Shared configuration constants for the broadcast FM IQ/RDS pipeline."""

from __future__ import annotations

from pathlib import Path

RTL_HELP_TIMEOUT_SEC = 3
VERSION_PROBE_TIMEOUT_SEC = 10

IQ_SAMPLE_RATE = 1_024_000.0
AUDIO_SAMPLE_RATE = 24_000
AUDIO_RESAMPLE_UP = 3
AUDIO_RESAMPLE_DOWN = 128
CHANNEL_FILTER_CUTOFF_HZ = 100_000.0
CHANNEL_FILTER_TAPS = 129
DISCRIMINATOR_NOMINAL_PEAK_RAD = 0.5  # ~2π * 75 kHz / 1.024 MHz ≈ 0.46 rad for nominal broadcast-FM deviation.
DEEMPHASIS_TAU = 50e-6  # Europe/Poland FM broadcast

SCAN_NOISE_FLOOR_FRACTION = 0.4  # Estimate the floor from the quietest 40% of bins.
SCAN_PEAK_MIN_ABOVE_NOISE_DB = 8  # Require peaks to stand meaningfully above the estimated floor.
SCAN_MERGE_DISTANCE_HZ = 200_000  # Merge nearby candidate peaks within a single broadcast-FM station cluster.

DEFAULT_GAIN = 19.7
DEFAULT_DURATION_SEC = 10
DEFAULT_RDS_TIMEOUT_SEC = 20
MIN_RDS_SNIFF_SEC_FOR_EARLY_EXIT = 5  # Require a minimum sniff window before trusting early-exit decisions.
EARLY_EXIT_PS_COUNT = 4  # Tuned with the current PS scoring and repeat thresholds; revisit if heuristics change.
EARLY_EXIT_PS_LEAD = 2  # Require a lead over the second-best PS candidate before exiting early.

DEFAULT_REDSEA_PATH = Path('/tmp/redsea/build/redsea')
