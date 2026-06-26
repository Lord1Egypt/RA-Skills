# SDR Architecture Patterns

## Contents
- 1. Design principles
- 2. Canonical SDR stack layers
- 3. Proven architecture patterns
- 4. Anti-patterns
- 5. Practical recommendations for home-lab SDR projects
- 6. Notes specific to SDRplay / SoapySDR style stacks

## 1. Design principles

### Separate radio work from product work
Treat these as different layers:
- **radio work**: tuning, sampling, demodulation, decoding
- **product work**: maps, dashboards, search, alerts, playback, auth, mobile UX

Good SDR projects usually keep those layers loosely coupled.

### Prefer mode-specific services
Do **not** build one giant app that tries to do:
- ADS-B
- NOAA
- rtl_433
- trunking
- APRS
- reverse engineering

all in the same DSP runtime.

Instead prefer:
- one service per mode or mission
- one UI that can aggregate them
- one shared metadata/event model where possible

### Make the UI consume stable outputs
The UI should ideally consume:
- JSON events
- image files
- audio clips
- metrics
- status endpoints

not raw SDR device state.

### Save IQ selectively
Do not record everything forever by default.
Good pattern:
- keep decoded events and summaries by default
- optionally save raw/IQ/baseband for:
  - debugging
  - unknown protocol work
  - significant satellite passes
  - manual operator-triggered captures

## 2. Canonical SDR stack layers

### Layer 1: hardware / drivers
Examples:
- RTL-SDR
- SDRplay
- Airspy
- HackRF
- BladeRF
- USRP

Related software:
- vendor libraries
- libusb / udev
- Soapy plugins
- gr-osmosdr drivers

### Layer 2: source / tuning
Examples:
- SoapySDR source
- RTL TCP source
- gr-osmosdr source
- SatDump source abstraction

### Layer 3: DSP / decode
Examples:
- rtl_433
- readsb / dump1090
- OP25
- trunk-recorder internals
- SatDump pipelines
- GNU Radio custom flowgraphs

### Layer 4: event / artifact outputs
Examples:
- JSON lines
- audio files per call
- image gallery outputs
- decoded packets
- time-series metrics
- geo events

### Layer 5: storage / distribution
Examples:
- filesystem watch folders
- SQLite / Postgres
- S3/object storage
- MQTT
- HTTP upload endpoints
- archive browser

### Layer 6: operator / product UI
Examples:
- map dashboards
- scanner playback apps
- browser receivers
- maintenance/admin panels

## 3. Proven architecture patterns

### Pattern A: recorder-first pipeline
Use when:
- trunked/public-safety calls
- you need archives and post-processing

Shape:
1. SDR ingest/recording service records discrete conversations
2. files + metadata land in watched storage
3. downstream UI or AI stack ingests completed calls

Examples:
- `trunk-recorder -> rdio-scanner`
- `trunk-recorder -> scanner-map`

Why it works:
- ingest is robust and separable
- downstream layers can be restarted/replaced independently

### Pattern B: browser receiver
Use when:
- user wants live tuning
- multiple people need access to one radio

Shape:
1. SDR source is owned by a web receiver server
2. server exposes spectrum/audio/control to browser clients
3. optional sidecar decoders run out-of-band

Examples:
- `openwebrx+`
- KiwiSDR style systems

Why it works:
- clean mental model
- great for operator interaction
- weak for event-centric workflows unless extended

### Pattern C: pass-based satellite pipeline
Use when:
- weather satellites
- orbital passes
- timed record + decode jobs

Shape:
1. scheduler determines pass windows
2. recorder captures only during pass
3. decoder/post-processor generates images/products
4. gallery/archive/UI presents products

Examples:
- `SatDump`
- Ground Station style orchestration

Why it works:
- respects the fact that satellite work is scheduled, not continuous

### Pattern D: decoder appliance + dashboard
Use when:
- home “radio observatory” with multiple modes
- mode switching on one SDR

Shape:
1. each mode has its own service container/runtime
2. only one hardware-owning mode runs at a time if sharing one SDR
3. shared dashboard reads status and outputs from all modes

Why it works:
- clean separation
- dashboard survives decoder churn
- easiest way to add features over time

### Pattern E: research bench
Use when:
- unknown protocols
- RF analysis and reverse engineering

Shape:
1. live exploration with `SDR++`, `GQRX`, or `SigDigger`
2. capture snippets/baseband
3. inspect offline in `inspectrum`
4. infer/replay/fuzz in `URH`
5. graduate to a custom decoder or `rtl_433` contribution if needed

Why it works:
- avoids prematurely automating unknowns

## 4. Anti-patterns

### Giant all-in-one app
Trying to do every mode in one process leads to:
- hardware lock contention
- impossible debugging
- ugly UI compromises
- fragile state machines

### UI tightly coupled to decoder internals
If the frontend expects exact live DSP semantics, every decoder change breaks the UI.

### Vendor library soup inside random containers
SDRplay / HackRF / Soapy stacks often fail because of:
- wrong library versions
- plugin ABI mismatch
- missing daemon/service layer
- missing `/dev/shm`
- USB permissions

### Treating “can open device once” as solved
A manual probe is not the same as a stable long-running ingest service.

## 5. Practical recommendations for home-lab SDR projects

### Best overall shape for a home radio observatory
- host machine physically attached to SDR handles hardware-specific ingest
- one service per mode:
  - ADS-B
  - rtl_433 / sensors
  - NOAA / satellite recorder
  - optional browser receiver
- one lightweight dashboard/UI aggregates state and outputs
- decoded outputs stored under a single project root
- add search/alerts only after ingest is stable

### Good project root layout
```text
radio-observatory/
  adsb/
    events/
    globe_history/
    graphs/
  ism433/
    events/
    captures/
  noaa/
    passes/
    raw/
    gallery/
  dashboard/
  status.json
  docker-compose.yml
```

### Implementation order
1. make one ingest mode reliable
2. make its outputs observable
3. build minimal UI around outputs
4. add second mode
5. only then add AI, maps, summaries, mobile polish

### Good “v1” outputs per mode
- ADS-B: aircraft JSON, map, graphs
- rtl_433: JSONL event stream + recent event panel
- NOAA: image gallery + pass log
- trunking: call files + metadata + listener UI

## 6. Notes specific to SDRplay / SoapySDR style stacks

### Common failure points
- Soapy runtime version does not match plugin version
- plugin exists but expected soname symlink is missing
- `sdrplay_apiService` not running or not reachable
- container missing `/dev/shm`
- USB cgroup permissions not granted
- app linked against one `libSoapySDR`, plugin built for another
- host and container each carry different SDRplay library worlds

### Safe mental model
For SDRplay + containers, assume you need to verify all of these explicitly:
1. device visible on host via USB
2. correct vendor API library present
3. correct Soapy plugin present
4. plugin ABI matches the loaded `libSoapySDR`
5. service/daemon layer alive if required
6. app can run continuously, not just probe once

### For fragile vendor stacks
Prefer one of these:
- native install on the SDR-attached host
- a purpose-built container image you own
- a bundle with pinned libraries and explicit runtime paths

Do **not** assume a generic SDR container will behave correctly with SDRplay just because `SoapySDRUtil --find` works once.

### What “done” looks like
A decoder is only “done” when:
- it survives restarts
- it runs for meaningful time without stalling
- it writes real events/artifacts
- it recovers from temporary RF or service glitches
- the UI sees useful outputs
