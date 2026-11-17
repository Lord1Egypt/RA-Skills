# Strength Training Recording Summary Workflow

This skill turns strength-training recordings or transcripts into clean `WorkoutSummary <date>` notes for future reference. It does not require a specific app, hosted storage, or retrieval feature. Groq is one supported transcription backend, not a requirement. The useful behavior is:

1. receive a local strength-training recording or transcript
2. transcribe audio with an available backend when needed
3. standardize exercise names and calculate completed work
4. write a concise summary note
5. print or save the result as requested

## Core Guardrails

- Preserve transcript timestamps when the input format provides them.
- Keep the workflow local by default: do not upload to hosted storage, create remote workout sessions, or store vector indexes unless the user explicitly asks.
- Print the summary in chat or stdout by default.
- Save the generated transcript or summary only when asked, or when the user supplied an explicit output path.
- Do not create web portals, review screens, retrieval indexes, or database records unless the task changes from "summarize this session" to "build an app pipeline."

## Inputs

Accept common strength-training recording formats:

- `.m4a` / MP4 AAC
- `.mp3`
- `.wav`
- `.caf` when the local tooling can convert it safely
- existing transcript or summary source files such as `.md`, `.txt`, `.srt`, `.vtt`, or `.json`

Before transcription, inspect:

- file exists
- file size
- container/magic bytes if a transcription call fails
- duration if local tools such as `ffprobe` are available

Useful inspection command:

```bash
ffprobe -hide_banner "$AUDIO"
```

## Choosing A Transcription Backend

Pick the first suitable backend that is ready:

1. Existing transcript file.
   - If the user provides `.txt`, `.srt`, `.vtt`, `.json`, or Markdown transcript output, summarize that directly.
2. Local Whisper CLI.
   - Best when the user wants no cloud dependency or has no API key ready.
   - Check with `command -v whisper`.
3. Groq Whisper.
   - Fast cloud option when `GROQ_API_KEY` is configured.
4. OpenAI or another compatible speech-to-text API.
   - Use only when the user has that provider configured or explicitly chooses it.

If none is ready, do not pretend transcription is available. Explain the options and ask which backend the user wants to set up.

## Local Whisper Option

Local Whisper needs no API key if the CLI is installed:

```bash
whisper "/path/to/workout.m4a" \
  --model turbo \
  --task transcribe \
  --output_format all \
  --output_dir ./transcripts
```

For Chinese/English mixed sessions, add `--language Chinese` only when Chinese is dominant. If the trainer regularly says English exercise names inside Chinese coaching, auto-detect may preserve mixed-language names better.

## Groq Option

Use Groq's OpenAI-compatible audio transcription endpoint:

```bash
curl https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@/path/to/workout.m4a" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=verbose_json" \
  -F "timestamp_granularities[]=segment"
```

Operational notes:

- Keep `GROQ_API_KEY` in the environment, never in the skill or output.
- Do not embed a real Groq API key in a publishable skill. It can leak through git history, exported `.skill` archives, logs, screenshots, or copied prompts.
- If a deployment needs convenience, document `GROQ_API_KEY` setup or use a local secret manager/runtime secret injection.
- Prefer `verbose_json` so segment timestamps are available for the summary.
- If the account has a 25 MB audio limit, split or compress long recordings before upload.
- If Groq returns no text, inspect container and content type. `.m4a` should usually be sent as an audio file with a real `.m4a` filename.

## Other Cloud APIs

Use provider-specific commands or SDKs only when the user has credentials ready. Keep these rules provider-neutral:

- request segment-level timestamps when supported
- do not hardcode API keys
- do not commit generated transcripts unless asked
- report provider limits clearly when a file is too large

## API Key Handling

Do not embed real API keys in this skill or any publishable package. Read service keys from environment variables such as `GROQ_API_KEY` or provider-specific equivalents, a local secret manager, or an OpenClaw secret mechanism supplied at runtime.

If a user has no cloud key ready, prefer an existing transcript or local Whisper when available. If a cloud backend is required but no credentials exist, explain the options and ask which provider they want to configure.

## Optional Local Preprocessing

Use local preprocessing only when needed:

