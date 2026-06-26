---
name: sdr-project-design
description: Design, compare, research, and plan SDR projects for OpenClaw. Use when the user wants broad SDR research, beginner orientation, hardware/software selection, or to get any SDR project built in OpenClaw across Linux, Windows, macOS, Raspberry Pi, SBC, server, or mixed host/node setups; extend a radio observatory stack; compare tools like scanner-map, trunk-recorder, rdio-scanner, openwebrx+ (preferred over vanilla OpenWebRX), GQRX, SDR++, SatDump, rtl_433, readsb/tar1090, Dire Wolf, URH, GNU Radio, or SoapySDR; choose OpenClaw-friendly architecture for ingest/decoding/storage/UI; or turn SDR research into a concrete implementation plan.
---

# SDR Project Design

Use this skill when the user wants to get an SDR project built in OpenClaw.

Treat this as an **OpenClaw builder skill first** and an SDR comparison skill second.
That means your job is not only to know the SDR ecosystem, but to turn that ecosystem into an OpenClaw-friendly plan:
- what upstream project(s) to borrow from
- what should run as mode-specific services
- what should live in a dashboard or web UI
- what should store files/events/metrics
- what to build first so the user gets working value quickly

## What this skill is for

This skill helps with:
- comparing SDR projects and picking the right stack
- designing end-to-end SDR architectures
- deciding between desktop, headless, web, and ingest-first designs
- choosing where decoding should happen
- structuring storage, APIs, event streams, maps, dashboards, and playback
- avoiding common SDR project mistakes like coupling hardware, DSP, and UI too tightly

## Workflow

1. **Run intake quickly**
   If the user’s requirements are fuzzy, read `references/project-intake.md` and fill in the missing shape of the project.

2. **Classify the project**
   Put the request into one or more buckets:
   - **scanner / dispatch / public safety**
   - **web receiver / remote tuning**
   - **satellite / weather / pass-based capture**
   - **unknown signal / reverse engineering**
   - **general desktop receiver / live exploration**
   - **data collection / observability / RF lakehouse**

3. **Pick the dominant upstream inspiration**
   Use the matching family reference first, not the whole landscape blob.

4. **Translate it into OpenClaw shape**
   Default to these OpenClaw-native layers:
   - SDR-attached host or node that owns hardware
   - mode-specific ingest/decoder services
   - shared files/events/status outputs
   - dashboard / browser UI / automations above that

   Do not assume Docker, Unraid, or Linux unless the user does. If platform/runtime choice matters, read `references/platform-deployment.md`.

5. **Separate the stack into layers**
   Always reason in layers:
   - hardware + driver layer
   - source / ingest layer
   - decoder / classifier layer
   - event / storage layer
   - API / stream layer
   - UI / workflow layer

6. **Prefer loose coupling**
   Recommend architectures where the SDR hardware can be swapped, the decoder can be changed, and the UI can keep working.
   Favor:
   - SoapySDR or clean source abstraction
   - filesystem or queue-based handoff where practical
   - simple HTTP/JSON APIs for dashboards
   - containers for services, native install only where hardware bindings are fragile

7. **Check failure modes before sounding confident**
   If the plan touches vendor drivers, SoapySDR, USB passthrough, or hardware sharing, read `references/common-failure-modes.md`.

8. **Recommend one build path, not ten**
   Give one primary OpenClaw build path, then brief alternates only if they materially matter.

9. **Use an example build when it helps**
   If the request matches a common shape, read `references/example-builds.md` and borrow the closest pattern.

## What to read

Read only the most relevant reference(s):

