# founder-product-video ops notes

Operational notes moved out of `SKILL.md` so the main skill stays workflow-shaped.

## Active server constraints

| Area | Note |
|---|---|
| SeeDance idempotency | Calls with identical prompt, refs, duration, and sound can replay a cached task. Use unique per-act seeds. |
| SeeDance moderation | Real-person references can intermittently trip the likeness filter. Re-roll the founder ref with stronger stylization before retrying. |
| MiniMax music length | Five `lyrics` sections drive 60-80s instrumental length more reliably than prompt prose. Avoid bare `[instrumental]`, which may be sung literally. |
| Brand logo uploads | `mcp__pika__upload_asset` rejects SVG (`image/svg+xml`). Use PNG/JPG/WebP logo exports from `build-a-brand`, or rasterize SVGs to PNG with `mcp__pika__html_to_png` before uploading. |
| CDN assets in HTML | Pika CDN does not send permissive CORS headers. Use CSS `background-image` for remote logos/photos in rendered HTML. |
| Captions | Prefer `add_captions` word-level timing over local transcription for default subtitle burn-in. Use manual subtitles only when exact timestamps already exist. |
| Final assembly | Prefer MCP `edit_concat` + `edit_audio_mix`; local concat/mix is only a fallback when the tool surface is unavailable. |
| Lower-third overlay | Local ffmpeg remains the fallback for arbitrary transparent alpha overlay until MCP exposes a general compose primitive. |
