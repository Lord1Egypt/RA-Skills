# YumFu v1.7.10

This release deepens YumFu's world-structure layer and actually wires that richer structure into live gameplay context helpers.

## Highlights

### 1) World data enrichment across core universes
A broad set of YumFu worlds now carries a much richer narrative structure instead of relatively flat lore blobs.

Added / expanded fields include:
- `key_figures`
- `city_and_region_hubs`
- `relationship_webs`
- `major_items_and_artifacts`
- `mainline_stages`
- `subfaction_networks`
- `quest_hubs`
- `city_subzones`
- `story_pressure_tracks`
- `item_threads`

This was applied across major and secondary worlds, including LOTR, Harry Potter, Game of Thrones, Sengoku, Xiaoao, Yitian, Warrior Cats, Journey to the West, Lobster Sanguo, F15 Down, and Captain Underpants.

### 2) Rich world structure now reaches live context builders
The new structure is no longer passive data sitting in `world.json`.

YumFu now threads it into:
- normal gameplay context building
- continue / re-entry context building
- daily evolution preparation
- re-entry rendering hooks

That means turns can now pull from named figures, pressure tracks, quest hubs, relationship webs, and item threads when generating actual gameplay pressure.

### 3) Cleaner story-spine extraction
Fixed a real helper bug where `main_questline` dict keys could leak into extracted text and produce dirty values like `main_objective: ...` in re-entry / spine output.

Extraction now:
- reads `main_questline.main_objective` cleanly
- uses `major_story_threads` as beats when present
- avoids flattening dict keys into player-facing spine text

## Why this matters
Before this release, YumFu had increasingly rich world content but did not consistently expose that structure to the helper layer that prepares actual turns.

With v1.7.10:
- world progression is easier to keep on a recognizable main line
- re-entry hooks can feel more specific and less generic
- detours can reconnect to main pressure more naturally
- important objects and named characters can recur with better continuity

## Scope
- no save format break
- no migration required
- focused on narrative/world-context quality and helper correctness
