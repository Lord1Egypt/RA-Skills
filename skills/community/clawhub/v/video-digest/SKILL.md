---
name: video-digest
version: 2.2.0
description: 把一段视频变成能读的笔记——公开字幕抓进本地私有缓存，按时间戳产出 Quick / Deep / Research 三档笔记，每句都能定位回原片。适合"三十分钟的视频只想花三分钟"和"口播内容想存成可检索文字"。Turn a video into timestamped Quick / Deep / Research notes from public captions or a supplied transcript, cached privately per user. Use when the user shares a video link and wants a summary, deep notes, or a citation-ready excerpt; also when they ask whether captions are available or why transcript fetching fails.
allowed-tools: RunCommand, Bash, Read, Write, WebSearch, WebFetch
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Video Deep Reader

## What It Does

Turn a YouTube video or supplied transcript into a useful reading artifact:

- **Quick**: decide in a minute whether the video is worth watching.
- **Deep**: understand the argument, evidence, structure, and important timestamps.
- **Research**: verify selected material claims against public primary sources.

The bundled fetch helper retrieves public metadata and subtitles; Research mode may additionally verify selected claims with public sources. The agent creates the semantic notes from these inputs.

Bundled components are deliberately separate:

- `fetch_video.py --doctor` checks the local dependency and optional network readiness.
- `fetch_video.py` retrieves public metadata and subtitles into the declared temporary cache.
- `fetch_video.py --retrieve-video` returns timestamped excerpts from that cache by validated video ID.
- The agent applies this file and `references/output-modes.md` to create the semantic notes.

## When to Use

Invoke when the user:

- provides a YouTube URL or video ID and asks to summarize, analyze, or understand it;
- pastes or uploads a transcript and asks for video notes;
- asks a follow-up question about a previously fetched video;
- wants to compare several videos or decide which one deserves deeper attention;
- asks to verify important claims made in a video.

A bare YouTube URL is enough only when the message is clearly asking the assistant to process that video. Do not activate when a link is merely cited, shared as a reference, requested for playback or download, or included as one source inside an unrelated task.

Do not invoke for:

- downloading the video or audio;
- bypassing login, age, geographic, paywall, or access controls;
- summarizing a video that has neither accessible subtitles nor a user-supplied transcript;
- publishing derived content without an explicit request.

## Output Language

Respond in the language of the user's current request. If unclear, ask once. Preserve quotations in their original language and add a translation only when useful.

Bundled scripts emit machine-readable JSON, status codes, and transcript text rather than a localized natural-language interface. Explain their results in the language of the user's current request.

## Select the Mode

| Request signal | Mode | Default output |
|---|---|---|
| Bare link, “总结”, “讲了什么”, “值不值得看” | Quick | One-screen decision card |
| “深读”, “完整笔记”, “论证过程”, “详细整理” | Deep | Timestamped structured notes |
| “核验”, “查证”, “research”, “是真的吗” | Research | Deep notes plus selected claim verification |
| Two or more links | Batch Quick | One Quick card per video |
| “决策卡”, “一张图看懂”, “结构化卡片”, 批量沉淀/建站 | Decision Card | One structured PNG per video (see templates/decision-card) |

If the requested depth is ambiguous, use Quick as the content mode. Still follow host confirmation requirements for package installation, file creation, and every other state-changing action.

## Step 1: Check the Environment

Run the read-only doctor before the first URL fetch in a session:

```bash
python3 <skill_dir>/scripts/fetch_video.py --doctor
```

Add `--network` only when a network diagnosis is needed. If a local proxy should be tested, pass its loopback port explicitly with `--proxy-port`; Doctor does not scan local ports. Doctor never installs packages or changes configuration.

