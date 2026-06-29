---
name: record2note
description: Use when converting voice recordings, voice memos, or speech transcripts into structured Markdown notes, setting up recording-folder monitoring, or processing pending transcription files on macOS or Windows
tags: [voice, recording, transcription, speech-to-text, speech-recognition, voice-memo, audio, audio-to-notes, meeting-notes, markdown, note-taking, summary, keypoints, todos, obsidian, notion, logseq, whisper, diarization, macos, windows, 录音, 语音转文字, 录音转笔记]
min_openclaw: 1.0.0
---

# record2note - Voice to Structured Notes

Convert voice recordings into structured Markdown notes with summaries, key points, todos, and speaker labels. The output works with Obsidian, Notion, Logseq, and similar note apps.

## Skill Directory

The skill root is the `record2note/` folder containing this `SKILL.md`. All script paths are relative to that folder.

## Preflight Checks

When the skill is used for the first time, follow this order:

1. Detect platform

```bash
uname -s
# Darwin = macOS, otherwise detect Windows through WSL or PowerShell environment
```

2. Check configuration

Config file: `<skill_folder>/config.json` (same folder as `SKILL.md`). If it does not exist, start the setup wizard.

3. Check dependencies

```bash
python3 <skill_folder>/scripts/common/deps_manager.py check
```

Dependency levels:

| Level | Contents | Size | When needed |
|---|---|---:|---|
| L1 Base transcription | ffmpeg + whisper binary + base model | ~200MB | Auto-downloaded on first transcription |
| L2 High quality | large-v3 model | ~3GB | User upgrades manually |
| L3 Speaker diarization | pyannote-audio + torch | ~2GB | When `diarization=true` |

`process.sh` / `process.ps1` will auto-run `deps_manager.py ensure L1` on first use, but it is better to download it during setup.

> **Important:** Before the first download, tell the user that the base model is about 148MB, medium is about 1.5GB, and large-v3 is about 3GB. On macOS, the whisper binary tries to install via Homebrew first, and falls back to building from source if needed (requires git and cmake). For China network environments, set `"mirror": "cn"` in `config.json`.
>
> **Progress:** During downloads, stream the progress output line by line (for example, `[████░░░░] 20%`). Do not truncate or hide it.

Manual dependencies still required:

- `fswatch` (macOS automatic monitoring only): `brew install fswatch`
- Python 3: macOS usually includes it; Windows: `choco install python`
- `git + cmake` (macOS only, when Homebrew is unavailable): `brew install git cmake`

Manual install commands:

```bash
python3 <skill_folder>/scripts/common/deps_manager.py install-whisper
python3 <skill_folder>/scripts/common/deps_manager.py install-ffmpeg
python3 <skill_folder>/scripts/common/deps_manager.py download-model
python3 <skill_folder>/scripts/common/deps_manager.py download-model ggml-medium.bin
python3 <skill_folder>/scripts/common/deps_manager.py download-model ggml-large-v3.bin
python3 <skill_folder>/scripts/common/deps_manager.py ensure L3
python3 <skill_folder>/scripts/common/deps_manager.py mirror
```

Mirror settings: `auto` (default), `cn`, or `intl`.

## Setup Wizard

Configuration is split into two groups:

- Required settings: vault path, sync method, model
- Advanced settings: sensible defaults, shown only when asked

### Standard Mode

```
record2note needs these settings:

1. Obsidian vault path: required, for example /Users/me/Documents/ObsidianVault
2. Sync method: iCloud / Syncthing / manual (macOS default: iCloud, Windows default: Syncthing)
3. Whisper model: base (148MB, fast) / medium (1.5GB) / large-v3 (3GB, best quality) (default: base)

Say "show advanced options" if you want more settings.
```

### Advanced Mode

```
All advanced settings:

1. Watch directory: ~/Recordings/raw (default)
2. Archive directory: ~/Recordings/archive (default)
3. Vault subdirectory: Journal/Transcripts (default)
4. Whisper binary: whisper-cli (default)
5. Whisper model path: /usr/local/share/whisper-models (default)
6. Transcript language: en (default)
7. Speaker diarization: enabled (default) / disabled
8. Speaker count: 0 (auto, default) / 2 / 3 / ...
9. Denoise: enabled (default) / disabled
10. VAD speech detection: disabled (default) / enabled (skip silence)
11. Mirror: auto (default) / cn / intl
12. iCloud watch subdir: VoiceRecordings (default)
13. Agent CLI: auto (default) / opencode / claude / codex / gemini / none
14. Note mode: markdown (default) / obsidian
15. Obsidian index page: Recording Index (default, only in obsidian mode)
```

