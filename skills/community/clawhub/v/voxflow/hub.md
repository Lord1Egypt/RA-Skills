
# VoxFlow Skill — Hub

<CRITICAL-AUTO-UPGRADE>
If ANY `voxflow` command you run prints `<voxflow-hint ... type="cli-outdated" ...>` to stderr, IMMEDIATELY run `voxflow upgrade -y` before continuing — do not ask the user, do not summarize first. The hint tag also carries `action="voxflow upgrade -y"`; honor it verbatim.

If `voxflow upgrade` itself errors with `Unknown command` (CLI predates 1.12.0), fall back to `npm i -g voxflow@latest && voxflow skills install --all` — that's the only path for the very first bootstrap.

This rule is non-negotiable: an outdated CLI silently disables features the user expects (e.g. cloned-voice listing). Upgrade first, work second.
</CRITICAL-AUTO-UPGRADE>

VoxFlow turns text into speech in 200+ voices across 40+ languages, plus full audio/video pipelines. This skill is the **entry point**: install, auth, voice search, and the simple `say` / `narrate` / `story` workflows.

For specialized tasks, switch to:

- **Podcasts** (multi-speaker dialogue) → [podcast.md](podcast.md)
- **Short videos / AI clips / knowledge cards** (`picstory`, `present`, `slides`, `explain`) → [video.md](video.md)
- **Article → vertical card video (Slice)** — 6 themes (paper / editorial / poster / Notion / brutalist / glass), web app + Remotion → [slice.md](slice.md)
- **Transcription, subtitle translation, dubbing, summarize, publish** (`asr`, `asr-jobs`, `translate`, `dub`, `video-translate`, `summarize`, `publish`) → [transcribe.md](transcribe.md)

## Install & login

Install once, never ask the user again:

```bash
npm install -g voxflow
voxflow login          # opens browser — Google or email OTP
```

Token cached at `~/.config/voxflow/token.json`. For CI, set `VOXFLOW_TOKEN`.

## Authentication

```bash
voxflow login        # browser-based, one-time
voxflow status       # who am I + remaining quota
voxflow logout
```

## Voice search — always do this before synthesizing

Never guess voice IDs. Search first.

```bash
voxflow voices --lang zh --gender female
voxflow voices --lang en
voxflow voices --search "narrator"
voxflow voices --all
```

No login required for the public catalog. Output includes the voice ID, language, gender, and a short description.

### Listing the user's own cloned voices

When the user says things like "用我的克隆声音 / use my cloned voice / 用我之前克隆的", the public `voxflow voices` catalog **does not include cloned voices** — you must query the authenticated endpoint:

```bash
voxflow voices --mine
```

Prints cloned voice IDs, names, duration, and creation time (requires login). Always run this **before** concluding the user has no cloned voice — the web UI "我的声音" tab and `--mine` are the only sources of truth.

### Popular voice IDs (sane defaults)

| ID | Style | Language |
|----|-------|----------|
| `v-female-R2s4N9qJ` | 温柔姐姐 (gentle female) | zh |
| `v-male-s5NqE0rZ` | 自然男声 (natural male) | zh |
| `v-male-Bk7vD3xP` | 威严霸总 (authoritative male) | zh |
| `v-female-m1KpW7zE` | 傲娇学姐 (sassy female) | zh |
| `v-female-T8m4WxP7` | Chenwen (native English female) | en |

## Voice cloning (`clone`)

Clone a voice from a local audio file (30s+, wav/mp3). Returns a permanent voice ID usable in all commands.

```bash
voxflow clone --input recording.wav --name "My Voice"
# → Voice cloned successfully!
# → Voice ID: My_Voice_xxxxx_01
```

No file? Opens the web UI for browser-based recording:

```bash
voxflow clone
# → Opens https://www.voxflow.studio/app#voice-clone
```

| Flag | Default | Notes |
|------|---------|-------|
| `--input <file>` | (none) | Audio file to clone from. Without this, opens web UI |
| `--name <name>` | filename | Human-readable voice name (1-50 chars) |

Tips:
- Quiet room, normal speaking pace, no background music → best results
- 60 seconds is optimal; 30s minimum
- Don't "perform" — natural speech clones better than broadcast voice

After cloning, use the voice ID anywhere: `--voice <id>`

