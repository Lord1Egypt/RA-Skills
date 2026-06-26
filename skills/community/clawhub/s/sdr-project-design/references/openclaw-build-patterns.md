# OpenClaw Build Patterns for SDR Projects

## Contents
- 1. Core OpenClaw mapping
- 2. Where things should run
- 3. Good project shapes
- 4. Build-order guidance
- 5. Common OpenClaw mistakes

## 1. Core OpenClaw mapping

When turning an SDR idea into an OpenClaw project, map it like this:

- **Hardware owner**
  - the host or paired node physically attached to the SDR
  - owns drivers, vendor libraries, USB access, and fragile radio runtime details

- **Mode services / runtimes**
  - one runtime per mission: ADS-B, rtl_433, NOAA, trunking, APRS, browser receiver, etc.
  - may be containerized or native depending on platform and driver fragility
  - write outputs to stable files, JSON, audio clips, images, or metrics

- **Shared project state**
  - status file
  - event directories
  - recent outputs
  - configuration

- **UI / automation layer**
  - dashboard
  - browser UI
  - notifications
  - summaries
  - search / filtering / map views

## 2. Where things should run

### Host attached to SDR
Prefer this for:
- SDRplay
- vendor-library-heavy stacks
- fragile USB or daemon/service dependencies
- first bring-up of new hardware

### Paired OpenClaw node
Prefer this for:
- remote SDR hardware in another room or machine
- GPU-heavy side work
- dedicated radio boxes
- keeping the main host lighter

### Dashboard/UI on the main OpenClaw host
Prefer this when:
- multiple mode services feed one UX
- the hardware layer is messy and should stay isolated
- the user wants one place to control and inspect everything

## 3. Good project shapes

### Shape A — single-SDR mode-switching observatory
Use when one SDR must serve many jobs.

Pattern:
- one hardware-attached host
- one service per mode
- only one hardware-owning mode active at a time
- dashboard controls mode and reads outputs

### Shape B — dedicated-receiver observatory
Use when multiple SDRs exist.

Pattern:
- dedicate a receiver per mission where possible
- avoid unnecessary switching logic
- aggregate outputs in one dashboard/UI

### Shape C — ingest + product split
Use when the user wants a polished app inspired by scanner-map / rdio-scanner / openwebrx+.

Pattern:
- upstream-style ingest service(s)
- OpenClaw-built dashboard/product layer
- optional integrations, summaries, alerts, maps

## 4. Build-order guidance

For almost any SDR project in OpenClaw:
1. prove hardware access
2. prove one decoder/ingest path
3. prove stable outputs
4. build minimal UI/status around those outputs
5. only then add switching, maps, AI, or mobile polish

If the project involves a browser-style UX:
- do not start from the frontend
- prove data and artifacts first
- then wrap it

## 5. Common OpenClaw mistakes

### Putting all SDR logic in the dashboard
Bad idea. Keep hardware-specific logic out of the UI.

### Building a pretty shell before proving ingest
This creates demo-ware with no stable signal path underneath.

### Assuming containerization is always easier
For SDRplay/vendor stacks, native host install or a purpose-built pinned container is often safer.

### Treating every project like a browser receiver
Some projects are actually:
- recorder-first
- pass-scheduled
- packet/event-first
- reverse-engineering benches

The UI should match the mission.
