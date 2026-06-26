# SDR Research Deep Dive

Use this file when the user wants broad SDR research, starting guidance, project ideas, or setup strategy from scratch.

## 1. What SDR is good for

Software-defined radio replaces dedicated radio hardware functions with software DSP blocks. In practice, SDR projects usually split into a few big families:

- **Live listening / tuning**: tune AM/FM/SSB/CW and explore signals in real time
- **Protocol decoding**: decode known things such as ADS-B, APRS, AIS, pager, weather satellites, trunked radio, ISM sensors
- **Reverse engineering**: inspect unknown bursts, measure modulation, symbol timing, packet framing, and replay/synthesize controlled signals where lawful
- **Persistent observability**: run always-on ingest, collect decoded events, build dashboards, search, maps, and alerts
- **Capture and offline analysis**: store IQ/baseband for later replay, demod, classification, and debugging

## 2. Core hardware tiers

### Cheap entry tier

- **RTL-SDR v3/v4 class dongles**
- Best for: ADS-B, AIS, rtl_433, pager, NOAA APT, FM/AM listening, simple narrowband tasks
- Why they matter: absurdly cheap, huge ecosystem, easiest way to get started
- Limits: 8-bit ADC, no full duplex, limited dynamic range, not ideal for wideband/high-performance work

### Mid-tier hobby / lab

- **Airspy Mini / Airspy R2 / Airspy HF+**
- **SDRplay RSP family**
- **HackRF One**
- Best for: better dynamic range, broader tuning, general experimentation, some transmit-capable work with HackRF
- Limits: device-specific driver quirks; HackRF is versatile but not the best RX-only performer

### Higher-end / semi-pro / lab

- **USRP (Ettus) family**
- **LimeSDR**
- **BladeRF**
- Best for: custom PHYs, GNU Radio work, serious duplex experiments, research
- Limits: cost, driver complexity, clocking/synchronization considerations

## 3. Driver stack reality

Most SDR pain is not the app. It is the stack below it:

- USB stability
- kernel modules grabbing the wrong device
- vendor runtime mismatches
- SoapySDR plugin mismatch
- container passthrough pain
- sample-rate / bandwidth / gain settings that are technically valid but operationally bad

### Important abstractions

- **rtl-sdr / librtlsdr**: baseline stack for RTL2832U dongles
- **SoapySDR**: hardware abstraction layer; great for swapping backends, but fragile if versions/plugins drift
- **gr-osmosdr**: common GNU Radio source/sink bridge for SDRs
- **vendor SDKs**: SDRplay API, UHD for USRP, HackRF tools/libhackrf, LimeSuite, BladeRF CLI/lib

## 4. Best-known open source SDR project families

### General live receiver software

#### SDR++

- Cross-platform, modern, fast, lightweight desktop receiver
- Strong first recommendation for general-purpose listening and exploration
- Good when the user wants "something that works now" without building a large stack

#### GQRX

- Mature desktop SDR UI built around GNU Radio / gr-osmosdr
- Good for Linux/macOS users who want a stable traditional receiver workflow
- Not the prettiest, but dependable

#### CubicSDR / SDRangel

- Worth knowing, but usually not the first recommendation unless the user specifically likes their workflow or needs SDRangel’s broader plugin-style feature set

### Browser / remote receiver

#### openwebrx+

- Preferred web receiver reference for OpenClaw-style remote/browser use
- Multi-user web interface
- Supports many demodulators and multiple SDR devices
- Strong fit for "radio observatory" / remote tuning / shared receiver deployments

Why it matters:
- browser-first operator UX
- multi-user access
- easier sharing than desktop apps

### Trunked / public-safety scanner stack

#### Trunk Recorder

- Records calls from trunked and conventional radio systems
- Uses SDRs plus GNU Radio and OP25-derived functionality for P25-heavy workflows
- Great ingest/recording core for headless systems
- Often paired with downstream UIs like OpenMHz, Trunk Player, or Rdio-Scanner

#### SDRTrunk

- Java desktop app popular for trunking setups
- Strong all-in-one operator experience for some users
- Better when a user wants one workstation app rather than decomposed services

#### Rdio-Scanner / scanner-map

- UX and data product layer on top of ingest/recorders
- Best when the user wants searchable audio, talkgroups, map/location intelligence, and a polished scanner experience

### Utility / observability protocols

#### rtl_433

- Generic data receiver for 315/345/433/868/915 MHz class ISM devices
- Excellent for weather sensors, tire pressure sensors, utility meters, environmental sensors, and assorted consumer devices
- One of the highest-ROI SDR tools because it quickly turns RF into useful JSON/events

Key strengths:
- low resource usage
- huge device decoder library
- JSON/CSV/MQTT/Influx/syslog outputs
- runs well on low-power hardware

#### readsb / dump1090 + tar1090

- Default ADS-B aircraft observability stack
- readsb/dump1090 for decoding, tar1090 for map/UI
- Fastest path to a useful aircraft station

#### Dire Wolf