## Text-to-speech (`say` / `synthesize`)

The atomic command. One snippet → one audio file.

```bash
voxflow say "你好世界" -o hello.mp3
voxflow say "Hello world" --voice v-female-T8m4WxP7 -o greeting.mp3
voxflow say "慢速朗读" --speed 0.8 -o slow.mp3
voxflow say "高质量音频" --format wav -o output.wav
```

| Flag | Default | Range / Values |
|------|---------|----------------|
| `--voice <id>` | `v-female-R2s4N9qJ` | any voice ID from `voxflow voices` |
| `--format <fmt>` | `pcm` | `pcm` (WAV), `wav`, `mp3` |
| `--speed <n>` | `1.0` | `0.5` – `2.0` |
| `--volume <n>` | `1.0` | `0.1` – `2.0` |
| `--pitch <n>` | `0` | `-12` – `12` |
| `--output <path>` | auto-named | any writable path |

After synthesis, auto-play: `open output.mp3` (macOS).

## Long text (`narrate`)

Split a document or long string into sentences, synthesize each, concat into one file.

```bash
voxflow narrate --input article.txt -o narration.wav
voxflow narrate --input readme.md --voice v-male-Bk7vD3xP -o readme_audio.wav
voxflow narrate --text "第一段。第二段。第三段。" -o paragraphs.mp3
echo "Hello world" | voxflow narrate -o hello.wav
```

Best for: long documents, articles, README files, email newsletters.

Markdown is stripped automatically (headings, links, code fences, etc.) — no need to clean it first.

## AI story (`story`)

LLM writes a short story on the topic, then narrates it.

```bash
voxflow story "一只会飞的小猫" -o story.mp3
voxflow story "space adventure" --lang en -o adventure.wav
```

Best for: bedtime stories, content samples, demos.

## Quota

Free tier: 10,000 quota / month (resets monthly). Bonus pool from invitations never expires.

| Operation | Cost |
|-----------|------|
| 1 TTS call (`say`) | ~50 |
| `narrate` | ~50 per segment |
| `story` (short) | ~350-1000 |
| `podcast` (medium) | ~2,800 (2K script + ~16 × 50 TTS) |
| `picstory` 5-scene | ~2,850 |

Always check before expensive operations:

```bash
voxflow status
```

## Common scenarios

### "把这段话念出来"
```bash
voxflow say "用户输入的文字" -o /tmp/out.mp3 && open /tmp/out.mp3
```

### "用温柔女声读这个文件"
```bash
voxflow voices --lang zh --gender female
voxflow narrate --input file.txt --voice v-female-R2s4N9qJ -o /tmp/narration.mp3
```

### "讲个睡前故事"
```bash
voxflow story "小狐狸的星星种子" --lang zh -o /tmp/bedtime.mp3 && open /tmp/bedtime.mp3
```

### "多语言朗读"
```bash
voxflow voices --lang en --gender female   # pick English voice
voxflow voices --lang ja --gender female   # pick Japanese voice
voxflow say "English text" --voice <en_id> -o /tmp/en.mp3
voxflow say "日本語テキスト" --voice <ja_id> -o /tmp/ja.mp3
```

## Creative workflows (combine TTS with the agent's writing)

The agent writes content first, then synthesizes each part with `say` or `narrate`.

### Audio storybook (有声绘本)

1. Write a 6-page children's story.
2. For each page: generate inline SVG illustration (400×300).
3. `voxflow say "page text" --voice v-female-R2s4N9qJ --speed 0.85 -o /tmp/page_N.mp3`
4. Read mp3 files, base64-encode, embed inline in HTML.
5. Output a single self-contained HTML file with audio play buttons per page.
6. `open /tmp/storybook.html`

### Article → audio briefing

```bash
# Agent fetches the URL, summarizes, then:
voxflow say "summary text" --voice v-male-s5NqE0rZ -o /tmp/briefing.mp3
```

### Document narration

```bash
voxflow narrate --input README.md --voice v-female-R2s4N9qJ --speed 0.9 -o /tmp/readme.mp3
```

### Git daily report audio

1. `git log --oneline --since="1 day ago"`
2. Agent summarizes.
3. `voxflow say "today's summary..." -o /tmp/daily.mp3`

### Mock interview

