# Scanner / Public Safety SDR Projects

## Core stack references

### scanner-map
- Repo: `PoisonedNumber/scanner-map`
- Shape: **AI-enhanced call mapping + web + Discord layer**
- Inputs: `SDRTrunk`, `TrunkRecorder`, or `rdio-scanner` style endpoints
- Best for:
  - fire/EMS/police mapping
  - AI summaries and call intelligence
  - event-centric scanner dashboards

### trunk-recorder
- Repo: `TrunkRecorder/trunk-recorder`
- Shape: **headless ingest/recording engine**
- Supports trunked P25 / SmartNet and several conventional use cases
- Uses GNU Radio and OP25-derived functionality in the deeper P25 path
- Best for:
  - recorder nodes
  - self-hosted call archives
  - feeding OpenMHz, Rdio Scanner, scanner-map
- Great when the user wants a decomposed service architecture instead of one desktop app

### rdio-scanner
- Repo: `chuot/rdio-scanner`
- Shape: **scanner-style playback/distribution UI**
- Inputs include Trunk Recorder, SDRTrunk, RTLSDR-Airband, and others
- Best for:
  - self-hosted live/recent call listening
  - frontend over existing recorders
- Caveat:
  - project has a restricted WebSocket API policy for native app ecosystem; plan around public documented interfaces

### SDRTrunk
- Repo: `DSheirer/sdrtrunk`
- Java app for decoding, monitoring, recording, and streaming trunked/mobile radio protocols
- Best when you want a more all-in-one local operator workflow than trunk-recorder provides
- Better fit for:
  - workstation-first users
  - users who want UI plus decode in one place
  - smaller systems where service decomposition is less important

### OP25
- Repo: `boatbod/op25`
- Deep P25-focused stack
- Best when RF/trunking depth matters more than polished general UX
- Often the right choice for someone who wants maximal control and accepts rough edges

### OpenMHz
- Hosted ecosystem around call sharing from trunk-recorder
- Useful as a reference distribution model
- Good inspiration for data model, playback UX, and archival browsing

### Trunk Player
- Self-hosted playback/archive layer often paired with trunk-recorder output

## Starting from scratch

### If the user wants the simplest path to a DIY scanner
Recommend:
- `SDRTrunk` for single-box operator workflow
- or `trunk-recorder` if they care more about archive/search/distribution than one local UI

### If the user wants a long-term self-hosted scanner platform
Recommend:
1. ingest/recording core (`trunk-recorder`)
2. playback UI (`rdio-scanner` or equivalent)
3. optional map / AI / event enrichment layer (`scanner-map` style)

### If the user is unsure whether they need trunking at all
Clarify first:
- conventional analog only
- conventional digital only
- P25 trunked
- DMR / NXDN / mixed environment

Because the right stack changes a lot once true trunk-following is required.

## Architecture patterns

### One-box local scanner
- SDRs attached to one host
- decoder + UI together
- good for experimentation or personal use

### Headless recorder + web UX
- SDR-attached ingest host
- recorder stores calls + metadata
- web UI separate
- best for always-on boxes, family/shared access, remote listening

### Intelligence-enhanced dispatch view
- recorder core
- metadata/event database
- geocoding / talkgroup metadata / AI summary layer
- map/event UI on top

## Hardware / deployment notes

- Trunking projects often want more bandwidth and cleaner RF conditions than casual FM listening
- Antenna and front-end filtering matter a lot
- Multi-site or multi-system monitoring may need multiple SDRs or higher-performance radios
- Cheap dongles can work, but public-safety-style projects punish poor dynamic range quickly

## Best-fit guidance

### If you want a modern dispatch intelligence experience
Use:
- `trunk-recorder` or `sdrtrunk` for ingest
- `rdio-scanner` for scanner/listening UX
- `scanner-map` for map/AI/event intelligence

### If you want the strongest OpenClaw pattern
Prefer:
- ingest/recording service on the SDR-attached host
- discrete call files + metadata as outputs
- separate playback/map/intelligence layers above that

### If you want the fastest operator success
Use:
- `SDRTrunk` first
- move to `trunk-recorder` + sidecars once the user wants scale, sharing, or cleaner architecture

## Operational checklist

Before calling a scanner build "working", verify:

1. control channel decode is stable
2. site frequencies and system definitions are correct
3. talkgroup metadata is usable
4. recordings are landing where expected
5. playback/search UI sees the data
6. retention/storage plan will not eat the disk alive
