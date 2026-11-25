# Sound Scenes

Sound Scenes use **UYDI Audio 3.1 TTS Next** for short, freestyle audio scenes in
Chinese or English. The model can produce dialogue, layered sound effects and ambience,
or instrumental music from structured scene directions. The optional `scene-optimize`
command asks the UYDI 3.8 Flash optimizer to expand an idea into an editable draft.
Optimization does not generate audio or spend generation credits.

## Scene draft JSON

Dialogue drafts have one to three characters, each with a voice description or an existing
saved UYDI voice ID, and up to 30 ordered lines. The selected `language` is both the
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

Limits: title 80 characters; 1–3 characters and at most 30 lines for dialogue; dialogue
line 1,200 characters; voice description 400 characters; line direction 200 characters;
scene description 1,600 characters; compiled prompt 3,000 characters; generated audio
up to 120 seconds. Only Chinese (`zh`) and English (`en`) are accepted by Sound Scenes.
In structured dialogue drafts, omit `@voice1` from user text; UYDI allocates reference slots when a
saved designed or cloned voice is selected. Use its corresponding voice type, `design` or `clone`.

## Freestyle prompts

For direct control of a Next scene use a freestyle draft with `scene-create --file`.
The same JSON, wrapped in `{"draft": ...}`, is accepted by `POST /api/v1/scenes/projects`.

```json
{"kind":"freestyle","title":"Studio visit","language":"en","text_prompt":"A warm host says, “Come on in.” A second voice laughs softly as the studio door closes.","rate":1,"volume":50,"seed":42}
```

The prompt is sent verbatim as `input.text_prompt`. Optional `references` are an array
of up to three `{"voiceId":"YOUR_VOICE_ID"}` objects in slot order. Use `@voice1`,
`@voice2` and `@voice3` in the prompt to refer to those recordings. A voice’s private `referenceAudioUrl` is available with `voices:read`. Uydi sends up
to 30 seconds of audio per reference. A freestyle draft accepts pace (0.5–2), integer
volume (0–100) and seed (0–2147483647). The output is a 24 kHz mono WAV, up to 120 seconds.
The optional optimizer works on structured drafts. Freestyle drafts go directly to the quote.

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
5. The user's generation or end-to-end test request authorizes its necessary generation
   and credit deduction. Pass the live estimate automatically as
   `--quoted-credits <totalCost>`; do not ask for a second quote approval. The CLI
   rechecks the quote and balance. If the quote changes, refresh it and continue only
   within the user's stated limits; never guess a price or change an uncertain request's key.
6. Wait for the render or resume it using `scene-status <renderId> --wait`. Download the
   completed WAV with `-o <file.wav>`. If a request times out, inspect its render status
   before retrying and reuse the printed idempotency key if a retry is needed.

Scene project operations use the account's existing `synthesis:read` and
`synthesis:write` grants. Scene generation charges the quoted fixed cost once per render;
optimization, project editing, estimates, status checks and audio downloads do not
generate audio or consume scene-generation credits.
