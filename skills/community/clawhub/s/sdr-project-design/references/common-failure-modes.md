# Common Failure Modes in SDR Projects

## Driver / hardware stack

### SoapySDR plugin/runtime mismatch
Symptoms:
- plugin visible but not usable
- decoder starts then stalls
- ABI/version errors

Check:
- exact `libSoapySDR` version
- plugin build target vs runtime target
- duplicate libraries on host/container

### Vendor daemon/service requirements
Symptoms:
- device probes once but long-running decoder dies
- service not responding
- intermittent read failures

Check:
- whether a vendor helper service must be running
- shared memory requirements (`/dev/shm`)
- startup ordering

### USB permissions / device access
Symptoms:
- works as root, fails in service/container
- permission denied or open failures

Check:
- udev rules
- libusb access
- device cgroup rules
- container mounts for `/dev/bus/usb`

### Device contention
Symptoms:
- one decoder works only when another is stopped
- random startup failures

Check:
- only one process owns the SDR at a time unless explicitly supported
- browser receiver / decoder / diagnostic tools are not competing for the same device

### SDRplay API service ownership
Symptoms:
- `rtl_fm -d driver=sdrplay` returns "No supported devices found"
- RSP1B visible to `rtl_test` but not to rtl_fm
- Device works with readsb/dump1090 but not rtl_fm

Root cause: SDRplay devices require the `sdrplay_apiService` daemon to be running. When this service owns the device, direct RTL-SDR style access (rtl_fm, rtl_test) fails even though SoapySDR can still reach the device.

Fix:
- The RSP1B via SoapySDR works even when `rtl_fm` doesn't — use SoapySDR as the access layer
- SoapySDR Python bindings + FM demod script → FIFO → direwolf is the working APRS path
- Do NOT use `rtl_fm` with SDRplay devices; use SoapySDR instead

### Container Docker image caching issues
Symptoms:
- `docker compose up --build` rebuilds but old image is still used
- Changes to Dockerfile not taking effect
- Container keeps running with old config

Root cause: Docker Compose caches the image layer even when `--build` is specified, unless `--no-cache` is passed. Also, if an old image has the same tag, Compose may reuse it.

Fix:
- `docker compose build --pull --no-cache` to force full rebuild
- `docker rmi <image>` to remove old image before rebuild
- Check `docker images | grep <name>` to verify correct image SHA is in use
- Restart container after rebuild: `docker compose down && docker compose up -d`

## Service design

### Manual probe works, service does not
Symptoms:
- ad hoc command succeeds
- systemd/containerized service flaps or stalls

Check:
- environment variables
- library paths
- entrypoint differences
- missing volumes, sockets, or shm mounts
- startup timing and retry behavior

### UI built before ingest is stable
Symptoms:
- pretty dashboard with unreliable/no data
- frequent rewrites because outputs keep changing

Fix:
- lock down outputs first
- make the UI consume stable files/JSON/metrics

### Monolith trying to do every mode
Symptoms:
- fragile state machines
- impossible debugging
- hard hardware switching bugs

Fix:
- split by mode
- one service per mission
- shared dashboard above them

## OpenClaw-specific

### Wrong placement of workload
Symptoms:
- hardware-heavy work pushed to the wrong machine
- poor USB behavior through indirection

Fix:
- keep fragile hardware stacks on the SDR-attached host or node
- keep dashboards and orchestration separate

### Overusing containers for vendor stacks
Symptoms:
- endless runtime/library weirdness

Fix:
- prefer native host install or a purpose-built pinned image when vendor stacks are fragile

## Operational caution

Keep a short caution in mind for projects that touch:
- public-safety systems
- digital voice decoding
- APRS/ham transmit paths
- shared/public audio publishing

Advise users to check local laws, licensing, service terms, and band-specific rules where relevant.