- Practical default for APRS / packet radio / igate style builds
- Excellent glue tool when audio/baseband is already available
- With non-RTL hardware, often paired via SoapySDR + FM demod pipeline instead of rtl_fm

#### rtlamr

- Utility meter decoding (where legal and relevant)
- Pairs well with MQTT / databases / dashboards

### Satellite / weather

#### SatDump

- One of the strongest all-around satellite processing tools right now
- Supports live SDR input and offline pipelines
- Good for weather sats, LRPT/HRPT/AHRPT, and many satellite workflows
- Usually the best first answer for people who want to get satellite images/data rather than build DSP from scratch

#### Other recurring tools

- WXtoImg lineage / NOAA APT style tools
- predict / gpredict for pass planning
- rotctl / rigctl ecosystems for rotators/radios where needed

### Reverse engineering / unknown signal work

#### URH (Universal Radio Hacker)

- Great for unknown digital signal analysis, protocol inference, and replay-oriented lab work
- Strong UI for framing and modulation exploration

#### inspectrum

- Excellent for offline spectral/time-domain visual inspection of captured signals
- Very good companion tool when URH or GNU Radio alone feels too heavy

#### SigDigger

- Useful explorer/analysis tool for signals and spectrum

#### GNU Radio

- The toolkit for custom DSP, custom receivers, experiments, and bespoke pipelines
- Best when off-the-shelf decoders are not enough
- Not the first thing to recommend to everyone because it has the steepest learning/setup cost

## 5. How to start from scratch

If a user says "I want to get into SDR" and gives no other detail, use this progression:

### Step 1: pick the mission

Ask what they actually want to do first:

- listen/tune around?
- track aircraft?
- decode weather sensors?
- build a police/fire scanner?
- receive satellites?
- reverse engineer remotes/sensors?

Mission matters more than hardware brand at the beginning.

### Step 2: pick the cheapest hardware that clears the mission

Default beginner picks:

- **RTL-SDR** for most receive-only beginner projects
- **Airspy HF+** or **SDRplay** when better RX matters
- **HackRF** only if they truly need transmit-ish experimentation / wider hacking flexibility

### Step 3: pick one software stack, not many

Examples:

- aircraft → readsb + tar1090
- ISM/weather sensors → rtl_433
- remote browser receiver → openwebrx+
- trunked scanner → trunk-recorder or SDRTrunk
- satellite imagery → SatDump
- unknown digital protocols → URH + inspectrum
- general listening → SDR++

### Step 4: validate the signal chain before scaling up

Always verify in this order:

1. hardware enumerates
2. driver can open it
3. sample stream exists
4. gain/frequency/sample rate are sane
5. only then add decoding/storage/UI

### Step 5: decide live-only vs observability

If the user wants repeatable value, steer toward observability:

- headless ingest service
- structured outputs (JSON/MQTT/files)
- dashboard/search/history above it

## 6. Common setup patterns by project type

### Beginner listening station

- Hardware: RTL-SDR / SDRplay / Airspy
- Software: SDR++ or GQRX
- Goal: tune, learn modulation types, hear immediate results

### Home RF observatory

- Hardware host owns SDRs
- mode-specific services: readsb, rtl_433, APRS pipeline, trunk-recorder, etc.
- outputs to files/MQTT/DB
- web dashboards on top

### Public-safety archive/search box

- SDR ingest + trunk-recorder
- searchable playback/UI via Rdio-Scanner or OpenMHz-style tooling
- optional maps/geocoding/statistics layer

### Weather/sensor telemetry box

- rtl_433 output to MQTT / Influx / Home Assistant
- dashboard and automation consume decoded events

### Satellite imaging station

- SatDump for pass capture and decode
- optional scheduler/orbit tools for automation
- archive outputs by pass/satellite

### RF reverse-engineering bench

- SDR source + GNU Radio/URH/inspectrum/SigDigger
- save IQ often
- document sample rates, center frequencies, modulation observations, and discovered framing

## 7. What to capture in setup documentation

When preparing a real SDR build plan, include:

- hardware model and antenna
- operating system / host type
- driver/runtime dependency chain
- known-good sample rate(s)
- center frequencies / bands of interest
- gain strategy
- whether the workflow is live, scheduled, or always-on
- output format and retention plan
- how health/status is checked
- what breaks first

## 8. Good publishing-quality heuristics for the skill

The skill should help another agent:

- choose a project family quickly
- recommend one good default stack
- avoid wasting time on the wrong hardware/software combo
- know which tools are battle-tested
- know when to use desktop app vs headless service vs web receiver
- know when GNU Radio is justified and when it is overkill

## 9. Strong default recommendations

If the user is undecided, these are good defaults:

- **General receive / learning** → SDR++
- **Remote browser receiver** → openwebrx+
- **Aircraft** → readsb + tar1090
- **433/868/915 sensors** → rtl_433
- **APRS / packet** → Dire Wolf
- **Trunked radio ingest** → trunk-recorder
- **Satellite data** → SatDump
- **Unknown digital signals** → URH + inspectrum + GNU Radio as needed
- **Hardware abstraction goal** → SoapySDR, but warn about version/plugin mismatch
