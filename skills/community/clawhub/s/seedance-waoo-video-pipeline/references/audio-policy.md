# Audio Policy

## Goal

Keep audio decisions aligned with the user’s real intent instead of mixing everything by habit.

## Main audio modes

### 1. 旁白为主
Use when the user wants narration to lead.

Priority:
1. narration
2. ambience
3. optional extremely light music only if approved

### 2. 环境音优先
Use when the user wants scene realism over speech.

Priority:
1. ambience
2. optional sparse dialogue
3. avoid obvious music bed

### 3. 无台词环境版
Use when the user wants only atmosphere.

Rules:
- no narration
- no fake speech implication unless approved
- ambience must match scene semantics

### 4. 角色说话版
Use when the user wants real spoken dialogue.

Rules:
- spoken text must be intentional, not accidental
- if the video prompt implies mouth movement, ensure the audio plan is explicitly decided
- do not leave a “mouth moving but no speech” mismatch without warning

## Ambience acceptance rules

Reject ambience if it sounds like:
- generic background music
- heroic score
- emotional bed with obvious melody
- unrelated indoor/urban noise

Accept ambience when it supports scene semantics, e.g.:
- wind
- snow pressure
- cold emptiness
- subtle room/temple air movement

## Cross-clip merge rules

When merging multiple clips:
- rebalance loudness between clips
- avoid hard ambience resets at clip boundaries
- use one continuous low bed if needed for naturalness
- do not let one clip sound like a separate project
