# SDR Hardware & Driver Integration Reference

How the major SDR hardware families connect to software — driver models, access layers, common integration patterns, and known issues.

---

## Universal abstraction: SoapySDR

**SoapySDR** (`soapysdr.org`) is the closest thing to a universal SDR driver API. It provides:
- a single `SoapySDR::Device` interface across all supported hardware
- device enumeration via `SoapySDR::Device.enumerate()`
- consistent stream read/write API (`SOAPY_SDR_CF32` complex float samples most common)
- plugin architecture so each hardware family ships as a loadable module

**When to use it:**
- when you want one code path to work across multiple SDR types
- when the hardware vendor provides a SoapySDR plugin
- as the integration target in Python or any language with SoapySDR bindings

**When NOT to use it:**
- when the upstream tool has its own native driver (e.g., `readsb` for RTL-SDR on ADS-B)
- when the native driver is significantly more performant or feature-complete

**SoapySDR plugin location:** determined by `SOAPY_SDR_PLUGIN_PATH` environment variable. Must match the ABI version the library was built against (`0.8-3` is common).

---

## RTL-SDR (RTL2832U chipset)

### Hardware
- USB TV tuner dongles based on RTL2832U + R820T/2/3 tuner
- Very cheap (~$20), popular for ISM, ADS-B, generalHF
- No transmit capability

### Driver options

**Option A — libusb direct (native)**
```
rtl_sdr, rtl_tcp, rtl_433, rtl_fm
```
These tools use `librtlsdr` which talks to the device over libusb-1.0 directly. No extra daemon needed. Requires write access to `/dev/bus/usb/XXX`.

**Option B — RTL-SDR SoapySDR plugin**
```
SoapySDR → SoapySDRPlay → RTL2832U
```
Available but rarely needed since native tools work fine.

### Docker/container integration
```
device_cgroup_rules:
  - 'c 189:* rwm'    # USB access for libusb
volumes:
  - /dev/bus/usb:/dev/bus/usb
```

**udev rule for non-root access:**
```
SUBSYSTEM=="usb", ATTR{idVendor}=="0bda", ATTR{idProduct}=="2832", MODE="0666"
```
Replace `0bda:2832` with actual vendor:product from `lsusb`.