Write the config:

**macOS:**
```bash
bash scripts/macos/setup.sh --vault "$VAULT" --sync "$SYNC" --model "$MODEL" [other options...]
```

**Windows:**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows\setup.ps1 -Vault "$VAULT" -Sync "$SYNC" -Model "$MODEL" -IcloudWatchSubdir "$ICLOUD_SUBDIR" -AgentCli "$AGENT_CLI" [other options...]
```

### Sync Setup Guidance

After `setup.sh` runs, explain the chosen sync method. The agent must help the user finish the sync setup.

#### iCloud Drive Sync

iCloud Drive lets iPhone recordings land in a macOS watch folder. After processing, files are moved out of iCloud into local archives, so they do not keep consuming iCloud space.

**Data flow:**

iPhone recording -> iCloud Drive/VoiceRecordings/ -> macOS fswatch -> process.sh -> local archive

**iPhone setup options:**

1. Shortcuts automation (recommended)
2. Third-party recorder that can save directly to iCloud Drive
3. Manual copy through Files or AirDrop

Confirm the user understands how recordings reach the iCloud watch directory.

#### Syncthing

Syncthing syncs files between phone and computer over LAN or relays, without cloud storage.

Install on each device, pair device IDs, share the watch folder, and confirm the folder is fully synced before testing.

#### Manual Mode

Move recordings into the watch directory yourself. Supported inputs:

- USB copy
- Cloud drive download
- Shared folder upload
- Direct file path when processing a recording

## Modes

### Automatic Monitoring

When the user says `Enable automatic monitoring`, run the installer and load the background service:

- macOS: launchd
- Windows: Task Scheduler

The service starts on login and watches the watch directory.

### Manual Processing

When the user says `Process recording`, `Check recordings`, or `Process pending`, handle one of these cases:

1. A specific file path
2. Batch processing of files in the watch directory
3. Processing existing JSON files in `$archive_dir/pending/`

```bash
# macOS
bash scripts/macos/process.sh "/path/to/audio.m4a"

# Windows
powershell -ExecutionPolicy Bypass -File scripts\windows\process.ps1 -InputFile "C:\path\to\audio.m4a"
```

## Transcription Flow

1. Convert the audio to 16kHz mono 16-bit WAV with ffmpeg
2. Optionally skip silence with VAD when `vad: true`
3. Optionally denoise with `afftdn` when `denoise: true`
4. Transcribe with whisper-cli using the fallback strategy described below
5. Compute a timeout from audio duration and model size
6. Optionally run pyannote-audio when `diarization: true`
7. Merge transcript and speaker labels into Markdown
8. Save metadata and transcript as JSON in `$archive_dir/pending/`
9. If `agent_cli` is not `none`, trigger the agent automatically

### Whisper Timeout

Use this formula:

`timeout = audio duration x model multiplier + 600 seconds`

| Model | Multiplier | 5 min audio | 30 min audio |
|---|---:|---:|---:|
| base | 3x | 25 min | 100 min |
| medium | 5x | 35 min | 160 min |
| large-v3 | 8x | 50 min | 250 min |

The 600-second buffer covers model loading and four retry attempts. If whisper times out, kill the process and continue with the next file.

### Duplicate Event Protection

In watch mode, fswatch can fire twice for the same file. Use two layers of protection:

1. A `.lock` file per audio file
2. A stability check that waits for file size to stop changing before processing

### Pending Directory

After transcription, save metadata and the transcript to `$archive_dir/pending/YYYY-MM-DD_<filename>.json`.

| Mode | Pending behavior |
|---|---|
| Manual mode | Generate notes immediately, keep pending JSON as backup |
| Automatic monitoring | Pending JSON is the only input for the agent |

### Automatic Agent Trigger

The `agent_cli` setting controls what happens after transcription:

| Value | Behavior |
|---|---|
| `auto` | Auto-detect, priority: opencode > claude > codex > gemini |
| `opencode` / `claude` / `codex` / `gemini` | Use that CLI |
| `none` | Do not trigger; only save pending JSON |

`trigger_agent.sh` runs the CLI in the background with the full config and templates. Logs go to `/tmp/record2note-agent.log`.

If launchd lacks user session permissions, switch to `none` and process manually.

On Windows, `trigger_agent.sh` needs a bash environment. Use Git Bash or WSL.

### Obsidian Mode

When `note_mode` is set to `obsidian`, generate notes with Obsidian-specific formatting:

| Feature | markdown | obsidian |
|---|---|---|
| Summary / key points / todos | Plain Markdown | Callouts such as `> [!abstract]` |
| `source` field | Plain path | Wikilink like `[[path]]` |
| Tags | Frontmatter tags | Frontmatter tags plus `recording` / `audio` |
| Index page | None | Maintain an index page with backlinks |

The index page lives at `$obsidian_vault/$obsidian_subdir/$obsidian_index.md`.

## Processing Pending Files

When the user says `Process recording`, `Check recordings`, or `Process pending`, or when the agent is triggered automatically:

1. Scan `$archive_dir/pending/`
2. For each JSON file:
   - Read metadata and transcript
   - Generate a structured note using the summary prompt below
   - Write the note into the Obsidian vault
   - Archive the original audio under `$archive_dir/YYYY-MM-DD/`
   - Update the note source field to the archive path
   - Delete the original file from the watch directory
   - Delete the processed pending JSON
3. Report each result in batch mode
4. If the pending directory is empty, tell the user there is nothing to process

## Summary Prompt

Use this prompt to turn the transcript into a structured note:

```
Please generate a structured note from the transcript below.

