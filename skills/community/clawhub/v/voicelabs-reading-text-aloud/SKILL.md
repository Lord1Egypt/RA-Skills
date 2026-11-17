---
name: reading-text-aloud
description: "Turns text into spoken audio in the user's VoiceLabs voices and hands back the audio link. Use when the user asks to 'read this paragraph in my Narrator voice', 'narrate these five sections', 'make a voiceover', 'convert this text to speech', 'generate an audio version', 'say this in my voice', or wants text to speech (TTS) for a script. Generation is metered by the user's plan."
---

# Read text aloud with VoiceLabs

Generate speech from the user's text in one of their voice profiles, wait for it to finish, and give them the audio link.

## Connecting and calling the tools

Every tool in this skill comes from the `voicelabs` MCP server, the VoiceLabs connector, and is written here as `voicelabs:<tool>`. The server lists the named tools and the Code Mode pair side by side.

- **Tools listed by name:** call them directly, for example `voicelabs:list_voice_profiles`.
- **Several operations in one round trip, or a named tool is missing:** call `voicelabs:search_tools` first, then call each tool inside `voicelabs:execute_typescript` as `external_<tool>` (for example `external_list_voice_profiles`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `voicelabs:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects VoiceLabs and approves that scope.
- **No `voicelabs` tools at all:** VoiceLabs is not connected yet. Install the VoiceLabs power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `voicelabs:list_voice_profiles`: the account's voices with id, name, language, `voice_type` (preset or cloned) and engine.
- `voicelabs:ensure_voice_profile`: make sure a named voice exists, creating it from a built-in preset if it does not. Safe to repeat.
- `voicelabs:speak`: start a generation from `text` with `profileId` or `profileName` and optional `language`. Returns `generationId` with status `generating`.
- `voicelabs:get_generation`: poll a generation; returns `status` (`generating`, `completed`, `failed`) and, once completed, `audioUrl`.
- `voicelabs:search_tools` and `voicelabs:execute_typescript`: start several generations in one round trip for multi-part scripts.

## Workflow

1. Pick the voice. If the user named one, pass it as `profileName`. Otherwise call `voicelabs:list_voice_profiles` and ask which voice, or suggest one that matches the text's language.
2. If the account has no voices, or `voicelabs:speak` returns `NOT_FOUND`, offer a built-in preset: call `voicelabs:ensure_voice_profile` with a name such as "Narrator" and use the id it returns.
3. Call `voicelabs:speak` with the text and the voice. Keep the `generationId`.
4. Call `voicelabs:get_generation` with that id. While the status is `generating`, call it again. When it is `completed`, give the user the `audioUrl`. If it is `failed`, report the `error` field.
5. For a long script, split it at paragraph or section breaks and generate each part (see below). Return the links in order, labelled by section.

## Several parts in one round trip

Call `voicelabs:search_tools` first to get the exact declarations, then start every part at once. Do not wait for audio inside the sandbox; return the ids and poll `voicelabs:get_generation` afterwards.

```ts
const parts = ["Section one text", "Section two text"];
const started = await Promise.all(
  parts.map((text) =>
    external_speak({ text, profileName: "Narrator" }).catch((e) => ({ error: String(e) })),
  ),
);
return started; // generationId per part, or "<CODE>: <details>"
```

## Rules

- Speak only the text the user gave or approved. Do not add intros, disclaimers, or extra lines.
- Audio links expire after about 15 minutes. If the user comes back later, call `voicelabs:get_generation` again for a fresh link.
- `QUOTA_EXCEEDED`: the account's allowance for the period is used. Relay the message as written and stop; do not push a plan or retry.
- `RATE_LIMITED`: wait the `retryAfterSeconds` it names, then continue.
- `SCOPE_MISSING`: the connection lacks `voice:generate`; the user can reconnect and grant it.
- Arguments are strict and camelCase (`profileId`, not `profile_id`).
