# Sound Scenes

Sound Scenes use **Qwen Audio 3.1 TTS Next** for short, freestyle audio scenes in
Chinese or English. The model can produce dialogue, layered sound effects and ambience,
or instrumental music from structured scene directions. The optional `scene-optimize`
command asks UYDI's Qwen 3.8 Flash optimizer to expand an idea into an editable draft.
Optimization does not generate audio or spend generation credits.

## Scene draft JSON

Dialogue drafts have one or two characters, each with a voice description or an existing
UYDI design voice ID, and up to 30 ordered lines. The selected `language` is both the
spoken language and the language used for newly generated scene text.

```json
{
  "title": "Rainy convenience store",
  "language": "en",
  "kind": "dialogue",
  "characters": [
    {"id":"clerk","name":"Clerk","voice":{"type":"description","description":"Calm, warm adult voice with a relaxed pace"}},
    {"id":"student","name":"Student","voice":{"type":"description","description":"Young adult voice, slightly breathless but friendly"}}
  ],
  "lines": [
    {"characterId":"student","text":"Is the last bus still running?","direction":"A little out of breath"},
    {"characterId":"clerk","text":"It just left. The rain has slowed everything down."}
  ],
  "atmosphere":"Rain taps on the shop awning, refrigerator hum inside, distant traffic. Keep ambience under the dialogue.",
  "seed":42
}
```

For sound effects and ambience, use `kind: "soundscape"` and set `characters: []` and
`lines: []`. Describe audible events directly in `atmosphere`:

```json
{"title":"Dawn woodland","language":"en","kind":"soundscape","characters":[],"lines":[],"atmosphere":"Layer close dew drops and soft leaves with scattered birdsong; a stream sits far behind. Slowly brighten the sound, then settle into a gentle natural loop."}
```

For original instrumental music, use `kind: "music"` with empty character and line
arrays. Specify style, tempo feel, instruments, dynamics and ending. Do not request
lyrics or singing:

```json
{"title":"Lantern festival cue","language":"zh","kind":"music","characters":[],"lines":[],"atmosphere":"轻快温暖的节庆器乐，笛子与拨弦乐器交替，加入克制的手鼓节奏；旋律逐渐展开，最后柔和收束。不要人声。","seed":42}
```

Limits: title 80 characters; 1–2 characters and at most 30 lines for dialogue; dialogue
line 1,200 characters; voice description 400 characters; line direction 200 characters;
scene description 1,600 characters; compiled prompt 3,000 characters; generated audio
up to 120 seconds. Only Chinese (`zh`) and English (`en`) are accepted by Sound Scenes.
Do not put `@voice1` references in user text; UYDI allocates reference slots when a
saved design voice is selected.

## Recommended workflow

1. Ask the user which language to use if it is unclear. Keep the page, scene draft and
   generated dialogue in that language.
2. Run `scene-optimize --language <zh|en> --idea <idea>` to produce a richer draft, or
   prepare the JSON directly. For an existing draft, pass `--draft-file <file>`; the
   optimizer must preserve user-authored dialogue and character identity.
3. Review the optimized JSON and save it to a file. Create a project with
   `scene-create --file <file>` or update one with `scene-save <projectId> --file <file>`.
   Scene files may be the direct draft, `{ "draft": ... }`, an optimizer's
   `{ "suggestion": { "draft": ... } }`, or a saved project response with `version`.
4. Run `scene-estimate <projectId>` and show the exact `totalCost` and `balance`. Never
   infer current pricing from older examples.
5. Generate only after the user has requested generation or approved the exact quote.
   Pass the same amount as `--quoted-credits <totalCost>`. The CLI rechecks the live
   estimate and refuses to start if the server quote changed or funds are insufficient.
6. Wait for the render or resume it using `scene-status <renderId> --wait`. Download the
   completed WAV with `-o <file.wav>`. If a request times out, inspect its render status
   before retrying and reuse the printed idempotency key if a retry is needed.

Scene project operations use the account's existing `synthesis:read` and
`synthesis:write` grants. Scene generation charges the quoted fixed cost once per render;
optimization, project editing, estimates, status checks and audio downloads do not
generate audio or consume scene-generation credits.
