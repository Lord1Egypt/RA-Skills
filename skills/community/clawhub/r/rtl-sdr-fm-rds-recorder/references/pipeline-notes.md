# Pipeline Notes

## Recommended pipeline

Direct live demodulation through `rtl_fm` was unreliable for broadcast FM recording in this environment:
- noisy output
- speed / resampling issues
- unstable practical tuning behavior

The reliable path was:
1. capture IQ with `rtl_sdr`
2. decode RDS station name with `rtl_fm` + `redsea`
3. apply a channel filter before FM discrimination
4. offline WBFM demod in Python/Numpy
5. apply `50 us` de-emphasis with `scipy.signal.lfilter` (Europe/Poland)
6. apply rational resampling to 24 kHz audio with `scipy.signal.resample_poly`
7. save WAV
8. encode MP3 with `ffmpeg` using `dynaudnorm` for simple one-pass loudness leveling

## Naming convention

If RDS station name is available, output files should use:

`<StationName>-<Frequency>-<RecordingTimeStart>.mp3`

Example:

`TROJKA-98.7812-20260330-002723.mp3`

If RDS is not available, use fallback:

`UnknownStation-98.7812-20260330-002723.mp3`

## Important environment note

This workflow assumes a Linux environment. Windows is not supported by the current scripts and process-management logic.

This workflow first tries `redsea` from `PATH`, then falls back to:

`/tmp/redsea/build/redsea`

If neither location works, do not continue with staged RDS-based recording as if naming were available. Instead:
- install `redsea` into `PATH`
- or build it again at the expected local path
- or patch the script to point to the correct binary

The skill should be treated as fully ready to use only after `redsea` is installed and reachable.
Run `--check` as an environment check before use:

```bash
python3 scripts/fm_iq_pipeline.py --check
```

If a probe-based tool reports `available: false`, inspect `probeMessage` first. That field contains the first useful stderr/stdout line from the launchability probe, and `probeReturnCode` may also be present.

If `--decode-rds` returns `UnknownStation`, inspect `rds-debug-<freq>.json`, especially `rtlFmStderrFirstLine`, for the first captured `rtl_fm` diagnostic line.

For station naming, the resolver intentionally uses only `ps` and `partial_ps`. `pi` is retained only as auxiliary/debug evidence, and other decoded redsea fields are ignored for naming.

## Useful example commands

Record one station:

```bash
python3 scripts/fm_iq_pipeline.py --record --freq 98.7812 --gain 19.7 --out-dir ./session
```

Scan FM band:

```bash
python3 scripts/fm_iq_pipeline.py --scan-fm --gain 19.7 --out-dir ./session
```

Decode and cache station name for one station:

```bash
python3 scripts/fm_iq_pipeline.py --decode-rds --freq 98.7812 --gain 19.7 --out-dir ./session
```

This step also writes `rds-debug-<Frequency>.json` for troubleshooting station-name selection. That debug JSON includes source-aware resolver output such as accepted/rejected status, confidence, rejection reason, best-candidate details per source, shape classes, per-candidate rejection reasons, `piCounts`, `rawPsCounts`, `rawPartialPsCounts`, `totalObjects`, `validObjects`, `sniffDurationSec`, and `rtlFmStderrFirstLine`. The script may stop the RDS sniff earlier than the full timeout when a PS candidate becomes confidently stable.

`--record --freq` does not run its own station-name sniffing pass. If naming matters, run `--decode-rds --freq` first and let record reuse the cached result from the same `--out-dir`.

By default, successful recording removes intermediate `.bin` and `.wav` files and keeps the MP3 plus metadata JSON. Use `--keep-intermediate` when you want to preserve those extra artifacts.
