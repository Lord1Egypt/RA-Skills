# Panel Identity and Order Guard

## Purpose

Prevent the pipeline from silently using the wrong image, wrong panel, or wrong ordering when moving from story-pack planning into production.

This guard exists specifically to reduce failures like:
- image from panel A being used for panel B
- subtitle/prompt from one panel drifting onto another panel
- merged clip order not matching storyboard order
- direct-run mode silently continuing past a wrong first image

## Guard rules

### 1. Panel identity lock
Before a new generation starts, the active clip must be locked by at least one strong identity:
- `panelId`
- or `panelIndex`

Preferred lock is both.

If `panelId` and `panelIndex` both exist but point to different records, stop immediately.

### 2. Image-text-panel consistency
The active production tuple should stay aligned:
- `panelId`
- `panelIndex`
- `imageUrl`
- `videoPrompt`
- `subtitleText`

If any of these are being borrowed from a neighbor clip without explicit user approval, stop.

### 3. New-image approval rule
For a brand new clip, the first usable image should be treated as a confirmation artifact.

Default policy:
- in 逐步确认模式: always pause and show it
- in 单条保交付模式: pause unless the image is already explicitly approved for that clip
- in 配额敏感直跑模式: still pause if identity is uncertain or if the image may be confused with a neighbor panel

### 4. Merge ordering rule
Before multi-clip merge:
- verify the chosen clips are in intended `panelIndex` order
- verify there is no duplicate panel
- verify no panel is silently skipped unless the user asked for a selective cut

### 5. Main clip isolation rule
Do not let a neighbor panel's image/text replace the current main clip unless the user explicitly changes the target.

## Recommended enforcement points

Apply this guard:
1. after `get-panel-context.ts`
2. before first image approval / first paid video generation
3. before multi-clip merge

## Minimum validation output

A guard result should clearly say:
- whether identity is locked
- whether ordering is valid
- whether duplicates exist
- whether user confirmation is required before continuing

## Failure handling

If guard validation fails:
- do not auto-continue into generation
- report the exact mismatch
- ask for target correction or approval
