# Workflow recipes

These recipes are intended for agent use.

## 1. Unknown language, best general result

```bash
node {baseDir}/assemblyai.mjs transcribe INPUT   --bundle-dir ./out   --all-exports
```

What this gives you:

- model routing
- language detection
- Markdown
- agent JSON
- raw JSON
- manifest
- paragraphs / sentences / subtitles

Use this as the safest “do the right thing” default.

## 2. Known English meeting, highest quality

```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --speech-model universal-3-pro   --language-code en_us   --speaker-labels   --bundle-dir ./out
```

## 3. Product demo with custom terminology

```bash
node {baseDir}/assemblyai.mjs transcribe ./demo.mp4   --custom-spelling @assets/custom-spelling.example.json   --keyterms "OpenClaw,AssemblyAI,Universal-3-Pro"   --bundle-dir ./out
```

Notes:

- use `--keyterms` when you want the model to pay attention to exact terms
- use `--custom-spelling` when you want specific renderings in the final text

## 4. Call-centre stereo recording

```bash
node {baseDir}/assemblyai.mjs transcribe ./call.wav   --multichannel   --speaker-map @assets/speaker-map.example.json   --bundle-dir ./out
```

Use this when left/right channels matter more than diarisation.

## 5. Named speakers from generic diarisation

First transcribe with speaker labels:

```bash
node {baseDir}/assemblyai.mjs transcribe ./interview.mp3   --speaker-labels   --bundle-dir ./out
```

Then identify the speakers:

```bash
node {baseDir}/assemblyai.mjs understand TRANSCRIPT_ID   --speaker-type name   --speaker-profiles @assets/speaker-profiles-name.example.json   --bundle-dir ./out
```

## 6. Role-labelled speakers for support or sales calls

```bash
node {baseDir}/assemblyai.mjs understand TRANSCRIPT_ID   --speaker-type role   --known-speakers "agent,customer"   --bundle-dir ./out
```

Good role pairs include:

- agent / customer
- interviewer / candidate
- host / guest
- doctor / patient
- salesperson / buyer

## 7. Translation with aligned utterances

```bash
node {baseDir}/assemblyai.mjs transcribe ./meeting.mp3   --translate-to de,fr   --match-original-utterance   --bundle-dir ./out
```

This is especially useful when a downstream agent needs:
- speaker separation
- timestamps
- per-utterance translations

## 8. Structured extraction through LLM Gateway

```bash
node {baseDir}/assemblyai.mjs llm TRANSCRIPT_ID   --prompt @assets/example-prompt.txt   --schema @assets/llm-json-schema.example.json   --out ./summary.json
```

Use this when the next consumer is a script, workflow engine, or another agent.

## 9. Re-render a saved transcript

If you already stored raw or agent JSON:

```bash
node {baseDir}/assemblyai.mjs format ./out/myfile.agent.json   --speaker-map @assets/speaker-map.example.json   --bundle-dir ./rerendered
```

## 10. Minimal stdout-only flow

For tiny clips or quick inspection:

```bash
node {baseDir}/assemblyai.mjs transcribe ./clip.wav --export markdown
```

For anything non-trivial, prefer `--bundle-dir` or `--out`.
