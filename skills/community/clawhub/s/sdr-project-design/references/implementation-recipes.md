# SDR Implementation Recipes

## Contents
- 1. Pick the right system shape
- 2. Recommended blueprints
- 3. Suggested build order
- 4. Hardware-sharing rules
- 5. Quick decision recipes

## 1. Pick the right system shape

### If the user wants a **radio observatory**
Use:
- one SDR-attached host for hardware ownership
- one service per mode
- one shared dashboard above them
- optional browser receiver as a separate service

### If the user wants a **public-safety intelligence system**
Use:
- `trunk-recorder` or `sdrtrunk` for ingest
- `rdio-scanner` for playback/listening UX
- `scanner-map` for map/AI/event intelligence

### If the user wants a **browser tuning station**
Use:
- `openwebrx+` as the operator-facing layer
- specialized decoders as sidecars when needed

### If the user wants a **satellite station**
Use:
- `SatDump` for record/process pipelines
- a pass scheduler or automation layer around it
- gallery/archive/dashboard on top

### If the user wants **unknown RF / protocol research**
Use:
- `SDR++` or `SigDigger` for live hunting
- `inspectrum` for offline analysis
- `URH` for protocol inference and fuzzing

## 2. Recommended blueprints

### Blueprint A - Home radio observatory
- **Hardware host**: machine physically attached to SDR
- **Mode runtimes**:
  - ADS-B: `readsb` + `tar1090`
  - ISM: `rtl_433`
  - Satellite: `SatDump` or scheduled recorder/decoder
  - APRS: `Dire Wolf`
- **Shared layer**:
  - `status.json`
  - event directories
  - dashboard/API
- **Optional**:
  - `openwebrx+` for free-tuning mode

Use this when the user wants "one place for radio shenanigans."

### Blueprint B - Dispatch / scanner intelligence
- **RF ingest**: `trunk-recorder` or `sdrtrunk`
- **call archive/playback**: `rdio-scanner`
- **intelligence layer**: `scanner-map`
- **optional publish/distribution**: OpenMHz or custom public feed

Use this when the user wants incident maps, transcripts, call playback, alerts, or scanner community features.

### Blueprint C - Browser-first receiver
- **operator UI**: `openwebrx+`
- **extra mode services**: separate specialized decoders if needed
- **storage**: bookmarks, recordings, clips, screenshots, event outputs

Use this when tuning and remote access matter more than event pipelines.

### Blueprint D - Research bench
- **live receiver**: `SDR++`
- **analysis**: `SigDigger`, `inspectrum`
- **protocol work**: `URH`
- **custom decode path**: GNU Radio or custom scripts

Use this when the user is still figuring out what the signal even is.

## 3. Suggested build order

### For a new observatory
1. make one mode reliable
2. expose outputs in a dumb/simple way
3. add dashboard visibility
4. add second mode
5. add automation/scheduling
6. add AI, maps, alerts, and summaries last

### For scanner/public safety
1. prove ingest
2. prove metadata quality
3. prove playback UX
4. add map/intelligence
5. add notifications/integrations

### For satellite
1. prove capture timing
2. prove decoding pipeline
3. prove artifact quality
4. add scheduler/gallery/archive

## 4. Hardware-sharing rules

### One SDR, many jobs
If one SDR must do multiple incompatible modes:
- run mode-specific services
- only let one hardware-owning service run at a time
- use the dashboard to switch modes
- persist outputs separately from mode state

### Multiple SDRs
If multiple SDRs exist:
- dedicate them by mission whenever possible
- do not over-orchestrate early
- stable dedicated receivers beat clever switching most of the time

## 5. Quick decision recipes

### "I want something cool fast"
Recommend:
- ADS-B first (`readsb` + `tar1090`)
- then `rtl_433`
- then satellite or browser receiver

### "I want a scanner app with map intelligence"
Recommend:
- `trunk-recorder` + `rdio-scanner` + `scanner-map`

### "I want to poke around signals manually"
Recommend:
- `SDR++`
- then add `URH` / `inspectrum`

### "I want a browser receiver with better digital voice direction"
Recommend:
- `openwebrx+`

### APRS / packet radio
**Key constraint:** On SDRplay RSP1B, `rtl_fm` cannot access the device directly — the SDRplay API service owns it. Use SoapySDR instead.

**Working stack (RSP1B):**
1. SDRplay API service running on host
2. SoapySDR Python FM demod → 16-bit PCM
3. sox to format/convert
4. FIFO (named pipe) as the handoff
5. direwolf reading from FIFO, decoding 1200 baud AFSK APRS
6. `packets.jsonl` for storage, `status.json` for state

**Minimal test:**
```bash
# Start SDRplay API service
/opt/hostbin/sdrplay_apiService &

# Verify device accessible
rtl_test -d driver=sdrplay   # may fail even when SoapySDR works
python3 -c "import SoapySDR; print(SoapySDR.Device().listSizes())"  # confirm

# Test direwolf alone (no hardware)
echo "K4XYZ-9>APRS,qAS:*hello" | direwolf -c /data/aprs/direwolf.conf
```

**Docker APRS container base image:** `debian:trixie-slim` + `apt-get install rtl-sdr direwolf sox`. Do not assume `rtl_fm` or SoapySDR Python bindings are pre-installed — verify and add as needed.

**Field-tested APRS/NOAA Soapy defaults (to avoid common breakage):**
- Use `SoapySDRDevice_makeStrArgs("driver=sdrplay")` (not legacy `make` signatures).
- Use exact-rate plans to avoid timing drift (`960k -> 48k` or another clean integer decimation path).
- Keep exactly one SDR owner process at a time; use maintenance-mode for ad-hoc captures.
- For audio quality checks, score channels by demodulated voice-band energy, not raw RF power.
- Always validate output WAV duration with `ffprobe` after capture.

**Debug sequence when audio is static:**
1. Verify decode chain using known-good sample WAV (proves downstream DSP/decoder path).
2. Verify Soapy open + stream with short IQ read test (`readStream` returns stable sample counts).
3. Capture 10s on all candidate channels using same DSP chain.
4. Select best channel by voice-band score, then produce final 30s standardized WAV.
5. If all channels score similarly/noise-only, treat as RF front-end issue (antenna/feedline/location), not parser/decoder.

### "I want to design a new SDR product"
Recommend:
- define the dominant mode first
- choose a proven ingest layer from the landscape
- keep UI separate from decoder runtime
- only build custom DSP where the existing projects truly stop helping