Transcript:
{{transcript}}

Requirements:
1. Create a concise title (within 15 characters)
2. Write a 100-200 character summary of the core content
3. List 3-5 key points
4. If there are actionable items, write them as checkboxes
5. Add 1-3 tags
6. Fix transcription errors using context
7. Format the transcript into paragraphs, with `[MM:SS]` timestamps at the start of each paragraph only

Output format:
Title: <title>
Summary: <summary>
Key Points:
- <point1>
Todos:
- [ ] <task1>
Tags: <tag1>, <tag2>
```

When `language` is not `zh`, use the English version of the prompt.

## Note Generation and Archiving

1. Read the template (`note-template.md` for Chinese, `note-template-en.md` for English)
2. Replace template variables:
   - `{{title}}`
   - `{{date}}`
   - `{{duration}}`
   - `{{source}}`
   - `{{speakers}}`
   - `{{language}}`
   - `{{tags}}`
   - `{{summary}}`
   - `{{keypoints}}`
   - `{{todos}}`
   - `{{transcript}}`
3. Write the note to `$obsidian_vault/$obsidian_subdir/YYYY-MM-DD-<title>.md`
4. Archive the audio to `$archive_dir/YYYY-MM-DD/<title>.<ext>`
5. Update the note source field to the archive path
6. Delete the watch file and pending JSON

## Error Handling

| Situation | Handling |
|---|---|
| Whisper GPU memory exhausted | Four-stage fallback: GPU -> `-nfa` -> `-nfa -t 2` -> `-ng` (CPU) |
| Whisper timeout | Compute timeout from duration and model, then kill and continue |
| Missing model file | Check `whisper_model_path` and ask the user to download again |
| pyannote load failure | Check `pip show pyannote-audio` and Hugging Face login |
| ffprobe failure | Skip duration, keep processing |
| ffmpeg conversion failure | Check ffmpeg and the audio file |
| File not fully synced | Wait for the configured sync delay and retry |
| Target path does not exist | Create it automatically |
| Agent CLI not found | Skip silently and save pending JSON only |

### Recovery

- Use a temporary directory during processing; archive and cleanup only after success
- Leave failed files in the watch directory
- Keep pending JSON files so they can be processed again later

## Uninstall

**macOS:** `bash scripts/macos/uninstall.sh`

**Windows:** `powershell -ExecutionPolicy Bypass -File scripts\windows\uninstall.ps1`

Uninstall stops and removes the background service and scripts, but it does **not** delete configuration files, recordings, or Obsidian notes.
