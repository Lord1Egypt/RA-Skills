# Satellite / Weather SDR Projects

## Core references

### SatDump
- Repo: `SatDump/SatDump`
- Best current open-source reference for satellite pipelines, live record + offline processing, and pass-centric workflows
- Strong CLI + GUI + pipeline model
- Start here for NOAA / Meteor / HRPT / pass-based work
- Particularly strong because it supports:
  - live SDR ingest
  - offline file processing
  - named pipelines
  - both GUI and CLI workflows

### Ground Station
- Web-oriented satellite orchestration pattern
- Useful as a systems reference for pass scheduling, decoder orchestration, telemetry UI, and station control

## Starting from scratch

### If the user wants weather images fast
Recommend:
- `SatDump` first
- one known-good SDR
- one known-good antenna/feedline path
- one target mode (for example NOAA APT or Meteor) before chasing harder pipelines

### If the user wants a full satellite station
Recommend layers:
1. pass prediction / scheduling
2. live capture / recording
3. demod / decode pipeline
4. archive/gallery output
5. dashboard for pass history and station health

### If the user is experimenting rather than operating
Encourage:
- saving baseband during test passes
- documenting sample rate, center frequency, and gain for successful captures
- starting with a single satellite family before broadening scope

## OpenClaw shape
Prefer:
- scheduled capture/record jobs
- decoder/post-processing pipeline
- gallery/archive outputs
- pass log and station status in a dashboard layer
- optional alerts for upcoming passes, failed captures, or decode completion

## Important setup realities

- Satellite projects are often constrained by pass timing more than CPU alone
- A station can fail because of antenna placement, feedline loss, polarization mismatch, tracking, clocking, or simply picking the wrong target for the hardware
- Weather and satellite projects benefit from keeping raw/baseband for test runs so decode settings can be retried later

## Best-fit guidance

### If you want satellite operations
Use:
- `SatDump` first
- then add scheduling, gallery, archive, and dashboard behavior around it

### If you want a home-lab weather/satellite observatory
Prefer:
- one capture service per mode/family
- append-only pass outputs
- a pass archive with preview images / products
- operational dashboards above the capture jobs

## Operational checklist

Before declaring a satellite build healthy, verify:

1. the SDR can sustain the required sample rate
2. gain and center frequency are sane
3. pass timing/orbit source is correct
4. recorded baseband is non-empty and usable
5. decode output lands in an organized per-pass/per-satellite structure
6. the next pass can run unattended
