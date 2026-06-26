# Story Pack Specification

## Goal

Seedance should output a stable intermediate pack that production can consume without reinterpreting the story from scratch.

This is the default required start point when the user only provides a short topic /一句文案.
Do not skip directly to panel regeneration or video submission in that case.

## Required Files

### 0. `E01_前置思考.md`
Should include:
- episode boundary
- core conflict
- main viewpoint
- intended style / tone
- rhythm plan
- why this should be one clip / one episode / multi-clip chain
- obvious production risks

This file exists to make the Seedance-side reasoning explicit before formal script writing.

### 1. `E01_剧本.md`
Should include:
- episode summary
- beat-by-beat scene progression
- emotional rhythm
- character intent
- candidate narration lines if useful

### 2. `E01_素材清单.md`
Should include:
- character list
- location list
- prop list
- weather/time constraints
- style constraints

Recommended fields:
- id
- name
- type
- must-have traits
- continuity notes

### 3. `E01_分镜.md`
Should include one row/block per shot or panel:
- shot id
- scene id
- panel index
- shot type
- action description
- camera movement
- continuity note
- subtitle candidate
- tail-frame handoff note if needed

## Quality Rules

- the pack must be concrete enough for production
- avoid abstract literary-only descriptions
- every shot should be visually producible
- weather and mood should be explicit when important
- continuity-sensitive shots should include handoff guidance

## Recommended Normalization

Keep story pack fields stable across episodes so downstream scripts can consume them predictably.
