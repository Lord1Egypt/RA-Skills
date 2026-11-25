---
name: voiceover
description: Generate narration with Subclip's selected speech provider and place it in the native audio lane.
metadata:
  tags: voiceover, audio, tts, speech
---

# Voiceover in Subclip

Read `$subclip-tts` and the live speech catalog. Default to the provider, model, and voice selected in Subclip's system settings. Honor an explicit creator choice. If no selection exists, use the live catalog default; ask only for missing required inputs.

Generate speech through Subclip's native speech tools. Reuse the creator's existing authorization for the exact script and settings. Do not request provider API keys, call provider APIs directly, create Node scripts, install packages, or write public-folder assets from this sandbox.

Import the completed speech into the audio library and place it on a native AudioPanel item/audio lane using its managed URL. Keep narration outside the Remotion/HyperFrames/HTML layer unless the creator specifically requires an embedded visual component to own that audio. Match scene timing to the imported audio's measured duration using Subclip's project tools; Subclip owns composition registration and export.

ElevenLabs is available only when it is the creator's selected or explicitly requested provider; it is not the default recommendation.
