# Cross-Platform SDR Deployment in OpenClaw

Use this file to avoid accidentally designing every SDR project as “Docker on Unraid.”

## Core principle

OpenClaw SDR projects should be **platform-flexible** by default.
Design around:
- hardware ownership
- mode services
- stable outputs
- dashboard / automation layer

Do **not** assume a specific host platform unless the user does.

## Platform guidance

### Linux hosts
Best general default for:
- always-on SDR services
- USB SDRs
- Docker/Podman friendly workloads
- headless observatory nodes

Good for:
- Unraid
- Ubuntu/Debian servers
- Raspberry Pi OS
- other Linux SBCs

### Windows hosts
Best for:
- desktop operator workflows
- SDR software that is strongest on Windows
- Java or GUI-heavy tools like some scanner stacks
- hardware setups where vendor tooling is easiest on Windows

Prefer:
- native install first
- separate OpenClaw dashboard/orchestration layer if the DSP stack is Windows-native

### macOS hosts
Best for:
- desktop/manual SDR exploration
- developer workstations
- lighter receiver/operator setups

Caution:
- USB and library paths can be fussier
- not always the best target for fragile always-on radio backends

### Raspberry Pi / SBCs
Best for:
- dedicated single-purpose receivers
- APRS igates
- ADS-B feeders
- small observatory satellites / weather jobs
- remote radio nodes

Caution:
- CPU limits
- storage wear
- thermal constraints
- some heavier browser or AI layers should live elsewhere

## Runtime guidance

### Native install
Prefer for:
- SDRplay or other vendor-library-heavy stacks
- hardware bring-up
- fragile USB/daemon requirements
- Windows/macOS-first radio apps

### Containers
Prefer for:
- stable Linux-native decoders
- clean service isolation
- mode-specific workloads with known dependencies
- reproducible headless services

Do not force containers when native is clearly safer.

### Mixed deployment
Often best overall pattern:
- **native or pinned runtime** for the fragile hardware-facing decoder
- **container or lightweight service** for dashboard/API/automation
- OpenClaw coordinates the whole thing

## OpenClaw build rule

Phrase recommendations like this:
- what should run **natively**
- what should run as a **service/container**
- what should run on the **main host**
- what should run on a **paired node**
- what outputs the dashboard should consume

That keeps the skill useful for Linux, Windows, macOS, SBCs, and mixed setups.
