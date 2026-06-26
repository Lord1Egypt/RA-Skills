# SDR Project Intake

Use this checklist before recommending an OpenClaw build path.

## Core questions

1. **What is the mission?**
- scanner / dispatch
- browser receiver
- satellite / weather
- ADS-B / aircraft
- APRS / packet
- ISM / sensors
- reverse engineering / unknown RF
- mixed observatory

2. **What hardware is involved?**
- SDR model(s)
- how many receivers
- where the SDR is physically plugged in
- host OS / node OS
- vendor-driver-heavy hardware or simple dongle

3. **How should the system behave?**
- live tuning by a human
- continuous event ingest
- scheduled pass capture
- archive and playback
- map / dashboard / alerts
- local-only vs shared/public access

4. **How many radios or modes must run at once?**
- one SDR / one mode at a time
- one SDR with switching
- multiple SDRs with dedicated roles

5. **What outputs matter most?**
- JSON events
- audio clips
- images/gallery
- waterfall/browser UI
- metrics/history
- searchable archive

6. **What are the operator expectations?**
- polished web app
- simple dashboard
- CLI/admin only
- mobile-friendly
- multi-user browser access

7. **What constraints matter?**
- CPU/GPU limits
- storage limits / retention expectations
- network/public exposure
- legal/compliance sensitivity
- how much fragility is acceptable in the hardware stack

## Minimum output after intake

After intake, the skill should be able to answer:
- dominant project family
- best upstream inspiration
- best OpenClaw shape
- what runs on host vs node
- what to build first
- biggest technical risks