- Convert CAF/LPCM to WAV if the selected backend rejects CAF.
- Convert odd containers to `.wav` or `.m4a` while keeping speech intelligible.
- Compress oversized files before upload, commonly to mono, 16 kHz, around 24 kbps when quality is sufficient for speech.
- Split long files into smaller ordered parts, commonly 15-minute chunks, and offset timestamps when merging transcripts.
- Prefer lossless stream copy splitting first; re-encode only when the chunks are still too large or the container fails.

Useful `ffmpeg` examples:

```bash
ffmpeg -i input.caf -ac 1 -ar 16000 output.wav
ffmpeg -i input.m4a -ac 1 -ar 16000 -b:a 24k output.m4a
ffmpeg -i input.m4a -f segment -segment_time 900 -c copy part_%03d.m4a
```

When splitting, preserve part order and add each part's start offset to segment timestamps before summarizing.

## Long Transcript Boundary Reconciliation

Keep the direct transcript-to-summary workflow. Do not turn this into a separate evidence-distillation and synthesis pipeline.

For a long timestamped transcript:

1. Divide it into contiguous primary windows of approximately 15 minutes.
2. Give each window up to 90 seconds of adjacent transcript as context only. Use that context to understand continuity, but do not count its sets, reps, weights, or cues in both windows.
3. Extract the provisional exercise records supported by each primary window.
4. At each boundary, compare only the final exercise from the preceding window and the first exercise from the following window.
5. Use up to three minutes of transcript before and after the boundary to decide whether they are one continuing exercise.
6. If they are the same exercise:
   - return one exercise record
   - include every genuinely distinct completed set exactly once
   - when one set starts before the boundary and finishes after it, use the later supported completed total
   - discard the earlier partial count instead of adding it as another set
   - preserve supported cues and notes from both sides
7. If they are different exercises, timestamps are inadequate, or continuity remains unclear, keep both original records.
8. Re-sequence the reconciled exercise list and write the final `WorkoutSummary`.

Do not regenerate unrelated exercise records during boundary reconciliation. The safe failure mode is to keep the original records rather than merge two distinct exercises.

## Summary Extraction

Build the final summary from the trainer's actual sequence. Capture:

- title line: `WorkoutSummary <date>`
- total workout length
- number of completed exercises
- exercise or drill name
- duration, not raw time range
- groups, sets, rounds, reps, duration, or holds
- important breaks or coaching pauses
- trainer cues and corrections only when they add something beyond reference exercise instructions
- homework, follow-up, or next-session plans

Preferred output:

```text
WorkoutSummary <date>
Total length: 45:20
Exercises completed: 6

1. Canonical exercise name, ~2 min, 2 groups * 10 reps/side
- Direct note or cue; no `dataset match` or `trainer-specific cue` label.
```

Rules:

- Use one numbered item per exercise.
- Keep the first line to canonical name, duration, and completed volume.
- Use duration on every exercise line, not raw time ranges. For split/non-contiguous groups, use total duration such as `~4 min total`.
- Use `scripts/calc_duration.py` to calculate durations from transcript ranges when helpful.
- Count completed groups/sets and reps from the transcript; if uncertain, mark approximate.
- Put the highest-value note on the next line as one bullet, without labels like `dataset match` or `trainer-specific cue`.
- Use `about`, `roughly`, or `~` when uncertain.
- Do not invent weights, reps, pain observations, or diagnoses.
- Do not include a table unless explicitly requested.

## Exercise Dataset Cross-Reference

Use `hasaneyldrm/exercises-dataset` to standardize exercise names and avoid repeating generic instruction text:

- Repository: `https://github.com/hasaneyldrm/exercises-dataset`
- Primary dataset file: `data/exercises.json`
- The README describes 1,324 exercise records and the main schema fields:
  - `id`
  - `name`
  - `category`
  - `body_part`
  - `equipment`
  - `instructions.<lang>`
  - `instruction_steps.<lang>`
  - `muscle_group`
  - `secondary_muscles`
  - `target`
  - `image`
  - `gif_url`

The dataset includes multilingual instruction fields. Use the language that best matches the transcript when comparing trainer cues:

- `en` English
- `es` Spanish
- `it` Italian
- `tr` Turkish
- `ru` Russian
- `zh` Chinese
- `hi` Hindi
- `pl` Polish
- `ko` Korean

Fallback order:

1. Transcript language, for example `zh` for Chinese trainer speech.
2. English `en`.
3. Dataset name and metadata only, if instructions are missing.

Dataset usage rule:

