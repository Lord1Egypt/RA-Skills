---
name: rtl-sdr-fm-rds-recorder
description: Record broadcast FM stations from an RTL-SDR using a reliable IQ-capture workflow with offline WBFM demodulation, RDS station-name extraction, and automatic MP3 naming. Use when working with RTL-SDR broadcast FM tasks such as scanning stations, recording radio audio, extracting RDS or PS station names, or saving files with station-name frequency time naming.
---

# RTL-SDR FM RDS Recorder

## Overview

Use this skill for reliable broadcast FM recording from an RTL-SDR. The preferred workflow is IQ capture with `rtl_sdr`, RDS station-name extraction, offline WBFM demodulation, and MP3 export. This skill currently targets Linux environments and should be treated as Linux-only.

## Workflow

1. Run `--check` to confirm the RTL-SDR is available and reachable before promising the skill is ready to use.
2. Confirm `redsea` is installed and reachable, either from `PATH` or from the expected local fallback path, before promising full RDS-ready behavior.
3. If `redsea` is missing, rebuild or reinstall it before running `--decode-rds` or any staged recording flow that depends on station naming.
4. When the user wants to discover stations first, run broadcast FM band scan mode and return a list of candidates with frequency and relative strength. Do not promise station names from scan mode alone.
5. Use `scripts/fm_iq_pipeline.py` for recording.
6. If needed, read `references/pipeline-notes.md` for setup-specific caveats.
7. Prefer a staged workflow: scan first, then decode RDS for one chosen frequency, then record that same chosen station with `--record --freq`, using the same `--out-dir` for both steps.
8. Return the produced MP3 file(s) to the user and mention station name / frequency.
9. For Telegram file delivery, send media-only replies when attaching generated files. Do not mix explanatory text with the `MEDIA:...` token in the same message; send the file attachment as its own message. If one reply contains multiple `MEDIA:...` tokens, put each token on its own line.

## Dependencies

This skill is Linux-only and is only fully ready to use when these tools are present.
- `rtl_sdr`
- `rtl_fm`
- `rtl_power`
- `ffmpeg`
- `python3`
- `numpy`
- `scipy`
- `redsea`

If `redsea` is missing, the recording pipeline may still work, but RDS station-name extraction and final file naming will fall back to `UnknownStation`. If `scipy` is missing, recording and demodulation are unavailable; `--check` and `--scan-fm` still work. The script first tries `redsea` from `PATH`, then falls back to the expected local path.

## Quick Start

Run `--check` first:

```bash
python3 scripts/fm_iq_pipeline.py --check
```

`--check` returns JSON. If a tool reports `available: false`, inspect `probeMessage` first; it contains the first useful line from the probe stderr/stdout. `probeReturnCode` is also included for probe-based checks when available.

Scan FM broadcast band first:

```bash
python3 scripts/fm_iq_pipeline.py --scan-fm --gain 19.7 --out-dir ./session
```

Decode RDS for one selected station and cache the resulting station name for later recording. For station naming, the resolver only uses `ps` and `partial_ps`; `pi` is kept only as auxiliary/debug evidence, and other decoded RDS fields are intentionally ignored for naming:

```bash
python3 scripts/fm_iq_pipeline.py --decode-rds --freq 98.7812 --gain 19.7 --out-dir ./session
```

If `--decode-rds` returns `UnknownStation`, inspect `rds-debug-<freq>.json`, especially `rtlFmStderrFirstLine`, for diagnostics.

Record one station using the cached result from the earlier decode step. Use the same `--out-dir` value:

```bash
python3 scripts/fm_iq_pipeline.py --record --freq 98.7812 --gain 19.7 --out-dir ./session
```

For longer recordings, pass `--duration 300` (5 minutes):

```bash
python3 scripts/fm_iq_pipeline.py --record --freq 98.7812 --gain 19.7 --duration 300 --out-dir ./session
```

By default, `--record` captures a short 10-second sample. Treat that as a station sample rather than a full-length recording unless you explicitly provide a longer `--duration`.

By default, output is written to `./output` relative to the current working directory. For staged workflows, prefer passing an explicit shared `--out-dir` value such as `./session`.

By default, successful recording keeps the MP3 and metadata JSON, but removes intermediate `.bin` and `.wav` files. Use `--keep-intermediate` when you need those artifacts for debugging or analysis.

## Stdout Output

