# OpenClaw Chat Mode

Use this mode when the user sends a voice message and expects a conversational result instead of only local files.

## Goal

For one inbound voice message, produce three user-visible outputs in this order:

1. transcript text
2. translation text
3. translated audio

## Recommended agent behavior

1. Detect audio/voice intent.
2. If OpenClaw already provided a transcript in the inbound context, use it.
3. If a transcript is not yet available, run or arrange transcription first.
4. Translate with the current model.
5. Send transcript text.
6. Send translation text.
7. Call the `tts` tool on the translated text.

## Output templates

### Transcript text

```text
转写结果
----------------
{transcript}
```

### Translation text

```text
翻译结果
----------------
{translation}
```

## Tool preference

- Use OpenClaw `tts` when replying back into chat with audio.
- Use Piper when the workflow needs a local wav file artifact.
- Use the local Python pipeline when you need persistent files or batch processing.

## Important constraint

The current local Python pipeline does not directly invoke the live OpenClaw model runtime. Therefore, in chat mode:

- translation should normally happen in the surrounding agent turn
- `tts` should normally be the final delivery mechanism for audio back to chat

## If the user wants full unattended automation

That is a gateway-level integration task. Implement it with an outer workflow or hook that reacts to inbound audio/transcribed messages, then drives the same three-stage response sequence.
