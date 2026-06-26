# Example SDR Builds in OpenClaw

## Example 1 — Home radio observatory

### Goal
One place for ADS-B, rtl_433, NOAA, APRS, and optional browser tuning.

### Upstream inspirations
- `readsb` + `tar1090`
- `rtl_433`
- `SatDump`
- `Dire Wolf`
- `openwebrx+`

### OpenClaw shape
- SDR-attached host owns hardware
- one service per mode
- dashboard aggregates outputs and controls mode if needed

### Build order
1. prove one mode (usually ADS-B)
2. add event/image outputs for other modes
3. add dashboard
4. add switching only if one SDR must serve many modes

## Example 2 — Scanner intelligence stack

### Goal
Capture calls, browse them, map them, summarize them.

### Upstream inspirations
- `trunk-recorder` or `sdrtrunk`
- `rdio-scanner`
- `scanner-map`

### OpenClaw shape
- ingest on SDR-attached host
- playback/archive layer above ingest
- map/intelligence layer above that

### Build order
1. prove ingest and metadata
2. prove playback UX
3. add map/intelligence
4. add alerts/integrations

## Example 3 — Browser receiver station

### Goal
Remote tune-anything SDR accessible in browser.

### Upstream inspirations
- `openwebrx+`

### OpenClaw shape
- browser receiver as operator-facing service
- optional sidecar decoders for specialized modes
- keep archive/event logic separate if needed

### Build order
1. prove SDR access and browser receiver
2. tune UX and persistence
3. add sidecar decoders only where needed

## Example 4 — Satellite / NOAA station

### Goal
Capture scheduled passes and turn them into artifacts people can browse.

### Upstream inspirations
- `SatDump`
- Ground Station style orchestration

### OpenClaw shape
- scheduled recorder/decoder jobs
- pass log + gallery outputs
- dashboard for pass state and recent products

### Build order
1. prove pass timing
2. prove decode quality
3. add gallery/archive
4. add scheduling polish and notifications
