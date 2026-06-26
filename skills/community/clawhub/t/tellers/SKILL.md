---
name: tellers
description: "Create, edit, and share AI-generated videos using tellers.ai — an AI video platform that aggregates leading generation models (Kling, Veo, LTX, ElevenLabs, and more) for video, image, and music. Use when a user wants to upload and edit real or user footage, generate videos from scratch using stock footage or AI models, add overlays, subtitles, music, or effects, create news summaries, highlight reels, promos, or custom client videos, share or export a finished video. Also handles uploading media, checking processing status, making assets public, and any tellers CLI operation. Triggers on phrases like 'create a video', 'make a highlight reel', 'upload footage to tellers', 'generate a summary video', 'create an edit', 'add subtitles', 'use stock footage', 'share a video preview', 'export video', 'tellers'."
---

# Tellers Skill

Tellers.ai is a video creation platform. The `tellers` CLI lets you upload media and generate AI-produced videos via a conversational agent.

## Installation

### 1. Install the CLI

```bash
brew tap tellers-ai/tellers && brew install tellers
```

### 2. Get an API key

Go to [app.tellers.ai](https://app.tellers.ai) → user menu (top right) → API keys → Create new.  
Credits are required. New Google SSO users get free starter credits.

### 3. Configure

```bash
# Required
export TELLERS_API_KEY=sk_...
```

Add the export to your shell profile (`~/.zshrc`, `~/.bashrc`) to persist it.

## Workflow 1: Upload Media (non-blocking)

**Always spawn an isolated subagent for uploads** — they can take minutes and shouldn't block the main session.

```bash
# The blocking command (run inside a subagent):
tellers upload upload /path/to/footage \
  --show-status-until-analysed \
  --machine-readable
```

**OpenClaw pattern for uploads:**
```
sessions_spawn({
  task: "Run this command and report the full JSON output when it finishes:\n\ntellers upload upload \"/path/to/footage\" --show-status-until-analysed --machine-readable\n\nParse the JSON and reply with the asset_ids on success.",
  runtime: "subagent"
})
```

The subagent announces the result when done. Extract `asset_ids` from the output to use in generation.

**Output** (parsed from subagent result):
```json
{
  "success": true,
  "elapsed_seconds": 161,
  "assets": [
    {"asset_id": "abc123", "local_path": "/path/to/file.mp4", "status": "success"}
  ]
}
```

**Upload options:**
```
--show-status-until-analysed       # Wait until AI analysis done (recommended)
--show-status-until-done           # Wait until transcoding done too
--disable-description-generation   # Skip AI time-based descriptions (faster)
--force-upload                     # Re-upload even if already tracked
--parallel-uploads 4               # Concurrent uploads (default: 4)
--ext mp4 --ext mov                # Filter by extension
--in-app-path "shoots/2026-03"     # Organise in-app path
```

## Workflow 2: Generate a Video (long-running)

Video generation runs the tellers AI agent and can take 5–20 minutes. **Always run generation inside an isolated subagent** — never block the main session.

```bash
# Blocking command: waits until agent finishes, prints the final JSON result
tellers --background --json-response "Generate a 90-second news summary video from today's footage"
```

**Output** (on completion):
```json
{
  "assets": [{"id": "abc123", "type": "video"}],
  "chat_id": "88425c45-d302-4af2-89d6-e72d7bd13239",
  "message": "...",
  "projects": ["7781484c-c396-44b3-a7b0-5dda23f33bef"],
  "status": "done"
}
```

Extract `projects[0]` as the project ID and `chat_id` to build the result URL.

**OpenClaw pattern for generation:**
Spawn an **isolated subagent** with the full blocking command. The subagent waits however long it takes and announces the result (preview link) when done. The main session stays free.

```
sessions_spawn({
  task: "Run this command and report the result when it finishes:\n\ntellers --background --json-response \"<prompt>\"\n\nParse the JSON output and reply with the project ID and chat_id so the URL can be constructed.",
  runtime: "subagent"
})
```

The `tellers.json_result` SSE event carries the final output. The `--background --json-response` flags extract and print it automatically.

## Workflow 3: Combined Upload + Generate

Common pattern for "upload these videos and make an edit":

1. Spawn subagent for upload → wait for it to finish and return `asset_ids`
2. Spawn a second subagent for generation with the asset context

Both steps use isolated subagents. Upload must complete before generation starts (asset needs to be processed first).

```
# Step 1 — spawn upload subagent, wait for result
upload_result = sessions_spawn({
  task: "Run: tellers upload upload \"/path/to/footage\" --show-status-until-analysed --machine-readable\nReport the full JSON output.",
  runtime: "subagent"
})
# → extract asset_ids from result

# Step 2 — spawn generation subagent with context
sessions_spawn({
  task: "Run: tellers --background --json-response \"Create a highlight reel from asset_id: <id>\"\nReport the full JSON output including project IDs.",
  runtime: "subagent"
})
```

## Other CLI Commands

```bash
# Interactive chat REPL (for exploration)
tellers "your prompt"

# Single response, no REPL
tellers --no-interaction "your prompt"

# List assets
tellers asset list

# Export a project to have a rendered and downloadable mp4 file
tellers project export <project-id>
```

## Result URL

After upload or generation, construct the app link from the returned IDs:

```
https://app.tellers.ai/?asset_id={asset_id or project_id}&chat_id={chat_id}
```

Examples:
```
# After upload — link to the asset:
https://app.tellers.ai/?asset_id=1830d8d9-c64a-4941-bf24-bcba9acdb2e0

# After generation — link to the project with chat context:
https://app.tellers.ai/?asset_id=7781484c-c396-44b3-a7b0-5dda23f33bef&chat_id=88425c45-d302-4af2-89d6-e72d7bd13239
```

Always surface this URL to the user when a generation or upload completes.

## Sharing & Public Previews

By default assets and projects are private. To share a public preview link:

```bash
# Make an asset or project publicly accessible
tellers asset set-anonymous-read {id}

# Public preview URL (shareable with anyone, no login required):
https://www.tellers.ai/preview/{asset_id}
```

**For maximum device compatibility** (especially mobile), don't share the project preview directly. Instead:
1. Export the project first — this renders a proper MP4: `tellers project export <project-id>`
2. The export produces a new asset ID
3. Make that asset public: `tellers asset set-anonymous-read <export-asset-id>`
4. Share: `https://www.tellers.ai/preview/<export-asset-id>`

Project previews may not play on all devices; exported assets always will.

## Credits & Support

Every upload, export, and generation request spends Tellers credits. To buy more, go to [app.tellers.ai](https://app.tellers.ai) and click **"Get more tokens"**.

Questions or issues:
- 𝕏 / Twitter: [https://x.com/@rguignar](https://x.com/@rguignar)
- LinkedIn: [https://www.linkedin.com/in/rguignar/](https://www.linkedin.com/in/rguignar/)
- Discord: [https://discord.gg/sGg2fnmfCr](https://discord.gg/sGg2fnmfCr)

## Error Handling

- Exit code 0 = success
- Exit code 1 = error (check stderr)
- HTTP 401 = bad/missing API key
- HTTP 402 = insufficient credits — direct user to app.tellers.ai to top up

## Reference

Full API docs: https://www.tellers.ai/docs/dev/api  
CLI source: https://github.com/tellers-ai/tellers-cli  
OpenAPI spec: `src/tellers_api/openapi.tellers_public_api.yaml` in the repo
