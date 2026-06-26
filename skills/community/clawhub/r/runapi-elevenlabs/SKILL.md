---
name: elevenlabs
description: Generate speech, dialogue, and sound with ElevenLabs through RunAPI. Use when the user asks an agent to create speech, dialogue, or sound effects, or transcribe audio with ElevenLabs. Default to the RunAPI CLI for one-off generation; use SDKs only when the user is integrating RunAPI into an app or backend.
documentation: https://runapi.ai/models/elevenlabs.md
provider_page: https://runapi.ai/providers/elevenlabs.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/elevenlabs
    requires:
      bins:
      - runapi
    install:
    - kind: brew
      formula: runapi-ai/tap/runapi
      bins:
      - runapi
    envVars:
    - name: RUNAPI_API_KEY
      required: false
      description: Optional RunAPI API key; runapi login or saved CLI config can also authenticate the runapi binary.
---

# ElevenLabs on RunAPI

Generate speech, dialogue, and sound with ElevenLabs through RunAPI. The default path for one-off agent tasks is the `runapi` CLI; SDKs are for application integration.

## Routing decision

- One-off generation, editing, or transformation for the user → use the **CLI path** with the `runapi` binary.
- Building an app, backend, worker, library, or production codebase → use the **SDK integration path**.

## CLI path

The `runapi` binary is the runtime dependency. Authenticate with `runapi login` (browser) or set `RUNAPI_API_KEY`; a saved CLI config also works — no required environment variable.

Inspect the available actions and request fields with CLI help:

```shell
runapi elevenlabs --help
runapi elevenlabs text-to-speech --help
```

Run a one-off task (synchronous — polls until the task completes):

```shell
runapi elevenlabs text-to-speech --input-file request.json
```

Submit asynchronously and poll separately:

```shell
runapi elevenlabs text-to-speech --async --input-file request.json
runapi wait <task-id> --service elevenlabs --action text-to-speech
```

Available actions: `text-to-speech`, `text-to-dialogue`, `text-to-sound`, `speech-to-text`, `isolate-audio`.

## SDK integration path

When integrating ElevenLabs into an app, backend, worker, or library — not for one-off tasks — use a RunAPI SDK package:

- JavaScript / TypeScript: `@runapi.ai/elevenlabs`
- Ruby: `runapi-elevenlabs`
- Go: `github.com/runapi-ai/elevenlabs-sdk/go`

## References

- Model overview, pricing, and rate limits: https://runapi.ai/models/elevenlabs.md
- Provider comparison: https://runapi.ai/providers/elevenlabs.md
- Full model catalog: https://runapi.ai/models.md

## Variants

- [Turbo v2.5 text to speech](https://runapi.ai/models/elevenlabs/text-to-speech-turbo-v2.5.md)
- [Multilingual v2 text to speech](https://runapi.ai/models/elevenlabs/text-to-speech-multilingual-v2.md)
- [Dialogue v3](https://runapi.ai/models/elevenlabs/text-to-dialogue-v3.md)
- [Sound effects v2](https://runapi.ai/models/elevenlabs/sound-effect-v2.md)
- [Speech to text](https://runapi.ai/models/elevenlabs/speech-to-text.md)
- [Audio isolation](https://runapi.ai/models/elevenlabs/audio-isolation.md)

