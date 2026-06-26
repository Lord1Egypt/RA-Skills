#!/usr/bin/env python3
"""Capture IQ from RTL-SDR, decode broadcast FM to MP3, and extract RDS station name.

Working broadcast FM pipeline for this skill:
- capture IQ with rtl_sdr
- decode RDS station name with rtl_fm + redsea
- offline FM discriminator in Python/numpy
- 50 us de-emphasis (Europe/Poland)
- resample to 24 kHz audio with rational resampling
- encode MP3 with ffmpeg
- save as <StationName>-<Frequency>-<RecordingTimeStart>.mp3 when RDS is available
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import heapq
import importlib.util
import json
import math
import os
import shutil
import selectors
import signal
import statistics
import subprocess
import time
import wave
from collections import defaultdict
from pathlib import Path

import numpy as np

from fm_config import (
    AUDIO_RESAMPLE_DOWN,
    AUDIO_RESAMPLE_UP,
    AUDIO_SAMPLE_RATE,
    CHANNEL_FILTER_CUTOFF_HZ,
    CHANNEL_FILTER_TAPS,
    DEFAULT_DURATION_SEC,
    DEFAULT_GAIN,
    DEFAULT_RDS_TIMEOUT_SEC,
    DEFAULT_REDSEA_PATH,
    DEEMPHASIS_TAU,
    DISCRIMINATOR_NOMINAL_PEAK_RAD,
    EARLY_EXIT_PS_COUNT,
    EARLY_EXIT_PS_LEAD,
    IQ_SAMPLE_RATE,
    MIN_RDS_SNIFF_SEC_FOR_EARLY_EXIT,
    RTL_HELP_TIMEOUT_SEC,
    SCAN_MERGE_DISTANCE_HZ,
    VERSION_PROBE_TIMEOUT_SEC,
    SCAN_NOISE_FLOOR_FRACTION,
    SCAN_PEAK_MIN_ABOVE_NOISE_DB,
)
from rds_observation import add_redsea_object, create_rds_evidence, sanitize_station_name
from station_identity import (
    MIN_STATION_SCORE_FOR_CONFIDENCE,
    resolve_station_identity,
    select_best_candidate,
)
from station_identity_debug import build_rds_debug_info

SCIPY_SPEC = importlib.util.find_spec('scipy')
if SCIPY_SPEC is not None:
    try:
        import scipy
        from scipy.signal import firwin, lfilter, resample_poly
    except ImportError:
        scipy = None
        firwin = None
        lfilter = None
        resample_poly = None
else:
    scipy = None
    firwin = None
    lfilter = None
    resample_poly = None

_CHANNEL_FILTER: np.ndarray | None = None


def resolve_redsea_bin() -> Path | None:
    redsea_in_path = shutil.which('redsea')
    if redsea_in_path:
        return Path(redsea_in_path)
    if DEFAULT_REDSEA_PATH.exists():
        return DEFAULT_REDSEA_PATH
    return None


def require_scipy() -> None:
    if scipy is None or firwin is None or lfilter is None or resample_poly is None:
        raise SystemExit("scipy is required for audio processing. Install python3-scipy.")


def detect_tool_version(command: list[str], banner_prefixes: tuple[str, ...] = ()) -> str | None:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=VERSION_PROBE_TIMEOUT_SEC)
    except (OSError, subprocess.SubprocessError):
        return None

    output_parts = []
    if result.stdout:
        output_parts.append(result.stdout.strip())
    if result.stderr:
        output_parts.append(result.stderr.strip())
    if not output_parts:
        return None

    lines = [line.strip() for line in '\n'.join(output_parts).splitlines() if line.strip()]
    if banner_prefixes:
        for line in lines:
            if line.startswith(banner_prefixes):
                return line

    first_line = lines[0] if lines else None
    if first_line and 'invalid option' in first_line.lower():
        return None
    return first_line or None


def probe_tool(command: list[str]) -> dict:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=RTL_HELP_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        return {'available': False, 'probeMessage': 'Timed out during probe'}
    except OSError as exc:
        return {'available': False, 'probeMessage': str(exc)}
    except subprocess.SubprocessError as exc:
        return {'available': False, 'probeMessage': str(exc)}

    output = '\n'.join(part for part in (result.stdout, result.stderr) if part)
    first_line = next((line.strip() for line in output.splitlines() if line.strip()), None)
    # Return code 127 traditionally means command-not-found from the invoked binary or shell.
    # For this probe, any other return code still proves the tool launched and responded.
    # RTL tools do not implement a real --help flag; they print usage on stderr and exit quickly with 1.
    return {
        'available': result.returncode != 127,
        'probeReturnCode': result.returncode,
        'probeMessage': first_line,
    }


def probe_rtl_tool(name: str) -> dict:
    if shutil.which(name) is None:
        return {'available': False, 'probeMessage': 'Not found in PATH'}
    return probe_tool([name, '--help'])


def environment_check() -> dict:
    redsea_bin = resolve_redsea_bin()
    rtl_sdr_probe = probe_rtl_tool('rtl_sdr')
    rtl_fm_probe = probe_rtl_tool('rtl_fm')
    rtl_power_probe = probe_rtl_tool('rtl_power')
    redsea_probe = probe_tool([str(redsea_bin), '--help']) if redsea_bin is not None else {'available': False, 'probeMessage': 'Not found in PATH or fallback location'}
    checks = {
        'rtl_sdr': rtl_sdr_probe,
        'rtl_fm': rtl_fm_probe,
        'rtl_power': rtl_power_probe,
        'ffmpeg': {
            'available': shutil.which('ffmpeg') is not None,
            'version': detect_tool_version(['ffmpeg', '-version']),
        },
        'python3': {
            'available': shutil.which('python3') is not None,
            'version': detect_tool_version(['python3', '--version']),
        },
        'scipy': {
            'available': scipy is not None,
            'version': (
                getattr(getattr(scipy, 'version', None), 'full_version', None)
                or getattr(scipy, '__version__', None)
            ) if scipy is not None else None,
            'installHint': None if scipy is not None else 'Install python3-scipy',
        },
        'redsea': {
            **redsea_probe,
            'path': str(redsea_bin) if redsea_bin is not None else None,
        },
    }
    return checks


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        details = [f"Command failed ({result.returncode}): {' '.join(cmd)}"]
        if result.stdout:
            details.append(f"stdout:\n{result.stdout.strip()}")
        if result.stderr:
            details.append(f"stderr:\n{result.stderr.strip()}")
        raise SystemExit("\n".join(details))


def process_redsea_output_chunk(
    chunk: bytes,
    buffer: bytearray,
    evidence,
) -> bool:
    buffer.extend(chunk)

    while b'\n' in buffer:
        raw_line, _, remainder = buffer.partition(b'\n')
        buffer[:] = remainder
        line = raw_line.decode('utf-8', errors='replace').strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        ps = obj.get("ps")
        add_redsea_object(evidence, obj)

        if ps:
            best_ps_candidate = select_best_candidate(evidence, evidence.ps_counts, 'ps')
            top_counts = heapq.nlargest(2, evidence.ps_counts.values())
            second_best_ps_count = top_counts[1] if len(top_counts) > 1 else 0
            # Early exit is intentionally based only on full PS, not partial PS.
            # Partial PS is useful for fallback naming, but not stable enough for early termination.
            if (
                best_ps_candidate is not None
                and best_ps_candidate.score >= MIN_STATION_SCORE_FOR_CONFIDENCE
                and best_ps_candidate.count >= EARLY_EXIT_PS_COUNT
                and (best_ps_candidate.count - second_best_ps_count) >= EARLY_EXIT_PS_LEAD
            ):
                return True

    return False


def detect_station_name(freq_mhz: float, gain_db: float, timeout_sec: int = DEFAULT_RDS_TIMEOUT_SEC) -> tuple[str, dict]:
    redsea_bin = resolve_redsea_bin()
    if redsea_bin is None:
        evidence = create_rds_evidence()
        result = resolve_station_identity(evidence)
        result.source = 'missing-redsea'
        result.rejection_reason = 'redsea-not-found'
        return "UnknownStation", build_rds_debug_info(freq_mhz, timeout_sec, evidence, result)

    rtl_fm_proc = subprocess.Popen(
        [
            'rtl_fm', '-M', 'fm', '-l', '0', '-A', 'std', '-p', '0', '-s', '171k',
            '-g', str(gain_db), '-F', '9', '-f', f'{freq_mhz}M'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,
        bufsize=0,
        start_new_session=True,
    )
    if rtl_fm_proc.stdout is None:
        raise RuntimeError("rtl_fm stdout pipe was not created")
    proc = subprocess.Popen(
        [str(redsea_bin), '-r', '171000', '-p'],
        stdin=rtl_fm_proc.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=False,
        bufsize=0,
        start_new_session=True,
    )
    rtl_fm_proc.stdout.close()

    evidence = create_rds_evidence()
    selector = selectors.DefaultSelector()
    if proc.stdout is None:
        raise RuntimeError("redsea stdout pipe was not created")
    if rtl_fm_proc.stderr is None:
        raise RuntimeError("rtl_fm stderr pipe was not created")
    selector.register(proc.stdout, selectors.EVENT_READ, data='redsea_stdout')
    selector.register(rtl_fm_proc.stderr, selectors.EVENT_READ, data='rtl_fm_stderr')
    start_time = time.monotonic()
    buffer = bytearray()
    rtl_fm_stderr_buffer = bytearray()
    redsea_stdout_open = True
    rtl_fm_stderr_open = True

    early_exit = False
    try:
        while True:
            elapsed = time.monotonic() - start_time
            if elapsed >= timeout_sec or early_exit:
                break
            if not redsea_stdout_open and not rtl_fm_stderr_open:
                break

            events = selector.select(timeout=0.5)
            for key, _ in events:
                chunk = os.read(key.fd, 4096)
                if not chunk:
                    selector.unregister(key.fileobj)
                    if key.data == 'redsea_stdout':
                        redsea_stdout_open = False
                    else:
                        rtl_fm_stderr_open = False
                    continue

                if key.data == 'redsea_stdout':
                    should_early_exit = process_redsea_output_chunk(chunk, buffer, evidence)
                    if elapsed >= MIN_RDS_SNIFF_SEC_FOR_EARLY_EXIT and should_early_exit:
                        early_exit = True
                        break
                else:
                    rtl_fm_stderr_buffer.extend(chunk)
            if early_exit:
                break
    finally:
        selector.close()
        for child in (proc, rtl_fm_proc):
            try:
                os.killpg(os.getpgid(child.pid), signal.SIGTERM)
            except ProcessLookupError:
                pass
        deadline = time.monotonic() + 5
        redsea_stdout_bytes = b''
        rtl_fm_stderr_bytes = b''
        for child in (proc, rtl_fm_proc):
            remaining = max(0.1, deadline - time.monotonic())
            try:
                stdout_data, stderr_data = child.communicate(timeout=remaining)
            except subprocess.TimeoutExpired:
                child.kill()
                stdout_data, stderr_data = child.communicate()
            if child is proc and stdout_data:
                redsea_stdout_bytes = stdout_data
            if child is rtl_fm_proc and stderr_data:
                rtl_fm_stderr_bytes = stderr_data
        if rtl_fm_stderr_bytes:
            rtl_fm_stderr_buffer.extend(rtl_fm_stderr_bytes)
        if rtl_fm_stderr_buffer:
            evidence.rtl_fm_stderr_first_line = next(
                (
                    line.strip()
                    for line in rtl_fm_stderr_buffer.decode('utf-8', errors='replace').splitlines()
                    if line.strip()
                ),
                None,
            )
        if redsea_stdout_bytes:
            process_redsea_output_chunk(redsea_stdout_bytes, buffer, evidence)

    evidence.sniff_duration_sec = min(timeout_sec, time.monotonic() - start_time)
    result = resolve_station_identity(evidence)
    debug_info = build_rds_debug_info(freq_mhz, timeout_sec, evidence, result)
    return result.station_name, debug_info


def get_channel_filter_coefficients() -> np.ndarray:
    global _CHANNEL_FILTER
    if _CHANNEL_FILTER is None:
        require_scipy()
        taps = firwin(CHANNEL_FILTER_TAPS, CHANNEL_FILTER_CUTOFF_HZ, fs=IQ_SAMPLE_RATE)
        taps.setflags(write=False)
        _CHANNEL_FILTER = taps
    return _CHANNEL_FILTER


def capture_iq(freq_mhz: float, duration_sec: int, gain_db: float, iq_path: Path) -> None:
    sample_count = int(IQ_SAMPLE_RATE * duration_sec)
    cmd = [
        "rtl_sdr",
        "-f",
        f"{freq_mhz}M",
        "-s",
        str(int(IQ_SAMPLE_RATE)),
        "-g",
        str(gain_db),
        "-n",
        str(sample_count),
        str(iq_path),
    ]
    run(cmd)


def demodulate_wbfm(iq_path: Path, wav_path: Path) -> None:
    require_scipy()
    data = np.fromfile(iq_path, dtype=np.uint8)
    if data.size < 2:
        raise RuntimeError(f"IQ file is empty: {iq_path}")

    i = (data[0::2].astype(np.float32) - 127.5) / 128.0
    q = (data[1::2].astype(np.float32) - 127.5) / 128.0
    x = i + 1j * q
    x = x - np.mean(x)
    channel_filter = get_channel_filter_coefficients().astype(np.float32, copy=False)
    x = lfilter(channel_filter, [1.0], x).astype(np.complex64, copy=False)

    y = np.angle(x[1:] * np.conj(x[:-1]))

    alpha = math.exp(-1.0 / (IQ_SAMPLE_RATE * DEEMPHASIS_TAU))
    z = lfilter([1 - alpha], [1, -alpha], y)

    z = resample_poly(z, AUDIO_RESAMPLE_UP, AUDIO_RESAMPLE_DOWN)
    z = z - np.mean(z)
    z = np.clip(z / DISCRIMINATOR_NOMINAL_PEAK_RAD, -1.0, 1.0)

    pcm = np.int16(z * 32767)

    with wave.open(str(wav_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(AUDIO_SAMPLE_RATE)
        wav_file.writeframes(pcm.tobytes())


def encode_mp3(wav_path: Path, mp3_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(wav_path),
        "-af",
        "dynaudnorm",
        "-c:a",
        "libmp3lame",
        "-b:a",
        "128k",
        str(mp3_path),
    ]
    run(cmd)


def scan_fm_band(out_dir: Path, gain_db: float, integration_sec: int = 30) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / 'fm_scan.csv'
    cmd = [
        'rtl_power',
        '-g', str(gain_db),
        '-f', '88M:108M:100k',
        '-i', '5',
        '-e', f'{integration_sec}s',
        str(csv_path),
    ]
    run(cmd)

    rows = []
    with csv_path.open() as f:
        reader = csv.reader(f, skipinitialspace=True)
        for row in reader:
            start = int(row[2])
            step = float(row[4])
            vals = [float(x) for x in row[6:] if x != '']
            for i, v in enumerate(vals):
                rows.append((start + i * step, v))

    acc: dict[float, list[float]] = defaultdict(list)
    for freq, val in rows:
        acc[freq].append(val)

    agg = [(freq, statistics.mean(vals)) for freq, vals in sorted(acc.items())]
    means = [x[1] for x in agg]
    noise_floor = statistics.mean(sorted(means)[: max(1, int(len(means) * SCAN_NOISE_FLOOR_FRACTION))])

    peaks = []
    for i in range(1, len(agg) - 1):
        freq, mean = agg[i]
        if (
            mean > agg[i - 1][1]
            and mean >= agg[i + 1][1]
            and mean - noise_floor > SCAN_PEAK_MIN_ABOVE_NOISE_DB
        ):
            peaks.append((freq, mean, mean - noise_floor))

    merged = []
    for peak in sorted(peaks, key=lambda item: item[0]):
        if not merged:
            merged.append(list(peak))
            continue

        last_peak = merged[-1]
        if abs(peak[0] - last_peak[0]) <= SCAN_MERGE_DISTANCE_HZ:
            if peak[1] > last_peak[1]:
                merged[-1] = list(peak)
        else:
            merged.append(list(peak))

    results = []
    for freq, mean, above_noise in sorted(merged, key=lambda x: x[1], reverse=True):
        freq_mhz = round(freq / 1e6, 4)
        results.append(
            {
                'stationName': 'UnknownStation',
                'frequencyMHz': freq_mhz,
                'meanDb': round(mean, 2),
                'aboveNoise': round(above_noise, 2),
            }
        )

    summary_path = out_dir / 'fm_scan_summary.json'
    summary_path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    return results


def rds_cache_path(out_dir: Path, freq_mhz: float) -> Path:
    return out_dir / f"rds-{freq_mhz:.4f}.json"


def load_cached_station_name(out_dir: Path, freq_mhz: float) -> str | None:
    cache_path = rds_cache_path(out_dir, freq_mhz)
    if not cache_path.exists():
        return None
    try:
        data = json.loads(cache_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return sanitize_station_name(str(data.get("stationName", "UnknownStation")))


def decode_rds_for_frequency(freq_mhz: float, gain_db: float, out_dir: Path, timeout_sec: int = DEFAULT_RDS_TIMEOUT_SEC) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    station_name, debug_info = detect_station_name(freq_mhz, gain_db, timeout_sec=timeout_sec)
    result = {
        'frequencyMHz': round(freq_mhz, 4),
        'stationName': station_name,
    }
    rds_cache_path(out_dir, freq_mhz).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (out_dir / f"rds-debug-{freq_mhz:.4f}.json").write_text(json.dumps(debug_info, ensure_ascii=False, indent=2) + '\n')
    return result


def record_frequency(
    freq_mhz: float,
    duration_sec: int,
    gain_db: float,
    out_dir: Path,
    keep_intermediate: bool = False,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    recording_start = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    freq_str = f"{freq_mhz:.4f}"

    station_name = load_cached_station_name(out_dir, freq_mhz)
    if station_name is None:
        station_name = "UnknownStation"
    base_name = f"{station_name}-{freq_str}-{recording_start}"

    iq_path = out_dir / f"{base_name}.bin"
    wav_path = out_dir / f"{base_name}.wav"
    mp3_path = out_dir / f"{base_name}.mp3"
    json_path = out_dir / f"{base_name}.json"

    capture_iq(freq_mhz, duration_sec, gain_db, iq_path)
    demodulate_wbfm(iq_path, wav_path)
    encode_mp3(wav_path, mp3_path)

    metadata = {
        "stationName": station_name,
        "frequencyMHz": freq_mhz,
        "recordingTimeStart": recording_start,
        "gainDb": gain_db,
        "durationSec": duration_sec,
        "mp3Path": str(mp3_path),
    }
    if keep_intermediate:
        metadata["iqPath"] = str(iq_path)
        metadata["wavPath"] = str(wav_path)
    else:
        iq_path.unlink(missing_ok=True)
        wav_path.unlink(missing_ok=True)
    json_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return mp3_path


def validate_freq(freq_mhz: float) -> None:
    if not (88.0 <= freq_mhz <= 108.0):
        raise SystemExit("--freq must be within the broadcast FM band: 88.0 to 108.0 MHz")


def validate_gain(gain_db: float) -> None:
    if gain_db < 0.0:
        raise SystemExit("--gain must be non-negative")


def validate_duration(duration_sec: int) -> None:
    if duration_sec <= 0:
        raise SystemExit("--duration must be a positive integer")


def validate_action_args(args: argparse.Namespace) -> None:
    action_count = sum(bool(action) for action in (args.check, args.scan_fm, args.decode_rds, args.record))
    if action_count != 1:
        raise SystemExit("Provide exactly one action: --check, --scan-fm, --decode-rds, or --record")

    if args.check:
        return
    if args.scan_fm:
        validate_gain(args.gain)
        return
    if args.decode_rds:
        if args.freq is None:
            raise SystemExit("Provide --freq with --decode-rds")
        validate_freq(args.freq)
        validate_gain(args.gain)
        return
    if args.record:
        if args.freq is None:
            raise SystemExit("Provide --freq with --record")
        validate_freq(args.freq)
        validate_gain(args.gain)
        validate_duration(args.duration)
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture IQ, decode WBFM to MP3, extract RDS station name, or scan FM band")
    parser.add_argument("--freq", type=float, help="Single frequency in MHz within the broadcast FM band, e.g. 98.7812")
    parser.add_argument("--scan-fm", action="store_true", help="Scan the 88-108 MHz broadcast FM band and print candidates")
    parser.add_argument("--decode-rds", action="store_true", help="Decode RDS station name for the provided --freq")
    parser.add_argument("--record", action="store_true", help="Record one station for the provided --freq")
    parser.add_argument("--check", action="store_true", help="Run environment check for required tools and binaries")
    parser.add_argument("--duration", type=int, default=DEFAULT_DURATION_SEC, help="Capture duration in seconds")
    parser.add_argument("--gain", type=float, default=DEFAULT_GAIN, help="RTL-SDR gain in dB")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("output"),
        help="Directory for output files",
    )
    parser.add_argument(
        "--keep-intermediate",
        action="store_true",
        help="Keep intermediate .bin and .wav files after successful MP3 creation",
    )
    args = parser.parse_args()
    validate_action_args(args)

    if args.check:
        print(json.dumps(environment_check(), ensure_ascii=False, indent=2))
        return

    if args.scan_fm:
        print(json.dumps(scan_fm_band(args.out_dir, args.gain), ensure_ascii=False, indent=2))
        return

    if args.decode_rds:
        result = decode_rds_for_frequency(args.freq, args.gain, args.out_dir)
        print(json.dumps([result], ensure_ascii=False, indent=2))
        return

    if args.record:
        mp3_path = record_frequency(args.freq, args.duration, args.gain, args.out_dir, args.keep_intermediate)
        print(mp3_path)
        return


if __name__ == "__main__":
    main()
