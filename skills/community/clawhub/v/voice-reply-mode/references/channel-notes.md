# Channel notes

## Telegram

Usually the easiest channel for this pattern.

Check:
- the bot can receive voice notes
- the bot can send audio/voice replies
- gateway `messages.tts` is enabled

Test:
- send a text message
- send a short voice note

## Feishu

Possible, but depends on bot capability, media upload support, and channel plugin behavior.

Check:
- bot permission to receive audio/voice content
- bot permission to upload and send voice/audio media
- whether the plugin exposes inbound audio as voice/audio to the agent

## Reality check

"Install skill and it works everywhere" is too optimistic.

What a skill can do reliably:
- package rules
- package scripts
- package config snippets
- explain channel prerequisites

What still depends on the user environment:
- channel permissions
- plugin support
- gateway config
- media upload path
