---
name: voicecheap
description: Use when the user asks to connect OpenClaw to their VoiceCheap account or use VoiceCheap for transcription, YouTube transcripts and chapters, subtitles, speech and permitted voice creation, images and thumbnails, dubbing, lip sync, publishing or workspace actions.
---

# VoiceCheap for OpenClaw

Follow [the workflow reference](references/workflows.md) for account access,
media actions, credits, retries, asynchronous status and privacy. Discover the
actual catalog before choosing a transcription, subtitle, voice, image, project
or workspace action; tools depend on the permissions the user grants.

If VoiceCheap is not connected, inspect existing MCP configuration with
`openclaw mcp status --verbose`. With the user's request to connect, add the
remote endpoint using the installed CLI's supported syntax:

```sh
openclaw mcp add voicecheap --url https://api.voicecheap.ai/mcp --transport streamable-http
openclaw mcp login voicecheap
```

Preserve an existing server and other connections. Let the user complete the
browser login and approve only `account:read` for a basic connection check.
For a requested media workflow, choose only its required permissions; a Read Only
preset may also expose project and media data. Do not extract or request
credentials. If the CLI or browser flow is unavailable, explain the exact step
the user needs to complete rather than claiming the server is configured.

Check `openclaw mcp doctor voicecheap --probe`, then use actual account/project
read tools through the active runtime. A saved configuration or successful probe
alone does not prove that an authenticated customer action succeeded. Reconnect
with additional user-approved permissions only when a requested workflow needs
them. No blanket tool auto-approval is required.

Keep account identifiers, private media, transcripts and credentials out of
public listings and demonstrations. Use synthetic review content and the
minimum permissions needed. Publishing outputs and cloning voices require
specific authorization; voice samples also require the speaker's permission.