- `--check` prints a JSON object keyed by tool name.
- `--scan-fm` prints a JSON array sorted by signal strength (strongest first). Each element includes `stationName`, `frequencyMHz`, `meanDb`, and `aboveNoise`.
- `--decode-rds` prints a JSON array with one element containing `frequencyMHz` and `stationName`.
- `--record` prints the path to the produced MP3 file as plain text.
- On Telegram, when returning a generated file to the user, send a separate media-only message containing just the `MEDIA:...` token so the platform treats it as an actual attachment.
- If a single reply contains multiple `MEDIA:...` tokens, put each token on its own line.

Examples:

```json
[{"stationName": "UnknownStation", "frequencyMHz": 98.7812, "meanDb": -28.5, "aboveNoise": 14.2}]
```

```json
[{"frequencyMHz": 98.7812, "stationName": "TROJKA"}]
```

```text
./session/TROJKA-98.7812-20260409-143022.mp3
```

## Expected Runtime

- `--scan-fm` takes about 30 seconds by default.
- `--decode-rds` can take up to about 20 seconds, but may finish earlier when early-exit conditions are met.
- `--record` takes roughly the requested `--duration` plus demodulation and MP3 encoding overhead.
- Full broadcast-FM orchestration over many stations can take several minutes.

## Example User Requests

These are examples of natural-language requests the assistant may receive. The assistant should interpret them as orchestration on top of this skill's atomic commands.

### Full broadcast FM band pass

Example request:

```text
Scan the entire broadcast FM band, go through all detected stations, extract the station name for each one, record audio, and send me all resulting MP3 files.
```

Expected orchestration:
- run `--check`
- run `--scan-fm --gain <dB> --out-dir ./session`
- for each found station:
  - run `--decode-rds --freq <MHz> --gain <dB> --out-dir ./session`
  - run `--record --freq <MHz> --gain <dB> --out-dir ./session`
- return all produced audio files to the user

### Top-N strongest broadcast FM stations

Example request:

```text
Scan the broadcast FM band, take the 5 strongest stations, extract their station names, record audio for them, and send me the MP3 files.
```

Expected orchestration:
- run `--check`
- run `--scan-fm --gain <dB> --out-dir ./session`
- select the strongest N stations from scan results
- for each selected station:
  - run `--decode-rds --freq <MHz> --gain <dB> --out-dir ./session`
  - run `--record --freq <MHz> --gain <dB> --out-dir ./session`
- return the produced audio files to the user

### Single-station flow

Example request:

```text
Record 90.9688 MHz from the broadcast FM band and label the file with the station name.
```

Expected orchestration:
- run `--check`
- run `--decode-rds --freq 90.9688 --gain <dB> --out-dir ./session`
- run `--record --freq 90.9688 --gain <dB> --out-dir ./session`
- return the produced MP3 to the user

## Output Expectations

The script should:
- in `--scan-fm` mode, save scan results and return frequency candidates only
- in `--decode-rds --freq` mode, try to extract the RDS station name and save it to a per-frequency cache file `rds-<Frequency>.json` plus a diagnostic file `rds-debug-<Frequency>.json`
- in `--record --freq` mode, produce MP3 and metadata JSON (intermediate IQ and WAV are removed by default; pass `--keep-intermediate` to retain them)
- `--record --freq` must use the cached result from the earlier decode step for station naming and must not run a second independent RDS naming pass
- `--decode-rds --freq` and `--record --freq` must use the same `--out-dir` value when staged naming consistency matters
- if no cache exists in that `--out-dir`, `--record --freq` falls back to `UnknownStation`
- name the MP3 as:
  - `<StationName>-<Frequency>-<RecordingTimeStart>.mp3`

## When to Read References

Read `references/pipeline-notes.md` when:
- the FM result sounds wrong or unstable
- RDS naming fails or looks inconsistent between decode and record steps
- `redsea` location or environment setup is in doubt
- you need example commands or naming details
- you need the rationale for staged scan → decode-rds → record usage

## Resources

### scripts/
- `scripts/fm_iq_pipeline.py` — main working FM + RDS pipeline orchestration
- `scripts/fm_config.py` — shared DSP, scan, timeout, and path constants
- `scripts/rds_observation.py` — RDS evidence collection and station-name sanitizing helpers
- `scripts/station_identity.py` — station identity resolver and candidate selection policy
- `scripts/station_identity_debug.py` — debug/report generation for RDS identity decisions

### references/
- `references/pipeline-notes.md` — setup-specific notes, naming, caveats, and examples