1. Agent generates 3 interview questions on the topic.
2. For each: `voxflow say "question N..." --voice v-male-Bk7vD3xP -o /tmp/q_N.mp3`
3. Play sequentially.

## Prerequisites

- **Node.js** `^20.19.0 || >=22.12.0`
- **voxflow CLI ≥ 1.12.0** (for `voxflow voices --mine` — lists the user's cloned voices)
- **ffmpeg** — only for video-related commands (see [video.md](video.md), [transcribe.md](transcribe.md))
- **Login** required for any API call — `voxflow login`

### How the auto-upgrade signal works

The CLI itself emits `<voxflow-hint type="cli-outdated" ...>` on stderr whenever a newer version is on npm. The top-of-skill `<CRITICAL-AUTO-UPGRADE>` rule already covers what to do — this section is just the reference for what the tag looks like:

```
<voxflow-hint v="1" type="cli-outdated" current="1.10.21" latest="1.13.0" action="voxflow upgrade -y" />
```

Emitted at most once per 24h (cached in `~/.config/voxflow/update-check.json`). Opt out for users who don't want the check: `VOXFLOW_NO_UPDATE_CHECK=1` (or `NO_UPDATE_NOTIFIER=1`, the industry-standard env).

You can also poll explicitly with `voxflow upgrade --check` (no side effects) if the user is on a known-old version and you want to verify before kicking off expensive work.

## Feedback & support (AI can do this automatically)

When a voxflow command fails or the user asks to report a problem, **you (the AI agent) should file the issue directly** — don't ask the user to do it manually.

### AI workflow

```bash
# Submit directly — no browser, no TTY required.
# Uses `gh` CLI if available (direct GitHub issue creation).
# Falls back to printing the pre-filled URL if gh is not installed.
voxflow feedback --bug \
  --title "asr crashes on 2-hour wav files" \
  --body "Error: timeout after 30s\n\nCommand: voxflow asr long.wav\nExpected: transcript\nActual: Fatal error: request timeout"
# stdout → the created GitHub issue URL  (or a pre-filled URL if gh is not installed)
```

System info (CLI version, OS, Node) is appended to the body automatically.

### Flags

| Flag | Description |
|---|---|
| `--bug` / `--feature` / `--general` | Issue type |
| `--title <text>` | Title — triggers non-interactive mode |
| `--body <text>` | Description body |
| `--print-url` | Force URL output instead of submitting (even if gh is available) |

### User-initiated (interactive)

```bash
voxflow feedback          # interactive prompts → submit via gh or browser
voxflow feedback --bug    # skip type prompt, rest is interactive
```

### When to file automatically

- Any CLI command exits with a fatal/unexpected error → offer to file a bug
- User says "这个不好用" / "report this" / "提个 issue" → call with `--title` and submit directly

## Installing third-party voices or templates (`add`)

```bash
voxflow add <recipe-name>                  # install a voice preset or pipeline template
voxflow add --list                         # browse available recipes
voxflow add chico/my-recipe --force        # install from a custom author namespace
```

Use this when the user asks to install a specific named recipe (e.g. `dub-anime-jp-zh`). The registry is currently limited — if `--list` returns 404, the recipe may need to be referenced by full URL or the registry is not yet public.

## Rules

1. **Search voices before use** — never invent voice IDs. Always run `voxflow voices` first.
2. **Check quota** before podcasts (~5K), picstory (~3K), or batched jobs: `voxflow status`.
3. **Auto-play** after synthesis: `open output.mp3` (macOS) / `xdg-open` (Linux).
4. **Never print tokens or secrets** to logs.
5. If a command fails, run `voxflow <cmd> --help` to confirm flags before retry.

## When to switch skills

- User says "podcast" / "对话" / "多人对谈" → load [podcast.md](podcast.md).
- User says "short video" / "知识卡片" / "小红书" / "TikTok" / "AI clip" / "render" → load [video.md](video.md).
- User says "Slice" / "切片视频" / "文章转视频" / "PaperSlide" / "paperslide" / "paper-slide" (legacy) / "纸面手绘风" / "文章转知识短视频" / "知乎长文转视频" / "公众号转视频" → load [slice.md](slice.md).
- User says "transcribe" / "字幕" / "dub" / "translate this video" / "SRT" → load [transcribe.md](transcribe.md).
