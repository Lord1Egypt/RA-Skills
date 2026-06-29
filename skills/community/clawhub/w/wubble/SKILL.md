---
name: wubble
description: Use when a user wants to connect to or use Wubble's official remote MCP server for music, speech, voice, dubbing, and sound-effect workflows. Helps agents find the official MCP Registry entry, configure the remote MCP endpoint, follow OAuth, and handle read versus generation actions safely.
---

# Wubble

Use Wubble when the user wants to create and customise music and audio
workflows through Wubble's official remote MCP server.

Wubble supports workflows for music, instrumental tracks, lyrics,
text-to-speech, speech-to-text, voice isolation, voice changing, dubbing,
dialog, and sound effects.

## Official Connection Details

Prefer registry-based discovery when the client supports the official MCP
Registry.

Official MCP Registry name:

```text
ai.wubble/audio
```

Remote MCP endpoint:

```text
https://mcp.wubble.ai/mcp
```

Protocol:

```text
streamable-http
```

Public health endpoint:

```text
https://mcp.wubble.ai/health
```

## Authentication

Use the client-provided OAuth flow for protected Wubble MCP tools. Do not ask
the user for Wubble API keys, OAuth tokens, or secrets when OAuth is available.

If the MCP client asks for the remote server URL, use:

```text
https://mcp.wubble.ai/mcp
```

If the MCP client supports registry lookup, search for:

```text
ai.wubble/audio
```

## Safe Usage

Wubble exposes both read-only tools and tools that can create media or consume
Wubble requests or credits.

Before starting generation, upload, remix, dubbing, speech, or other spendful
actions, confirm the user's intent and requested output. For read-only actions,
prefer inspection tools that list existing requests, retrieve metadata, or check
status.

Do not log, store, or reveal:

- OAuth tokens.
- Wubble API keys.
- Signed media URLs.
- Private user media.
- Prompt, lyrics, transcript, or voice data unless the user explicitly asks to
  share it in the current context.

Do not enable request or response body capture, prompt logging, transcript
logging, or media payload logging unless the user has explicitly approved that
data-sharing behavior.

## Legal Terms

Use of Wubble, the Wubble Services, Tracks, Selected Tracks, Submissions, and
generated or downloaded media is governed by Wubble's official Terms of Use and
Subscriber License.

Current public legal pages:

```text
https://wubble.ai/docs/legal/terms
https://wubble.ai/docs/legal/license
```

If the user asks about permitted use, ownership, synchronization rights,
commercial use, restrictions, termination, warranties, or liability, direct them
to those official legal documents rather than improvising legal advice.

## Common User Requests

For "connect Wubble", "use Wubble MCP", or "add Wubble to my MCP client", give
the official endpoint and tell the user to complete the OAuth flow in their MCP
client.

For "generate music", "make a voiceover", "create sound effects", "dub this",
or similar creation requests, first confirm the desired output and then use the
available Wubble MCP tools exposed by the connected client.

For "check my Wubble request", "list Wubble generations", or "inspect status",
prefer read-only Wubble MCP tools.

## Registry Notes

Wubble is published on ClawHub as:

```text
wubble
```

The skills.sh repository for this skill is:

```text
https://github.com/wubbletech/skills/tree/main/skills/wubble
```