If the pinned dependency is missing, show the exact repair command:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r <skill_dir>/requirements.lock
```

Do not install anything without explicit user approval.

## Step 2: Get a Transcript

### YouTube URL or video ID

Run:

```bash
python3 <skill_dir>/scripts/fetch_video.py "<youtube-url>"
```

For a local proxy, pass only the loopback port:

```bash
python3 <skill_dir>/scripts/fetch_video.py "<youtube-url>" --proxy-port 7890
```

The script:

- validates YouTube hosts and video IDs;
- calls the pinned `yt-dlp` Python API directly;
- never invokes a shell or external executable;
- accepts only a loopback proxy port and no proxy credentials;
- writes `meta.json` and `transcript.txt` to a private per-user cache under the system temporary directory;
- prints the cache directory as JSON.

The cache hierarchy must be owned by the current user with `0700` directory permissions. Cache files use atomic replacement, `0600` permissions, and reject symbolic links. Temporary cache is not a durable archive. Create a user-visible note file only when the user explicitly requests one.

### Cookie mode (bot check fix)

Shared/data-center egress IPs trigger YouTube's bot check ("Sign in to confirm
you're not a bot") on the player/caption endpoints, while playlist listing still
works. When a fetch fails that way, retry in cookie mode — **only after the user
has explicitly agreed to use their YouTube login**:

```bash
python3 <skill_dir>/scripts/fetch_video.py "<youtube-url>" --cookies chrome
# or with an exported cookies.txt:
python3 <skill_dir>/scripts/fetch_video.py "<youtube-url>" --cookies /path/to/cookies.txt
```

One-time setup (already done on this machine):

```bash
.venv/bin/pip install yt-dlp-ejs bgutil-ytdlp-pot-provider
# bgutil POT provider script (generates the PO Token YouTube requires):
git clone --depth 1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git vendor/bgutil
cd vendor/bgutil/server && npm install && npx tsc   # produces build/generate_once.js
```

Requirements and behavior:

- `--cookies chrome` reads Chrome cookies directly; **Chrome must be fully quit
  (Cmd+Q)** or the cookie database is locked. A keychain prompt may appear — user
  clicks Allow.
- Cookie mode forces `player_client=web` (overridable via `--player-client`),
  wires the bundled yt-dlp-ejs solver (needs `node` in PATH) and the bgutil
  POT script; `ignore_no_formats_error` is enabled so caption-only fetches
  succeed even when video formats are unavailable.
- `ios`/`android` clients ignore cookies; `tv` needs none but is bot-checked on
  these IPs — keep the default `web`.
- Use sparingly (batches of ~10), the fetch runs under the user's logged-in
  identity. Never log, copy, or transmit cookie contents.

### Supplied transcript

If the user provides transcript text or a transcript file, skip YouTube fetching. Treat it as `User-provided transcript` and preserve any timestamps already present.

### No subtitles or failed fetch

Do not stop at “unsupported.” Offer the smallest viable fallback:

1. Ask the user to paste or upload a transcript.
2. If the user already supplied an audio/video file, use an available transcription capability only with the user's request.
3. If neither is available, explain the exact limitation without inventing content.

## Step 3: Produce the Requested Output

Follow `references/output-modes.md`.

### Quick

Keep it to one screen:

- title, channel, duration, and source link;
- 2–3 sentence summary;
- five timestamped takeaways;
- one “worth watching if…” judgment;
- important uncertainty or missing context.

### Deep

Include:

- concise overview;
- timestamped structure;
- argument map: claim → reasoning → evidence → limitation;
- `Video statement` and `Author opinion` as separate labels;
- notable quotations;
- unanswered questions and useful follow-ups.

Do not call a statement a verified fact merely because it appears in the video.

### Research

Start from Deep, then verify only material claims that affect the conclusion.

- Prefer primary sources, official documentation, papers, or original datasets.
- Attach each verification result to the corresponding video timestamp.
- Label each claim `Supported`, `Partly supported`, `Contradicted`, or `Not verified`.
- State source date and scope.
- Do not perform broad web research when the user only asked for a summary.

### Batch Quick

For each video provide:

- one-sentence thesis;
- three key timestamps;
- evidence quality;
- novelty;
- recommendation: Deep now / Save / Skip.

Compare videos only on common dimensions.

### Decision Card（结构化决策卡，输出升级层）

在 Quick/Deep 之上的可选输出：1 视频 = 1 张图 = 4 区块——讲了什么 / 解决什么问题 / 适用范围 / 漏洞与偏见。定位是「决定看不看」的决策层，适合批量沉淀和内容分发。

- 模板与数据格式见 `templates/decision-card/`（card.html + README.md）。
- 数据文件 `struct-data.js`：每个视频一条 `STRUCT` 记录（title/what/problem/scope/caveat）。
- `caveat` 必须写该视频真实的局限（样本、立场、时效、幸存者偏差），禁止套话。
- 渲染：本地 http 服务 + WebKit headless，按 README 的 boundingBox+clip 方式逐张截图。
- 批量场景（如视频站每周更新）：新视频先出 Quick 笔记，高价值条目再升级决策卡。

## Follow-up Retrieval

The retrieval script accepts a video ID, never an arbitrary file path:

```bash
python3 <skill_dir>/scripts/fetch_video.py --retrieve-video <video-id> --keyword "attention"
python3 <skill_dir>/scripts/fetch_video.py --retrieve-video <video-id> --at 3:20
python3 <skill_dir>/scripts/fetch_video.py --retrieve-video <video-id> --list
```

It reads only transcripts created under the managed temporary cache. Quote the relevant timestamp range in the answer.

## Content Integrity

- Preserve what the source actually says; remove filler, not substance.
- Separate a video's claims from external verification.
- Keep numbers, dates, named entities, caveats, and uncertainty.
- Trust visible slide text over an obvious transcription error when the user supplies frames or screenshots.
- Do not attribute a claim to a speaker unless the source supports the attribution.
- Do not turn the summary into promotional copy unless explicitly requested.

## Completion Standard

- The selected mode matches the request.
- Every major point can be traced to a timestamp or labeled transcript section.
- Claims and opinions remain separate.
- Research mode includes source-backed verification and scope.
- Fetch failures produce a usable transcript fallback.
- No package installation, durable file write, publishing, or external state change occurs without explicit approval.
