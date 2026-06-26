# waoowaoo Input Specification

## Purpose

This file defines how production resolves a concrete clip target from waoowaoo state.

## Minimum Required Inputs

- project id
- episode id
- panel id or clip identity
- source image / first-frame source
- video prompt
- subtitle text
- existing video state if present

## Resolution Rules

### Source of Truth Priority
1. database/project state
2. current formal task result
3. explicit user override
4. temporary probe data

### Main Clip Rule
At any time, one clip may be designated as the **main clip**.
That clip gets priority for:
- quota use
- subtitle alignment
- narration generation
- ambience work
- final packaging

### Subtitle Authority
Use the panel's current subtitle field (`srtSegment` or equivalent) as the authoritative short-text source unless the user explicitly overrides it.

### Existing Output Handling
If multiple outputs exist for the same panel:
- identify whether they are probe or formal
- prefer formal accepted output
- do not merge result counts across probe and formal tasks

## Guard Requirements Before Generation

Before first-image approval or paid generation, validate:
- target `panelId`
- target `panelIndex`
- `imageUrl`
- `videoPrompt`
- `subtitleText`

These fields should resolve to the same active panel identity.
If they drift across neighboring panels, stop and re-lock the target.

## Suggested Resolved Output

```json
{
  "projectId": "",
  "episodeId": "",
  "panelId": "",
  "panelIndex": 0,
  "imageUrl": "",
  "videoPrompt": "",
  "subtitleText": "",
  "existingVideoUrl": "",
  "isMainClip": true
}
```
