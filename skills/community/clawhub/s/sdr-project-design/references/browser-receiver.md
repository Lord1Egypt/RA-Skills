# Browser Receiver SDR Projects

## Core references

### openwebrx+ (preferred)
- Preferred repo family: `psyb0t/openwebrxplus` and related `openwebrx+` forks
- Lineage/background: `jketterl/openwebrx`
- Shape: **multi-user browser receiver**
- Best for:
  - remote tuning
  - public or private shared receivers
  - browser-based SDR access with stronger digital-voice interest than vanilla OpenWebRX
- Why it matters:
  - multi-user UX
  - broad hardware support
  - browser-first deployment model
  - easier sharing than desktop-only receiver tools

### KiwiSDR
- Different hardware model, but very useful as a UX reference for browser SDR ergonomics
- Study for interface/product ideas more than direct software reuse
- Good inspiration for:
  - shared listening UX
  - band navigation
  - simple public receiver experiences

## Starting from scratch

### If the user wants a remote receiver they can open from any browser
Recommend:
- `openwebrx+` first
- one supported SDR and one good antenna
- a simple private deployment before adding public access

### If the user wants a radio observatory feel
Recommend splitting the stack into:
1. browser receiver for operator tuning
2. separate decoder/event services for things like FT8, APRS, digital voice, ADS-B, or trunking
3. shared storage and dashboards above that

### If the user wants public internet access
Treat browser receiver projects like exposed infrastructure:
- TLS / reverse proxy
- auth or access control if not meant to be public
- bandwidth and CPU planning
- clear isolation between public receiver UX and sensitive internal SDR services

## OpenClaw shape
Prefer:
- `openwebrx+` as operator-facing layer
- decoder/event services separate from the browser receiver if they need different runtime assumptions
- hardware ownership kept local to the SDR-attached host/node
- web UI above a stable SDR service layer, not fused with every other decoder in the same runtime if avoidable

## When this is the wrong choice
Do **not** default to a browser receiver if the real goal is:

- trunked public-safety recording archive
- satellite pass processing
- unknown signal reverse engineering
- simple single-user desktop tuning

In those cases, use the specialized stack first and add browser access later only if it truly helps.

## Operational checklist

Before calling a browser SDR deployment done, verify:

1. SDR device opens reliably after reboot
2. waterfall/audio latency is acceptable
3. browser clients can connect concurrently
4. frequency/gain/device config survives service restart
5. reverse proxy / allowed origins / auth are set correctly if exposed
6. CPU stays sane under real user load
