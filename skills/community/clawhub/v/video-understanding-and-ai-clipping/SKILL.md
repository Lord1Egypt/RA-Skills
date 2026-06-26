---
name: wayinvideo
description: "WayinVideo AI video editing and analysis suite. Includes highlight extraction, natural language video search, content summarization, and transcription. Example scenarios: 'extract video highlights' / '分析这个视频' / 'Um clipe de um gato pulando na mesa.' / 'Transcrivez cette vidéo.'. Supports online URLs and local files with customizable export options like aspect ratio, captions, and AI reframing. Features persistent configuration for seamless automation and sub-agent optimized background polling. Use when the user needs any form of AI video editing, highlight discovery, or content analysis."
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      bins: ["python3"]
      env: ["WAYIN_API_KEY"]
    primaryEnv: "WAYIN_API_KEY"
    files: ["wayinvideo-cli/**/*"]
---

# WayinVideo - Mastering Video Editing & Understanding with AI-Powered Tools

## What is WayinVideo?
WayinVideo is an AI video editing and analysis platform designed to simplify complex video tasks with a few clicks, such as extracting viral highlights, searching for specific moments using natural language, generating comprehensive summaries, providing high-quality transcriptions, etc. WayinVideo not only provides a friendly GUI to users, but also APIs for agents to automate their workflows. Whether you are dealing with online URLs (YouTube, TikTok, etc.) or local files, WayinVideo offers customizable export options like AI reframing and captioning to make your content ready for any platform. This skill encompasses WayinVideo CLI, which simplifies the API usage and allows for persisting user preferences.

## Installation & Setup
Check if the WayinVideo CLI is already installed: `wayinvideo --help`.

- **Recommended**: Install as a local package: `pip3 install -e <ABS_PATH_TO_SKILL>/wayinvideo-cli`
- **No-Install Option**: If you prefer not to install, replace `wayinvideo <command>` with:
  `PYTHONPATH=<ABS_PATH_TO_SKILL>/wayinvideo-cli python3 -m wayinvideo <command>`

## Quick Start
Follow this simple workflow to use the CLI effectively:

1.  **Check Environment**: Ensure `WAYIN_API_KEY` is set.
2.  **Confirm Video Source**: 
    - If it's a supported URL (YouTube, Vimeo, Dailymotion, Kick, Twitch, TikTok, Facebook, Instagram, Zoom, Rumble, Google Drive), proceed to step 4.
    - If it's an unsupported URL, download it first.
    - If it's a local file (or downloaded), proceed to step 3.
3.  **Upload Local Video**: Run `wayinvideo upload --file-path <path>` to get a video `identity`.
4.  **Submit Task**: Use `wayinvideo submit <task_type> --url "<url_or_identity>"` with desired options.
5.  **Poll Results**: Use `wayinvideo poll --type <type> --id <id>` to track progress and get final results.

## What WayinVideo CLI can do?
WayinVideo supports several specialized tasks to match different user needs:

| Task Type | Description | Best Use Case | Documentation |
| :--- | :--- | :--- | :--- |
| `clip` | Extracts engaging highlights. | Creating viral social media clips or highlight reels. | `basics/ai-clipping.md` |
| `search` | Natural language video search. | Locating specific scenes, topics, or events (e.g., "the part where they talk about taxes"). | `basics/find-moments.md` |
| `summarize` | Structured content summary. | Quick understanding, key info extraction, or video QA. | `basics/video-summarization.md` |
| `transcribe` | Speech-to-text conversion. | Subtitle creation, speaker analysis, or searchable transcripts. | `basics/video-transcription.md` |
| `export` | Standalone video rendering. | Changing ratio/captions/hooks for existing clip/search results. | `basics/export.md` |

You MUST read the corresponding documentation before you submit that task.

### Selecting the Right Task
- **"Make this viral" / "Give me highlights"** -> Use **`clip`**. It's best for broad, subjective requests.
- **"Where do they mention X?" / "Find the cat jumping"** -> Use **`search`**. Perfect for specific search intent.
- **"What is this video about?" / "Summarize this meeting"** -> Use **`summarize`**. Ideal for high-level understanding.
- **"I need the full script" / "Who said Y?"** -> Use **`transcribe`**. Best for detailed textual evidence and speaker tracking.
- **"Change the subtitles to dual-lang" / "Make these clips 9:16"** -> Use **`export`**. Best for re-rendering results from a prior `clip` or `search` task.

## Advanced Usage

### Polling in the Background
Polling can be time-consuming. Run `wayinvideo poll` in a subagent or as a background task whenever possible. This allows you to stay responsive to the user while the subagent handles the task.

**Parallel Processing**: For scenarios involving multiple videos or multiple tasks (e.g., clipping and summarizing the same video simultaneously), it is highly recommended to spawn multiple parallel subagents or background tasks. This allows for concurrent execution and significantly reduces the total wall-clock time.

**Pro Tip**: 
For OpenClaw users, use `--event-interval 300` to enable progress updates via the `openclaw` CLI every 300 seconds (default is 0/disabled).
  - When you receive a reminder, update the user on the current progress.
  - Actively check the subagent/background task status every 2 * `--event-interval` seconds.
      - If the task is still active, notify the user that processing is ongoing (e.g., "Processing is still in progress; as the video is quite long, it may take a bit more time").
      - If the task is no longer active (crashed or stopped), notify the user and offer to retry (start polling again or resubmit).

### Customizing User Preferences
- **Reflect on Patterns**: Periodically review the user's recent tasks and interactions to identify consistent preferences (e.g., target language, bilingual subtitles, specific caption styles, or aspect ratios).
- **Persist Settings**: Use `wayinvideo config set <key> <value>` to save these preferences globally, ensuring a smoother and more personalized experience. Examples:
    - `wayinvideo config set defaults.target zh`
    - `wayinvideo config set defaults.clip.ratio RATIO_9_16`

### Reporting Results
If WayinVideo CLI outputs files locally, ALWAYS include the file path in your response. If the user asks for video transcription, ALWAYS ask whether they want the subtitles converted to a common format (e.g., .txt).

If an `export_link` is provided in the result:
1. **Check Expiration**:
   - If the project has expired (3 days after submission), notify the user and re-run.
   - If the `export_link` has expired (24 hours after the last poll), run `wayinvideo poll --type <type> --project-id <id>` again to refresh it.
2. **Provide the Link**: Always include the `export_link` as a clickable Markdown link. **NEVER** truncate, shorten, or alter these links.
3. **Download**: If the user wants to download the video or use it locally, use: `curl -L -o <filename> "<export_link>"`.

### Handling Complex Scenarios

You **MUST** read the corresponding advanced documentation before proceeding with these tasks.

| I want to... | Read |
| :--- | :--- |
| "Learn [subject] from these [N] videos" | `advanced/learning_from_videos.md` |
| "Find the most [adjective] clip from the video" | `advanced/searching_best.md` |

## Principles

1.  **Exhaust All Options**: Never claim a task is impossible until every tool, parameter, and workflow combination has been exhausted. There are no excuses—only creative problem-solving and persistent attempts.
2.  **Act First, Ask Later**: Use the tools at your disposal before asking for permission. When you must ask for clarification, always include diagnostic data or status updates as evidence. Never rely on memory—verify facts with documentation or logs first.
3.  **Owner, Not NPC**: Take full ownership of the end-to-end outcome. Proactively manage background tasks, handle link expirations, and deliver final results without waiting for the user to nudge you. Move the needle, don't just react.
