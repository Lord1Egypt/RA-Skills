---
name: vibbit-skills
version: 1.0.9
display_description: |
  Help you use Vibbit AI to generate B-roll materials, replicate viral scripts, break down trending videos, check avatars, and generate avatar voiceover videos with one click.
  - B-roll Image Generation — Tell me the topic or script, and I'll generate matching B-roll images
  - Viral Replication — Give me a Douyin/Xiaohongshu/Bilibili link, and I'll analyze the video content, extract the script structure, and replicate it
  - Viral Breakdown — Deep analysis of a video's hook, rhythm, and script to understand why it went viral
  - Check Avatars — See which avatars are available in your account
  - Avatar Voiceover — Give me a script, choose an avatar, and I'll generate a voiceover video
description: Call Vibbit OpenAPI to complete five capabilities — AI image generation, parse Douyin/Xiaohongshu/Bilibili links, viral video breakdown, query available avatar list, initialize avatar voiceover video workflow. When users say "generate an image / AI image", "parse this Douyin/Xiaohongshu/Bilibili link", "break down this viral video / video breakdown", "show me my avatars / list avatars", or "use XX avatar for voiceover / initialize avatar video / avatar voiceover", this skill should be triggered proactively, even if the user doesn't explicitly mention "vibbit" or "openapi". As long as the task maps to one of these five capabilities and the user is working with the Vibbit/willing-agentcy system, prioritize this skill over writing HTTP requests manually.
metadata:
  openclaw:
    primaryEnv: VIBBIT_API_KEY
    requires:
      env:
        - VIBBIT_API_KEY
      anyBins:
        - ffprobe
    envVars:
      - name: VIBBIT_API_KEY
        required: true
        description: "Vibbit platform API Key, get it from https://app.vibbit.ai/api-keys"
      - name: VIBBIT_BASE_URL
        required: false
        description: "API base URL, defaults to https://openapi.vibbit.cn, use this to switch to test environments"
---

# Vibbit OpenAPI Skill

Wraps Vibbit OpenAPI's five capabilities into a Node.js CLI so Claude doesn't need to write HTTP calls manually each time. Two are **synchronous** APIs (submit and get results immediately), and three are **asynchronous** APIs (script auto-polls until COMPLETED/FAILED).

## When to Trigger

Trigger this skill when the user's request matches any of the following:

| User Intent (Examples) | Task Type | Sync? |
| --- | --- | --- |
| "Generate an image", "AI draw a cat", "create image" | `AIGC_IMAGE_GENERATION` | Async |
| "Parse this Douyin link", "What's this Xiaohongshu link about" | `PARSE_CONTENT_URL` | Async |
| "Break down this viral video", "Video breakdown", "Analyze this product video" | `VIDEO_BREAKDOWN` | Async |
| "What avatars do I have", "List available avatars" | `QUERY_DIGITAL_HUMAN_LIST` | Sync |
| "Use XX avatar for voiceover", "Initialize avatar video", "Avatar voiceover" | `DIGITAL_HUMAN_ORAL_BROADCAST` | Sync |

Do not use this skill for any scenarios outside these five.

## Prerequisites

The user's shell must have these environment variables exported:

- `VIBBIT_API_KEY` — Bearer token issued by Vibbit platform, **required**, script exits with error if missing
- `VIBBIT_BASE_URL` — **Optional**, defaults to production `https://openapi.vibbit.cn`; export this variable to override for other environments (test/staging)

When `VIBBIT_API_KEY` is missing, tell the user to get it from https://app.vibbit.ai/api-keys, and after they get it, help them configure it; don't guess or skip.

Node.js 18+ required (uses built-in `fetch`). The script gets material metadata via remote API `https://tools.vibbit.ai/api/file-info`, no WASM or npm dependencies needed. If the system has `ffprobe` (comes with ffmpeg), it will automatically be used as a fallback probe method, but it works fine without it.

## Script Path

Script directory: `$VIBBIT_SKILL_DIR = ~/.claude/skills/vibbit-skills/scripts`, main entry is `$VIBBIT_SKILL_DIR/vibbit.js`. The `$VIBBIT_SKILL_DIR` in examples below is for readability only; use the actual absolute path when calling.

> **Standalone Usage**: `scripts/vibbit.js` is a **self-contained** single file with no npm dependencies. Copy it to any Node 18+ machine and run directly, not limited to `~/.claude/skills/`. If the system has `ffprobe`, it can optionally be auto-enabled, but it works fine without it.

