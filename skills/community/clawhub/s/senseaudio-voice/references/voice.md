# Voice and Cloning Reference

## Table of Contents

- Voice catalog and plan levels
- Clone workflow constraints
- TTS dictionary note
- Operational guidance

## Voice Catalog and Plan Levels

The source doc defines voice availability by subscription tier:

- Free: basic voices (example IDs include `child_0001_a`, `male_0004_a`, `male_0018_a`)
- Trial/VIP tier: additional premium voices (examples under `male_0027_*`, `male_0023_a`)
- Higher tiers (SVIP etc.): broader emotional and role-oriented voices (examples across `male_*`, `female_*`)

When the user asks for "voice unavailable" troubleshooting:

1. Confirm exact `voice_id` requested.
2. Check the account tier entitlement.
3. Query the platform voice list endpoint/doc flow before concluding.

## Clone Workflow Constraints

Per source doc:

- Voice cloning is completed on the platform side first (record/upload + training).
- Direct API cloning initiation is not supported.
- API usage starts after clone completion using returned clone `voice_id`.

Recording/material requirements in doc:

- 3-30 seconds
- <=50MB
- formats: MP3/WAV/AAC
- quiet environment recommended

## TTS Dictionary Note

The document states dictionary-based polyphone correction is constrained:

- Intended for clone voice use.
- Model requirement explicitly references `SenseAudio-TTS-1.5`.

When user asks to use `dictionary`:

1. Verify they are using clone `voice_id`.
2. Verify model compatibility in their current API version.
3. If mismatch, provide fallback without dictionary or guide model switch.

## Operational Guidance

- Keep a mapping table in application config:
  - business scenario -> preferred `voice_id`
  - fallback voice per locale/style
- Fail fast on unknown `voice_id` and return actionable error.
- For emotional variants, pick explicit voice IDs rather than runtime randomization.

