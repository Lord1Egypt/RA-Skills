---
name: tts-topmediai
description: |
  TopMediai text-to-speech skill. Supports key entitlement info, voices listing
  (official + cloned), and text-to-speech generation.
author: TopMediai
---

# TTS TopMediai Skill

## Capability Overview
This skill supports:
1) Get current API key entitlement information
2) Get available voice list (official + cloned)
3) Convert text into speech with selected speaker voice

## Preflight Check (Mandatory)
- Configure `TOPMEDIAI_API_KEY` in `<skill_root>/.env`
- Optional: `TOPMEDIAI_BASE_URL` (default `https://api.topmediai.com`)
- If key is missing, stop and ask user to configure

## Main Command
- `/tts_topmediai action=info|voices|tts text="..." speaker="..." emotion="..."`

## Extra Commands
- `topmediai_tts_key_info`
- `topmediai_tts_voices`
- `topmediai_tts_generate text="..." speaker="..." emotion="..."`

## API Endpoints Used
- Key info: `GET {BASE_URL}/v1/get_api_key_info`
- Official voices: `GET {BASE_URL}/v1/voices_list`
- Cloned voices: `GET {BASE_URL}/v1/clone_voices_list`
- TTS: `POST {BASE_URL}/v1/text2speech`