## How to Call

Always use the bundled CLI, don't call HTTP APIs directly. This is important because the wire format has several gotchas:

1. `input_info.input` is an **already-stringified** JSON (double-encoded), not a nested object
2. All fields use **snake_case** (`task_type`, `input_info`, `digital_human_id`, etc.)
3. `oral_broadcast`'s `material_list` requires complete `file_info` structure for each element (including `file_size` / `mime_type` / `width` / `height` / `duration`, etc.), which the script auto-detects and generates

```bash
node $VIBBIT_SKILL_DIR/vibbit.js <subcommand> [--args]
```

On success, the script writes JSON to stdout: sync tasks return `{"result": ...}`, async tasks return `{"task_id": "...", "result": ...}`; on failure, it outputs `{"error": "..."}` and exits with non-zero code. After getting stdout, parse out useful fields first, then present to the user in natural language; don't dump raw JSON to the user.

## Subcommands

### 1. AI Image Generation — `gen_image`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js gen_image \
  --prompt "a cute orange cat sitting on a window sill, studio ghibli style" \
  [--ref-url https://cdn.example.com/ref.jpg]
```

- `--prompt` required. Translate/copy the user's words as-is; don't add embellishments unless the user explicitly asks for refinement
- `--ref-url` optional, reference image

The script submits and auto-polls; the final `result` usually contains the generated image URL, give the URL directly to the user.

### 2. Parse Link — `parse_url`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js parse_url \
  --url "https://v.douyin.com/xxxxxxx"
```

Supports Douyin/Xiaohongshu/Bilibili share links. `result` typically contains original video URL, title, description, ASR subtitles. Only show fields the user cares about, don't dump everything.

### 3. Viral Video Breakdown — `breakdown`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js breakdown \
  --video-url "https://cdn.example.com/video.mp4" \
  --sub-tasks asr,hot,bgm
```

- `--video-url` required. Can pass share links (Douyin/Xiaohongshu/Bilibili) or raw MP4 URLs directly; breakdown includes parsing capability internally, no need to call `parse_url` first
- `--sub-tasks` required, comma-separated, options:
  - `asr` — Speech to text
  - `transition` — Transition analysis
  - `hot` — Viral hooks analysis
  - `bgm` — Background music
  - If user doesn't specify, default to `asr,hot`, and **tell the user what you chose** so they can correct

Breakdown tasks are slow, 1-2 minutes is normal. During the wait, proactively tell the user "Analyzing video, please wait" so they know it's running, not stuck.

### 4. Query Avatar List — `list_digital_humans`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js list_digital_humans
```

Synchronous API. Returns available avatar configurations for the current user (tenant-level + shared + personal). When presenting to the user, at least show names, list by group, let the user directly say "use XX", don't make them manually enter IDs.

### 5. Initialize Avatar Voiceover — `oral_broadcast`

```bash
node $VIBBIT_SKILL_DIR/vibbit.js oral_broadcast \
  --message "Hello everyone, today I'll introduce a new product..." \
  --digital-human-id 10001 \
  [--title "New Product Launch"] \
  [--material-url https://cdn.example.com/a.mp4 \
   --material-name "Product A Shot.mp4" \
   --material-url https://cdn.example.com/b.jpg \
   --material-name "Packaging Close-up.jpg"]
```

- `--message` required. **Both chat message and preset script** — backend automatically sets `has_script` to true, whatever text the user passes will be used as the video voiceover script verbatim, LLM won't rewrite it
- `--digital-human-id` required. If user doesn't specify which one, call `list_digital_humans` first to let them choose, then continue
- `--title` optional. If passed, it's used as the preset title, skipping the LLM auto-title generation step; if not passed, backend calls the model to generate as usual
- `--material-url` optional, repeatable. Each item only passes URL, `file_name` defaults to auto-inferred from URL tail.
- `--material-name` optional, repeatable. **If passed, must match the count of `--material-url`, corresponding in order of appearance**. Use this when the user provides friendly names (e.g., OSS key is gibberish, display name has specific requirements); can omit entirely if not needed.

**Before calling `oral_broadcast` in any case, B-roll image generation must be completed first**. Whether the script is user-provided or generated and confirmed in conversation, always run `gen_image` first, get the image URLs, then submit the voiceover. Unless the user explicitly says "no B-roll" or "no images", this step cannot be skipped.

Synchronous API. The returned `result` is a **string URL** pointing to the frontend chat page (production and demo domains differ). When returning to the user, present in the following format, don't use other wording:

```
All set for you
Topic: {voiceover title or first 10 chars of script}
Avatar: {avatar name}
B-roll Materials: {N} images total (omit this line if no materials)
Check it out, and if it looks good, generate the video 👉 {URL}
```

## Capability Combinations

- User says "help me make a voiceover" but **doesn't provide a script** → First ask "What topic do you want this video to cover?", help write a voiceover script based on the topic, show it to the user for confirmation; after script is confirmed, if no avatar is selected yet, list avatars for the user to choose; after selection, automatically chain B-roll generation + voiceover (same as the flow below)
- User says "help me make a avatar voiceover" but doesn't specify avatar, **and already has a script** → First `list_digital_humans`, present options to the user, wait for them to choose before continuing
- User says "help me make a voiceover" and provides a script, or there's already a confirmed script in context → **Must generate B-roll first, then submit voiceover, cannot skip**:
  1. Based on the script topic, automatically infer 3-4 B-roll scene descriptions, call `gen_image` sequentially to generate (no need for user to describe scenes additionally)
  2. Collect all successfully generated image URLs (skip failures, don't block the flow)
  3. Include images as `--material-url` in `oral_broadcast`, submit together
  4. Return result in new format (including B-roll count)
- User says "help me replicate this video" / "viral replication" + share link → Go through complete replication flow:
  1. `parse_url` to parse the link, get title + ASR subtitles
  2. Show the original video script (restored from ASR subtitles) to the user
  3. Extract the original video's hook structure, rhythm, core selling points from subtitles, use the same logic to **recreate** a voiceover script (not copy, but recreate), show to the user
  4. Ask "Which script to use? Or want to modify?", wait for user confirmation before continuing
  5. Based on script topic, automatically infer 3-4 B-roll scenes, run `gen_image` in parallel
  6. Submit script + successfully generated B-roll together to `oral_broadcast`
  7. Return result in unified format
- User asks "what can you do" / "what features" / "how to use" → Reply:

  > I can help you with these:
  >
  > - Make voiceover videos — If you have a script, I'll make it directly; if not, tell me the topic and I'll write it
  > - Replicate viral videos — Drop a Douyin/Xiaohongshu/Bilibili link, and I'll make one for you
  > - Break down videos — Analyze why a video went viral, where the hooks are, how the rhythm flows
  > - Generate B-roll — Auto-generate images based on voiceover content
  > - Check avatars — See which avatars you can use
  >
  > What would you like to do?

- **First interaction**: If the user has no clear task intent after installation or update (e.g., just greeting, saying "hi", "hello", "start", etc.), proactively reply with the feature introduction above to guide the user to choose what they want to do
- User drops a Douyin share link saying "analyze this viral video" → Directly call `breakdown`, pass the share link, no need to call `parse_url` first
- User only wants to know the content of a share link (not analysis) → `parse_url` is enough
- User wants the original link/download address of a video → Call `parse_url`, extract the original video URL from the result and give to the user
- User mentions a reference image URL when doing AI image generation → Use `gen_image --ref-url`, don't mistakenly trigger `parse_url` or `breakdown`

## Error Handling

- **Missing API Key** → Tell the user: "Need to configure Vibbit API Key first to continue. Get it here: https://app.vibbit.ai/api-keys, then tell me and I'll help you configure it.", don't guess or skip
- **HTTP 401/403** → Tell the user: "API Key has expired, please get a new one from https://app.vibbit.ai/api-keys and reconfigure"
- **Task failed** → Tell the user the task didn't succeed, suggest contacting Vibbit support with the task link; don't dump raw error messages to the user
- **Wait timeout (over 10 minutes)** → Tell the user: "Video is still processing, may need more time. Contact support with your task link: {chat page URL returned by oral_broadcast}"

## Don't Do These

- Don't write `curl` / `fetch` yourself — always use `vibbit.js`. snake_case + double-stringified JSON + file_info structure are traps that easily cause bugs when written manually
- Don't dump complete raw JSON responses to the user, extract key fields (URL, title, transcription, etc.) and present in natural language
- Don't make up avatar IDs or video URLs, ask the user if they don't provide them
