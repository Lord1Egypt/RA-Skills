# Voice Canvas reference

Read this reference when a request needs multiple speakers, multiple languages, ordered
lines, controllable pauses, or one merged delivery instead of a single TTS clip.

## Safe workflow

1. Run `credits`, `voices`, and the relevant `system-voices --language <code>` searches.
   Voice compatibility is a hard constraint; never invent a voice ID or use a voice that
   does not list the node language.
2. Run `canvas-create --title <title>` and retain the returned project ID and version.
3. Build a JSON document, then run `canvas-save <projectId> --file <file>`. When editing
   an existing project, start from `canvas-show`, preserve unchanged node IDs, and keep
   the returned current version. This enables audio reuse and prevents overwriting a
   newer edit from another client.
4. Run `canvas-estimate <projectId>`. Report the exact charge, available balance,
   character usage, chargeable nodes, and reused nodes. Do not render if `sufficient`
   is false.
5. Run `canvas-render <projectId> -o <file.wav>`. It estimates again, starts the durable
   background render, waits for completion, and downloads the final WAV. Use
   `--no-wait` only when the user wants the render left in the background.
6. If waiting was interrupted, use `canvas-status <renderId> --wait -o <file.wav>`.
   Do not start another render merely because the first command lost its connection.

## Canvas JSON

`canvas-save` accepts one JSON object:

```json
{
  "title": "Product launch story",
  "version": 1,
  "nodes": [
    {
      "id": "preserve-this-id-when-editing",
      "language": "en",
      "languageSource": "manual",
      "voice": {
        "type": "user",
        "id": "voice-id-from-voices",
        "name": "Warm Narrator"
      },
      "text": "Welcome to the story.",
      "pauseAfterMs": 300
    },
    {
      "language": "zh",
      "languageSource": "manual",
      "voice": {
        "type": "system",
        "id": "voice-id-from-system-voices",
        "name": "UYDI Voice"
      },
      "text": "接下来，让我们一起出发。",
      "pauseAfterMs": 450
    }
  ]
}
```

- A new node may omit `id`; the service creates one. Preserve the returned ID thereafter.
- `languageSource` is `manual` when the agent or user chose the language. `auto` is valid
  only when the language came from the product's detector; the CLI does not guess it.
- `voice.type` is `user` for `voices` results and `system` for `system-voices` results.
- Each node requires one language, a compatible voice, non-empty text for rendering, and
  a pause from 0 to 3000 ms. Each node is limited to 600 characters.
- The project has no application-level node cap. Total text is limited by plan: Free
  2,000 characters, Pro 20,000 characters.
- Supported language codes: `zh`, `en`, `ja`, `ko`, `fr`, `de`, `ru`, `pt`, `th`, `id`,
  `vi`, `es`, `it`, `ms`, `fil`, `ar`.

## Costs, reuse, and retries

- New or changed node audio costs 1 credit per 10 characters, rounded up per node.
- Reordering nodes or changing only pauses reuses completed node audio and costs no new
  synthesis credits. Playback, merging, downloading, and system-voice previews are free.
- The CLI prints the render `Idempotency-Key` before starting. If the request result is
  uncertain, retry `canvas-render` with `--key <same-key>` and the same project version.
  A different payload with that key is rejected.
- Only one render may be active for a project. Edits made during rendering belong to the
  next project version and are not part of the active render.
- A failed node prevents delivery of a partial final file. Successful node audio remains
  reusable for the next render, and failed charges are refunded once by the service.

## Command details

- `system-voices --language <code>` supports `--search`, `--gender`, `--age`,
  `--scenario`, `--cursor`, and `--limit`.
- `canvas-estimate` and `canvas-render` default to the current project version. Pass
  `--version` when replaying an exact workflow; stale versions return a conflict.
- `canvas-render` waits up to 1,800 seconds by default. Override with `--timeout <seconds>`.
- `canvas-status` without `--wait` returns the current render and per-node states. Add
  `--wait` to poll until completion and `-o` to download when ready.
- `canvas-renders` lists completed deliveries. Incomplete or failed renders are not
  presented as finished history.
- `canvas-delete` is destructive and is rejected while a render is active.
