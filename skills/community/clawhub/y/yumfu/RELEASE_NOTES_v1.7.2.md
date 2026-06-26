# YumFu v1.7.2 — Delivery Flow + TTS + Journey to the West Style Fix 🐒

## Highlights

This release tightens YumFu’s real gameplay delivery flow and improves consistency across visuals and voice.

## What's New

### 1. Stronger turn delivery rules
- Added stricter per-turn delivery rules to prevent duplicate image sends
- Explicitly disallowed the bad pattern of sending an image first and then sending image+caption again for the same turn
- Refined fallback behavior so slow image generation should prefer:
  - **text first**
  - then **delayed image later**
  instead of duplicate-feeling image delivery

### 2. New turn delivery state tracking
- Added `scripts/turn_delivery_state.py`
- Tracks per-turn delivery status:
  - `main_text_sent`
  - `image_sent`
  - `tts_sent`
  - `image_mode`
- Prepares YumFu for safer de-duplication and more stable multi-step turn delivery

### 3. Default per-save TTS rules
- Added stable per-save TTS settings
- TTS is now designed to be **enabled by default** unless explicitly turned off
- Voice selection is now language-aware and save-aware
- Same save + same language should keep the same voice unless the player explicitly asks to change it

### 4. Turn TTS generation workflow
- Added `scripts/generate_turn_tts.py`
- Added `scripts/resolve_tts_voice.py`
- Supports generating one gameplay-turn voice message with a stable voice profile
- Designed for **voice-bubble** delivery on supported chat platforms

### 5. Journey to the West art style correction
- Fixed the visual direction for **西游记 / Journey to the West**
- Clarified that this world should **not** lean toward wuxia or xianxia aesthetics
- Updated it toward a:
  - **bright**
  - **classic**
  - **storybook / fairytale**
  - **simple mythic Chinese illustration**
  style, with classic cloud-edged decorative shapes and traditional Journey to the West visual feeling

## Why this release matters

YumFu is not just adding worlds — it is becoming more coherent as a real playable AI RPG system.

This release focuses on player experience quality:
- cleaner delivery
- fewer confusing duplicate messages
- more stable TTS behavior
- better world-specific visual identity

## No breaking changes

- No save reset required
- No new user command required
- Existing worlds remain compatible

## Release Focus

**Main theme of v1.7.2:**
> Make YumFu feel cleaner, more stable, and more stylistically correct during real gameplay.
