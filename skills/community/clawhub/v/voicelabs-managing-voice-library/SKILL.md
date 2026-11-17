---
name: managing-voice-library
description: "Lists and manages the voice profiles on a VoiceLabs account: shows voices, adds built-in preset voices, suggests a voice for a language, and clones a voice from a recording only after the user confirms the speaker consented. Use when the user asks 'what voices do I have', 'add a built-in narrator voice', 'which voice fits French', 'clone my voice from this recording', 'create a custom voice', or wants to manage their voice library."
---

# VoiceLabs voice library

Show the user their voices and add the ones they need. Built-in preset voices can be added freely; a cloned voice copies a real person and is handled with care.

## Connecting and calling the tools

Every tool in this skill comes from the `voicelabs` MCP server, the VoiceLabs connector, and is written here as `voicelabs:<tool>`. The server lists the named tools and the Code Mode pair side by side.

- **Tools listed by name:** call them directly, for example `voicelabs:list_voice_profiles`.
- **Several operations in one round trip, or a named tool is missing:** call `voicelabs:search_tools` first, then call each tool inside `voicelabs:execute_typescript` as `external_<tool>` (for example `external_list_voice_profiles`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `voicelabs:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects VoiceLabs and approves that scope.
- **No `voicelabs` tools at all:** VoiceLabs is not connected yet. Install the VoiceLabs power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

- `voicelabs:list_voice_profiles`: every voice on the account with id, name, description, language, `voice_type` (`preset` or `cloned`), default engine, and generation and sample counts. An empty account returns an `emptyState` message; relay it rather than reporting a failure.
- `voicelabs:ensure_voice_profile`: make sure a voice with a given `name` exists, creating it from a built-in preset (optional `engine`, `builtinVoiceId`, `language`, `description`). Idempotent: the same name returns the same profile with `created: false`.
- `voicelabs:clone_voice_profile`: create a cloned voice from a 2 to 30 second recording (`name`, `referenceText` with the exact words spoken, the audio as `audioBase64` or `audioUrl`, optional `language`). Only present when the user granted the `voice:clone` scope.
- `voicelabs:search_tools`: lists the exact declarations, including the accepted engines and languages, when you need them.

## Workflow

1. Call `voicelabs:list_voice_profiles`. Present the voices in a table: name, type, language, engine, generations.
2. To add a narrator or a voice in another language, call `voicelabs:ensure_voice_profile` with a clear name and the `language`. Report whether it was created or already existed, and its id for `voicelabs:speak`.
3. To clone a voice, first confirm the recording is of the user's own voice, or that the person speaking has agreed to have their voice cloned. Then check `voicelabs:list_voice_profiles` for a name clash, and call `voicelabs:clone_voice_profile` with the recording and the exact words spoken in it.
4. Offer the `reading-text-aloud` skill to try the voice.

## Rules

- Never clone a voice without that confirmation of consent, and never clone a public figure or someone the user has not said agreed. If `voicelabs:clone_voice_profile` is not available, cloning happens in the VoiceLabs studio; say so.
- `voicelabs:ensure_voice_profile` only adds built-in presets; do not describe it as cloning.
- A duplicate name is refused on cloning; pick another name with the user.
- `QUOTA_EXCEEDED` on cloning means a plan limit on saved cloned voices; relay the message as written and stop.
- Deleting voices is not available through this connector; point the user to the studio.
