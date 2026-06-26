# Provider Matrix

Use this matrix to pick providers quickly.

| Task | Primary | Secondary | Why |
|---|---|---|---|
| Photoreal product images | Freepik `mystic` | fal `fal-ai/flux-2-pro` | Mystic is strong for polished marketing visuals |
| Fast concept ideation | fal `fal-ai/flux-2` | Freepik `flux-2-klein` | Lower latency iteration loops |
| Typography-heavy posters | Freepik `seedream-v4-5` | Freepik `seedream-v4-5-edit` | Better prompt-to-text rendering |
| Multi-image consistent edits | Nano Banana 2 `google/gemini-3-1-flash-image-preview` | Freepik `seedream-v4-5-edit` | Good instruction-following with multiple references |
| Hero scene video | Freepik `kling-v3-omni-pro` | fal `fal-ai/kling-video/v2/image-to-video` | Quality-first motion with cinematic style |
| Fast scene video fallback | fal `fal-ai/minimax/video-01/image-to-video` | Freepik `kling-v3-omni-std` | Faster queue completion in some workloads |
| Voiceover | Freepik `/v1/ai/voiceover/elevenlabs-turbo-v2-5` | fal text-to-speech model | Easy ElevenLabs integration |
| Background music | Freepik `/v1/ai/music-generation` | fal audio model (search per project) | Built-in marketing music workflow |
| Final composition and captions | Remotion | Remotion + FFmpeg utilities | Deterministic timeline and export control |

## Decision shortcuts

- Need exact style continuity across many assets -> Nano Banana 2 first.
- Need polished product hero shots -> Freepik Mystic first.
- Need fastest idea exploration -> fal Flux first.
- Need final branded delivery -> always finish in Remotion.

## Environment variables

- Freepik: `FREEPIK_API_KEY`
- fal: `FAL_KEY`
- Nano Banana 2: `INFERENCE_API_KEY` or interactive `infsh login`
