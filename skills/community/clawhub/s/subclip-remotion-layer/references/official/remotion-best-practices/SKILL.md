---
name: remotion-best-practices
description: Frame-driven React motion authoring within the Subclip sandbox.
version: 4.0.530
---

Read `$subclip-remotion-layer` and its authoring contract first. Use the allowlisted markup references for timing, sequencing, effects, images, embedded visual assets, motion blur, and light leaks. Subclip owns fonts/resources, media/audio libraries, composition registration, preview, and export.

Use only pinned imports accepted by `validate_runtime_layer_source`. Package installation, standalone CLIs, provider API keys, arbitrary fetch/scripts, and project scaffolding are unavailable. Use Subclip's selected speech provider and native audio lane for voiceover. Existing `$subclip-map-route` and `$subclip-map-explainer` skills remain the supported map workflows; no additional map SDKs or paid map providers are enabled.