### Common tools
- `rtl_433` — ISM band decoder
- `rtl_fm` — general FM demod
- `readsb` / `dump1090` — ADS-B (these have their own RTL-SDR driver, don't need rtl_fm)
- `rtl_tcp` — network streaming server

### Known issues
- Sample rate jitter on cheap dongles
- Frequency offset (use `-p ppm` to correct)
- No direct sampling / HF support on most models (some E4000 tuners do HF directly)

---

## SDRplay (RSP1A, RSP1B, RSP2)

### Hardware
- Software-defined radio with full 0-2 GHz coverage
- Requires external enclosure/antenna (not plug-and-play like RTL-SDR)
- Single device can be shared between apps via the API service

### Driver model

**The SDRplay API service is required.** The device cannot be accessed directly like RTL-SDR.

```
sdrplay_apiService (host daemon, runs as service)
  └── RSP1B via USB
        └── SoapySDRPlay (SoapySDR plugin) → any SoapySDR app
        └── readsb --dev-sdrplay, dump1090 --dev-sdrplay (native SDRplay path)
```

### Starting the service
```bash
# On host (must be running before any SDRplay app)
/usr/local/bin/sdrplay_apiService
# Or via s6 supervision: s6-svc -u /run/service/sdrplay
```

### Integration patterns

**Pattern 1 — Native SDRplay tools (no SoapySDR)**
```
readsb --dev-sdrplay --net ...
dump1090 --dev-sdrplay --net ...
```
These use the SDRplay API directly. No SoapySDR involved.

**Pattern 2 — SoapySDR apps via SoapySDRPlay**
```
SOAPY_SDR_PLUGIN_PATH=/usr/local/lib/SoapySDR/modules0.8-3
LD_LIBRARY_PATH=/usr/local/lib
# then any SoapySDR-compatible app
```

**Pattern 3 — Python SoapySDR bindings**
```python
import SoapySDR
from SoapySDR import SOAPY_SDR_CF32
sdr = SoapySDR.Device()  # finds first SDRplay
rx = sdr.setupStream(SOAPY_SDR_CF32, "RX")
sdr.activateStream(rx)
# read samples...
```

### SoapySDRPlay ABI
- Built against SoapySDR ABI `0.8-3`
- The `.so` file must be in `SOAPY_SDR_PLUGIN_PATH`
- Host bind-mount `/usr/local/lib/SoapySDR/modules0.8-3` into container
- Also bind-mount the `.so` library itself if needed

### Container Docker integration
```yaml
environment:
  - SOAPY_SDR_PLUGIN_PATH=/usr/local/lib/SoapySDR/modules0.8-3
  - LD_LIBRARY_PATH=/usr/local/lib
volumes:
  - /usr/local/lib:/usr/local/lib:ro
  - /usr/local/lib/libSoapySDR.so.0.8-3:/usr/lib/x86_64-linux-gnu/libSoapySDR.so.0.8:ro
  - /usr/local/bin/sdrplay_apiService:/opt/hostbin/sdrplay_apiService:ro
command:
  - /opt/hostbin/sdrplay_apiService &
  - sleep 3
  # then run your app
```

### Critical: rtl_fm does NOT work with SDRplay
```
rtl_fm -d driver=sdrplay  # → "No supported devices found"
```
Even though the device is accessible via SoapySDR. The `rtl_fm` RTL-SDR path cannot share the device with the running API service. **Always use SoapySDR for SDRplay access in custom pipelines.**

### SDRplay API service and device sharing
The `sdrplay_apiService` must be running before any app tries to access the RSP1B. The service can be started once at host boot and left running — it manages the USB device and handles multiple client connections.

### Proven SoapySDR audio-capture pattern (RSP1B)
Use this sequence for reliable FM/NFM audio extraction:
1. `SoapySDRDevice_makeStrArgs("driver=sdrplay")`
2. `setSampleRate(RX, ch0, 960000)` (or another rate that cleanly decimates to audio)
3. `setFrequency(RX, ch0, freq_hz)`
4. `setupStream(RX, "CF32")` + `activateStream()`
5. `readStream()` loop into complex float I/Q
6. FM discriminator (`atan2` phase-difference)
7. Decimate to fixed audio rate (prefer exact integer ratio)
8. De-emphasis + low-pass for voice-band monitoring
9. Normalize and write 16-bit PCM/WAV

Recommended defaults for NOAA/NFM voice sanity captures:
- `sdr_rate=960000`, `audio_rate=48000`, `decim=20`
- use de-emphasis (75 µs) and ~3 kHz low-pass
- keep one SDR owner process at a time (maintenance-mode captures)

### Known failure signatures (important)
- `makeStrArgs failed` usually means plugin/runtime visibility mismatch or device/session contention.
- `undefined symbol: SoapySDRDevice_getError` indicates Soapy ABI mismatch between library and plugin/build.
- “2x duration” WAV files usually indicate wrong sample-rate labeling vs effective decimated sample count.
- Choosing channel by raw RF power can pick noise; score by demodulated voice-band quality instead.

### Known issues
- API service must be on same host as USB connection (no network access to the device itself)
- SoapySDRPlay and native SDRplay tools can coexist if both use the same API service
- RSP1B is 12-bit ADC, better dynamic range than RTL-SDR

---

## HackRF One

### Hardware
- USB 2.0 (limited by bus speed)
- 1 MHz to 6 GHz coverage, receive and transmit
- Popular for reverse engineering, ham radio, general exploration

### Driver options

**Option A — libhackrf (native)**
```
hackrf_transfer, hackrf_sweep
```

**Option B — SoapySDR HackRF plugin**
```
SoapySDR → SoapyHackRF
```
SoapySDR is the normal way HackRF gets used in custom pipelines.

### Integration
```bash
apt-get install libhackrf-dev hackrf
hackrf_transfer -r filename.cf32 -f 144390000 -g 40 -l 40 -s 2000000
```

### Docker/container
```yaml
device_cgroup_rules:
  - 'c 189:* rwm'
volumes:
  - /dev/bus/usb:/dev/bus/usb
```

---

## BladeRF 2.0 (xA4, xA9, Micro)

### Hardware
- USB 3.0, high bandwidth
- 47 MHz to 6 GHz, transmit + receive
- FPGA-based — can run custom firmware
- More powerful than HackRF but also more expensive

### Driver model
- `libbladeRF` — C API, primary driver
- `SoapySDR` plugin available but often native libbladeRF tools are preferred

### Integration
```bash
apt-get install libbladeRF-dev bladeRF-cli
bladeRF-cli -d "*:serial=xxxxx" -f rx样本.cf32
```

### Container integration
Similar USB passthrough as other USB SDRs.

---

## USRP (Ettus Research / NI)

### Hardware
- High-end SDR, Ethernet or USB 3.0
- UHD driver stack (`libuhd`)
- Requires Ettus firmware images
- Most powerful consumer SDR available

### Driver model
- `libuhd` (UHD) — the vendor driver stack
- `SoapyUHD` plugin for SoapySDR compatibility
- Most SDR apps that support USRP use SoapySDR → SoapyUHD

### Integration
```python
import uhd
usrp = uhd.usrp.MultiUSRP()
```

### Common issues
- Requires firmware upload on first use (`usrp_find_devices`, `uhd_image_loader`)
- Ethernet models require specific network config (MTU 9000 often needed)
- Not typically containerized — usually runs directly on Linux

---

## SoapySDR Python Bindings

### Installation
```bash
pip install SoapySDR          # may fail in minimal Docker images
apt-get install python3-soapysdr  # Debian/Ubuntu package
```

### Basic usage
```python
import SoapySDR
from SoapySDR import SOAPY_SDR_CF32

# Enumerate devices
results = SoapySDR.Device.enumerate({})
print(results)

# Connect to first device
sdr = SoapySDR.Device(results[0])

# Configure
sdr.setSampleRate(0, 2e6)
sdr.setFrequency(0, "RF", 144.39e6)
sdr.setGain(0, "AMP", 0)
sdr.setGain(0, "LNA", 40)

# Stream
rx = sdr.setupStream(SOAPY_SDR_CF32, "RX")
sdr.activateStream(rx)

buf = bytearray(4096 * 8)  # 4096 complex float32 samples
sr = sdr.readStream(rx, [buf], len(buf) // 8)
print(f"Read {sr.ret} samples")
```

### In containers
If `SoapySDR` pip install fails in a minimal image, either:
1. Install the system package (`python3-soapysdr`)
2. Bind-mount the host's working Python environment
3. Use a full Debian base image instead of alpine/slim

---

## Driver layer decision guide

| Hardware | Best access path | SoapySDR? | Special requirement |
|---|---|---|---|
| RTL-SDR (generic) | `librtlsdr` via rtl_433, readsb, rtl_fm | via plugin, rarely needed | USB passthrough, cgroup rules |
| SDRplay RSP1B | SoapySDR via SoapySDRPlay, or native SDRplay API | Yes, required | `sdrplay_apiService` must run |
| HackRF One | libhackrf or SoapySDR | Yes | USB 2.0, less bandwidth |
| BladeRF 2.0 | libbladeRF native usually preferred | Available | USB 3.0 |
| USRP (Ettus) | libuhd or SoapyUHD | Yes | firmware upload, Ethernet for USRP-X series |
| Airspy | libairspy or SoapySDR | via plugin | USB 3.0 recommended |

---

## USB device passthrough for containers

### cgroup rules (Docker)
```yaml
device_cgroup_rules:
  - 'c 189:* rwm'   # all USB devices — works for most SDRs
```

### Specific device (more secure)
```yaml
device_cgroup_rules:
  - 'c 189:003 rwm'   # only this specific USB bus:device
```
Get the numbers from `ls -la /dev/bus/usb/` inside the container.

### udev rules (host Linux, for non-root access)
```
# /etc/udev/rules.d/99-sdr.rules
# RTL-SDR
SUBSYSTEM=="usb", ATTR{idVendor}=="0bda", ATTR{idProduct}=="2832", MODE="0666", GROUP="plugdev"
# SDRplay
SUBSYSTEM=="usb", ATTR{idVendor}=="1df7", ATTR{idProduct}=="3050", MODE="0666", GROUP="plugdev"
# HackRF
SUBSYSTEM=="usb", ATTR{idVendor}=="1d50", ATTR{idProduct}=="6089", MODE="0666", GROUP="plugdev"
```
Reload with: `sudo udevadm control --reload-rules && sudo udevadm trigger`

### /dev/bus/usb bind mount (most reliable)
```yaml
volumes:
  - /dev/bus/usb:/dev/bus/usb
```
Binds the entire USB bus tree. Works for any USB SDR without cgroup rules.

---

## Multi-device and device sharing

### Only one process owns the SDR at a time
Unless the driver explicitly supports sharing (some SoapySDR devices do, RTL-SDR via rtl_tcp can be shared over network), only one process can hold the device handle.

**Design pattern:**
- one hardware-owning service per mode
- dashboard switches modes by stopping one container and starting another
- RSP1B via sdrplay_apiService can accept multiple client connections simultaneously — it handles the multiplexing internally

### Network streaming as a sharing workaround
For RTL-SDR: run `rtl_tcp` on the host, then connect multiple clients over the network.
```
rtl_tcp -a 0.0.0.0 -p 1234
# clients connect over LAN
```
Downside: network latency affects time-sensitive applications (ADS-B still works fine, spectrum analysis less so).

### SoapySDR as a network-transparent layer
`SoapyRemote` allows a SoapySDR client to talk to a SoapySDR server over the network, effectively streaming samples from a remote SDR.
```
# Server (on host with SDR)
SoapySDRServer --bind
# Client (anywhere on LAN)
SoapySDRDevice("soapysdr://192.168.1.x:5000")
```
Useful for separating the SDR host from the processing host.