- Do not put the full `data/exercises.json` into the model conversation.
- Treat it as a local/reference data source.
- Load or cache it outside the prompt.
- Build a small lookup/index over normalized `name`, equipment, target, body part, muscle group, and translated instruction text when useful.
- Match transcript candidates against that index.
- Bring only the top candidate records or compact snippets into the final LLM summary step.
- Use code or shell tools for fuzzy matching when available; use the LLM for judgment only after narrowing candidates.
- If using a subagent, hand it this workflow and the dataset path/URL, not the entire JSON blob.

## Fuzzy Matching Helper

This skill includes `scripts/match_exercises.py`, a stdlib-only helper that:

- accepts candidate exercise names or a candidates file
- loads a local `data/exercises.json` or downloads/caches the raw GitHub JSON
- matches against normalized exercise name, equipment, body part, target, muscle group, secondary muscles, and compact instruction snippets
- supports dataset instruction language selection with `--lang`
- returns compact JSON top matches for the final summarization step

Examples:

```bash
python scripts/match_exercises.py --lang zh --top-k 3 "深蹲" "侧平举"
python scripts/match_exercises.py --lang zh --top-k 3 "哑铃侧平举"
python scripts/match_exercises.py --lang en --top-k 5 "dumbbell lateral raise"
python scripts/match_exercises.py --dataset ./data/exercises.json --candidates-file candidates.txt --pretty
```

Use this helper before the final LLM summary. Do not pass the full helper output if `top-k` is large; keep only the winning record or a short candidate list per exercise.
For generic spoken names, expect several plausible variants; use nearby transcript context such as equipment, position, machine, side, incline, seated/standing, or single-arm/single-leg wording to choose.
Include equipment or variant words in candidates when the transcript provides them, for example `哑铃侧平举` instead of only `侧平举`.

## Duration Helper

This skill includes `scripts/calc_duration.py` for calculating duration from one or more transcript ranges:

```bash
python scripts/calc_duration.py 00:00-01:42
python scripts/calc_duration.py 03:50-05:17 07:51-10:00
```

Use the returned duration on the summary line instead of raw ranges. For split/non-contiguous work, add `total` if it helps clarity, e.g. `~4 min total`.

Suggested matching workflow:

1. Load or fetch `data/exercises.json` if available.
2. Detect transcript language and whether the session is monolingual or mixed language.
3. Build a normalized index from `name`, plus optional aliases inferred from equipment, target, category, translated exercise wording, and common spoken variants.
4. Extract candidate spoken exercise names from the transcript.
5. Fuzzy-match each candidate against the dataset and use transcript context to break ties:
   - equipment mentioned by trainer
   - target/body part
   - movement pattern
   - whether the trainer says a variant such as single-leg, side plank, incline, cable, band, dumbbell, or bodyweight
   - Chinese terms that describe the same movement, body part, or equipment
6. Use the dataset `name` as the summary name only when confidence is high. If the user wants Chinese output, include the Chinese-friendly spoken label beside the canonical name. Do not say `dataset match` in the summary.
7. If confidence is low, keep the spoken/trainer name and optionally add `approx.` rather than forcing a bad match.
8. Compare trainer cues to `instructions.<transcript_lang>` or `instruction_steps.<transcript_lang>`, falling back to English.
9. Include only cue highlights that are:
   - corrective for this user
   - repeated or emphasized
   - a safety/pain modification
   - a progression/regression
   - materially different from the dataset's generic instructions

Do not copy long dataset instructions into the summary. Use the dataset as a reference for standardization and cue filtering, not as summary content.

## Chinese/English Sessions

For mixed Chinese/English training audio:

- Preserve practical exercise meaning over literal translation.
- Do not force all exercise names into English if the trainer used Chinese and the user expects Chinese output.
- Prefer canonical dataset names for standardization, but keep helpful Chinese labels or trainer-spoken names when they disambiguate.
- Clean up noisy transcript fragments into normal exercise names.
- Keep trainer emphasis points such as breathing, bracing, foot pressure, knee tracking, tempo, shoulder position, and tennis-transfer homework.
- Compare Chinese trainer cues against `instructions.zh` / `instruction_steps.zh` first. Only fall back to English when Chinese fields are missing or unhelpful.

## What Is Intentionally Out Of Scope

- Next.js API routes
- remote workout session records
- Neon/Postgres tables
- web portal behavior
- review/finalization screens

Only add those pieces back if the user explicitly asks for a full application pipeline.
