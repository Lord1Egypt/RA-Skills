# General Desktop / Utility SDR Projects

## Desktop live exploration

### SDR++
- Repo: `AlexandreRouma/SDRPlusPlus`
- Cross-platform, modular, lightweight-feeling desktop SDR app
- Strongest modern desktop baseline for “fast, pleasant, plugin-capable” SDR UI
- Best for:
  - general listening
  - tuning around unknown bands before deeper tooling
  - users who want immediate success without building a headless stack first
- Why it matters:
  - wide hardware support
  - modern UI
  - low friction compared with heavier frameworks

### GQRX
- Repo: `gqrx-sdr/gqrx`
- Classic desktop receiver/explorer
- Useful baseline for feature expectations in a desktop app
- Best for:
  - Linux/macOS operators
  - traditional receiver workflows
  - users who want a mature, stable, no-drama desktop path

### CubicSDR
- Repo: `cjcliffe/CubicSDR`
- Cross-platform desktop SDR app with SoapySDR integration
- Good historical reference for broad device support and desktop visualization
- Better as a comparison point than a universal first pick

### SDRangel
- Broad “kitchen sink” DSP app
- Great reference for breadth and ambition; less ideal as a default simplicity model
- Use when the user wants one giant toolbox and accepts the complexity cost

## Utility / mode-specific projects

### readsb + tar1090
- Default reference stack for ADS-B / aircraft observability
- `readsb` / `dump1090` class decoders handle ingest
- `tar1090` provides the polished map/operator UI
- Best for:
  - always-on aircraft tracking
  - web map UI
  - historical/operational observability more than live knob-turning
- Design pattern:
  - decoder service
  - map/UI service
  - optional feeders / exporters

### Dire Wolf
- Practical APRS / AX.25 software TNC reference
- Good for receive-only monitoring, digipeater, igate, and packet experimentation
- Best when the SDR can be turned into clean audio/baseband before packet decode

### rtl_433
- Core decoder for many consumer/weather/sensor devices in ISM bands
- Best when the protocol/device is already known
- One of the highest-value SDR utilities because it turns RF into useful structured output fast
- Strong outputs include:
  - JSON
  - CSV
  - MQTT
  - Influx
  - syslog
  - trigger hooks
- Great for:
  - weather stations
  - door/window sensors
  - TPMS
  - utility-ish devices
  - Home Assistant / automation pipelines

### rtlamr
- Narrow, useful reference for utility meter decoding
- Best as a focused service inside a broader observability stack

## Best-fit guidance

### If you want a human-operated RF workstation
Use:
- `SDR++` first
- `GQRX` / `CubicSDR` as comparison references
- `SDRangel` for maximalist inspiration

### If you want aircraft tracking / ADS-B
Use:
- `readsb` or equivalent decoder first
- `tar1090` as the visual/operator layer

### If you want APRS / packet / igate work
Use:
- `Dire Wolf` first
- then add mapping, uplink, or gateway behavior around it

### If you want ISM / sensor observability
Use:
- `rtl_433` first
- route structured events to MQTT, Influx, databases, or home automation
- only escalate to GNU Radio / reverse-engineering tools if the target device is unsupported

## Starting from scratch by use case

### General listener / learner
1. Buy or attach a receive-only SDR
2. Start with SDR++
3. Verify tuning, waterfall, and gain behavior
4. Save exact sample rate / gain / antenna notes once you find good settings

### ADS-B station
1. Start with a single tuned decoder service
2. Validate local decode rate before adding feeders
3. Add tar1090 only after raw ingest is stable
4. Add history/export/metrics last

### Sensor / weather station
1. Start with rtl_433 in JSON mode
2. Confirm real devices decode cleanly
3. Forward to MQTT or file sink
4. Build automation/dashboard after decode stability is proven

### APRS / packet station
1. Confirm RF front-end and FM demod path
2. Feed Dire Wolf with known-good audio
3. Validate packet decode
4. Add igate, maps, dashboards, or message routing later

## APRS build notes (RSP1B / SDRplay on Unraid)

**The RSP1B problem:** `rtl_fm` cannot directly access the RSP1B when the SDRplay API service is running — the device is already claimed. The working path is:

```
SoapySDR (RSP1B) → Python FM demod → FIFO (named pipe) → direwolf → APRS packets
```

**Working container stack (Debian trixie base):**
- `rtl-sdr` package provides `rtl_fm` (not in all rtl_433 images — verify with `which rtl_fm`)
- `direwolf` is in Debian apt (`apt-get install direwolf`)
- `sox` for format conversion between stages
- `socat` if using UDP piping between stages

**Dire Wolf 1.7 config notes:**
- Audio device for FIFO input: `ADEVICE plug:file:/path/to/fifo` (NOT `ADEVICE -` which fails)
- PTT config requires RTS or DTR: `PTT NONE` works
- Invalid/unsupported commands in 1.7: `LOGKISS`, `BEACONING`
- `MYCALL` is valid; set to `NOCALL` for receive-only
- Running as root produces warnings but is not fatal

**Building from source (if Debian package is too old):**
```
apt-get install cmake libasound2-dev libssl-dev libudev-dev make gcc libc6-dev
git clone --depth 1 --branch 1.7 https://github.com/wb2osz/direwolf /tmp/direwolf
cd /tmp/direwolf && mkdir build && cd build && cmake .. && make -j && make install
```

**FM demod pipeline options:**
1. SoapySDR Python bindings → custom FM demod → sox → FIFO → direwolf (most flexible)
2. `rtl_fm` (if device accessible) → sox → FIFO → direwolf (simpler but RTL-only)
3. `rtl_fm` → UDP port → direwolf listening on that UDP (least reliable due to timing)

**Python SoapySDR bindings in Docker:** `pip3 install SoapySDR` may fail depending on base image. Alternative: bind-mount host's `libSoapySDR.so` and use the host Python with the bindings installed natively.
