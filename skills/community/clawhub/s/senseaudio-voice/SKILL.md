---
name: senseaudio-voice
description: Guide for SenseAudio voice selection, plan-level voice entitlement checks, and cloned voice usage constraints in TTS calls. Use this whenever user asks why a voice_id is unavailable, how to use cloned voices, or how to configure pronunciation/dictionary behavior for clone voices.
---

# SenseAudio Voice

Use this skill for voice inventory, entitlement, and clone-related integration behavior.

## Read First

- `references/voice.md`

## Workflow

1. Confirm target `voice_id` and user account tier.
2. Verify whether the requested voice is entitlement-limited.
3. For clone use cases, ensure platform-side cloning is completed first.
4. Validate dictionary/model constraints before enabling polyphone overrides.
5. Provide fallback voice strategy when requested voice is unavailable.

