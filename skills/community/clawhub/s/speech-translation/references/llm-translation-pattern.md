# LLM Translation Pattern

Use this pattern when the agent itself should perform translation instead of a manual paste flow or external translation API.

## Recommended agent workflow

1. Run transcription first.
2. Read `01_transcript.txt`.
3. Translate with the current model.
4. Save the translated text to a file such as `02_translation.txt`.
5. Run the synthesis stage by invoking the pipeline with:
   - `--translation-backend llm`
   - `--translation-file <path>`

## Translation prompt pattern

Use a short, deterministic prompt. Example:

```text
Translate the following spoken transcript from {source_lang} to {target_lang}.
Requirements:
- Preserve meaning accurately.
- Normalize obvious speech disfluencies when helpful.
- Do not add commentary.
- Output only the translated text.

Transcript:
{transcript}
```

## Why this pattern

The current bundled pipeline is local Python code. It does not directly call the live OpenClaw model runtime from inside Python. The cleanest default is therefore:

- ASR and TTS stay in scripts
- translation is produced by the agent/model in the surrounding workflow
- the pipeline consumes that translation file deterministically

## When to prefer service instead

Prefer `service` when you need:
- unattended batch runs
- a stable HTTP translation provider
- non-agent environments where no live model is available
