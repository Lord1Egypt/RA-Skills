# SDR Dashboard / UI Patterns

Use this file when the user asks how an SDR dashboard should behave, or when a project needs a polished observatory UI.

## Core pattern

Do **not** treat every decoder burst as a first-class UI object.

Prefer this model:
1. **raw append-only event stream** stays on disk
2. **aggregator** groups/normalizes by device, call, aircraft, pass, or session
3. dashboard renders:
   - **current state cards**
   - **recent history**
   - **operator controls**
   - **artifact/map/audio views**

## Best ideas borrowed from upstream projects

### scanner-map
Borrow:
- map-first layout for geographic events
- event cards with recency and actionable detail
- clustering/filtering rather than raw firehose spam

### openwebrx+
Borrow:
- mode switching controls
- operator-centric panel layout
- decoding as an integrated experience, not hidden backend magic

### SatDump
Borrow:
- artifact-oriented presentation
- gallery/history around successful outputs
- pass/job thinking instead of constant stream thinking

### Rdio Scanner
Borrow:
- group transmissions into higher-level listening objects
- show recency/history, not every packet/burst equally

### SDR++ / desktop receivers
Borrow:
- clear operator status
- simple tuning/frequency presets
- dense but readable control surfaces

## Recommended observatory UI shape

### Top bar
- project/system status
- active mode badge
- hardware status
- quick links

### Control strip
- mode buttons
- mode-specific presets (frequencies, bands, pipelines)
- notes about current operating state

### Current-state cards
Use cards for stable entities, not raw bursts.
Examples:
- weather station card
- aircraft summary card
- APRS station card
- active scanner call card
- current satellite pass card

### History section
Show recent changes over time:
- recent calls
- recent weather updates
- recent passes
- recent decoded packets/events

### Operator artifact area
One large “main pane” for the mode’s natural artifact:
- aircraft map
- pass image gallery
- spectrum/waterfall
- audio player/listener

## Grouping guidance by mode

### ADS-B
- summary cards + tar1090 map
- do not redraw your own map if tar1090 already solves it well

### rtl_433 / ISM
- group by **device id / model / likely device identity**
- card should show latest decoded values and last seen time
- history should show change-over-time, not every repeated burst

### NOAA / satellite
- gallery + pass timeline
- status by pass, not by every internal decode line

### Scanner/public safety
- card/list by call/session/talkgroup event
- audio/transcript/map layered together

## Anti-patterns

- showing every decoder burst as a top-level row forever
- mixing hardware-debug noise into the operator UI
- rebuilding a solved mode artifact (like tar1090 map) for no reason
- coupling dashboard rendering directly to fragile decoder internals

## Practical rule

A good SDR dashboard should answer:
- what mode is active?
- is it healthy?
- what useful thing is happening now?
- what changed recently?
- what can the operator do next?