- **broad SDR research, beginner orientation, or "help me understand the SDR landscape"** → `references/sdr-research-deep-dive.md`
- **project still fuzzy / missing requirements** → `references/project-intake.md`
- **scanner / dispatch / public safety** → `references/scanner-public-safety.md`
- **browser receiver / remote tuning** → `references/browser-receiver.md`
- **satellite / weather / pass-based capture** → `references/satellite-weather.md`
- **unknown signal / reverse engineering** → `references/reverse-engineering.md`
- **desktop live exploration, ADS-B, APRS, packet, or utility modes** → `references/general-desktop-and-utility.md`
- **architecture, system decomposition, and implementation planning** → `references/architecture-patterns.md`
- **how to actually assemble the stack** → `references/implementation-recipes.md`
- **how SDR ideas map onto OpenClaw host/node/service/dashboard structure** → `references/openclaw-build-patterns.md`
- **cross-platform deployment choices (Linux/Windows/macOS/Pi/native vs container)** → `references/platform-deployment.md`
- **hardware/runtime pain and common breakage** → `references/common-failure-modes.md`
- **SDR hardware/driver integration (RTL-SDR, SDRplay, HackRF, USRP, SoapySDR bindings, USB passthrough)** → `references/hardware-driver-integration.md`
- **worked example OpenClaw builds** → `references/example-builds.md`
- **dashboard / UI design patterns for SDR observatories** → `references/dashboard-ui-patterns.md`

## Heuristics

- **Trunked/public-safety ingest**: start with `trunk-recorder` or `sdrtrunk`; add `rdio-scanner` or `scanner-map` above them.
- **Call mapping / AI summaries / geocoding / dispatcher UX**: `scanner-map` is the strongest inspiration.
- **Browser-based tuning and multi-user receiving**: prefer `openwebrx+`; treat vanilla OpenWebRX mainly as lineage/background unless there is a specific compatibility reason not to.
- **Desktop live tuning and general exploration**: `SDR++`, `GQRX`, `CubicSDR`.
- **Satellite capture/processing**: `SatDump` first.
- **ADS-B / aircraft observability**: `readsb` / `dump1090` class decoders plus `tar1090` for map/UI are the default reference stack unless the user wants something stranger.
- **APRS / packet / igate ideas**: `Dire Wolf` is the default practical reference. Note: SDRplay/RSP1B requires SoapySDR + FM demod → FIFO pipeline, not `rtl_fm` directly.
- **Unknown 315/433/868/915 protocol work**: `rtl_433` for known devices, `URH` + `inspectrum` + `SigDigger` for discovery/reverse-engineering.
- **Deep custom DSP**: GNU Radio.
- **Hardware abstraction / avoiding vendor lock-in**: SoapySDR, but be wary of plugin/runtime/version mismatch.

## Output shape

When helping the user, usually give:
- **best-fit stack**
- **why this stack**
- **OpenClaw layout** (what runs where)
- **what each layer does**
- **implementation order**
- **likely pain points**

## OpenClaw defaults

Unless the user asks otherwise, prefer:
- SDR hardware owned by the host or paired node physically attached to it
- one mode-specific runtime per mode instead of one giant SDR app
- one shared dashboard/UI that reads files, JSON, metrics, and status from those mode services
- lightweight automation around outputs, not around raw DSP internals
- browser control or dashboard UI for operators, with a separate debug/maintenance path

A mode-specific runtime can be:
- a container
- a native service
- a pinned app/runtime on Windows or macOS
- a dedicated SBC/node process

If a project looks like a polished web product, borrow the upstream UX ideas but keep the OpenClaw build split into:
1. hardware/driver ownership
2. decoder/ingest services
3. storage/event outputs
4. web/dashboard layer

## Important SDR reality checks

- Driver stacks matter as much as app choice.
- SoapySDR is great, but version mismatches and vendor plugin/runtime issues are common.
- Satellite, trunking, and ISM projects often want different sample-rate, storage, and scheduling assumptions.
- A good SDR project usually has **two UIs**:
  - an operator UI
  - a maintenance/debug path

## Good default design style

For a home-lab “radio observatory” style project, prefer:
- **headless ingest services** on the machine with the SDR attached
- **web UI** separate from the hardware-specific code
- **append-only event storage** for decoded things
- **saved IQ/baseband only when needed**, not for everything
- **mode-specific services** rather than one giant app trying to do all DSP paths at once
