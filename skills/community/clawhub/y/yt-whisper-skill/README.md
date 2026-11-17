# yt-whisper-skill

An [OpenClaw](https://docs.openclaw.ai/) **skill** that transcribes YouTube videos locally with
Whisper (CUDA) and archives clean, URL/title-headed transcript files. It also turns a transcript (or
any input document) into a structured **AI summary** and a compact **research plan**.

Everything needed ships in this repository: the skill instructions (`SKILL.md`), the scripts, and a
one-shot installer that builds the local virtual environment.

## Features

- Download YouTube audio and transcribe with Whisper on CUDA
- Auto model selection (faster model for long videos)
- Respects `t=` / `start=` / `end=` timestamps in YouTube URLs
- Category inference from the title, or forced with `--category`
- Single URL, multiple URLs, or bare 11-char video IDs
- Optional language detection / forced language
- Temp media cleanup after each run
- Produces `*_AISUMMARY.md` (structured report) and `*_AISEARCHPLAN.md` (deep-research brief)

## Install

```bash
git clone https://github.com/<owner>/yt-whisper-skill.git
cd yt-whisper-skill
bash scripts/install.sh
```

`install.sh`:
1. checks `ffmpeg` and `python3`,
2. creates the local virtual environment at `./.venv` and installs `yt-dlp` + `openai-whisper`,
3. copies the runner to `~/.local/bin/yt-transcribe` and to `~/Transcriptions/Scripts/`,
4. reports whether a JavaScript runtime (`node`/`deno`/`bun`/`quickjs`) is available.

To use it as an OpenClaw skill, symlink the repository into your skills root:

```bash
ln -sfn "$PWD" ~/.openclaw/skills/yt-whisper-skill
```

## Usage

```bash
bash scripts/yt-transcribe.sh "https://youtu.be/VIDEO_ID"
bash scripts/yt-transcribe.sh "https://youtu.be/ID1" "https://youtu.be/ID2"
bash scripts/yt-transcribe.sh "https://youtu.be/VIDEO_ID" --language it
bash scripts/yt-transcribe.sh "https://youtu.be/VIDEO_ID" --category Philosophy
```

Output: `~/Transcriptions/<Category>/<safe_title>_<video_id>.txt`

## Requirements

- `ffmpeg`
- `python3` (used to build the venv)
- a JavaScript runtime for `yt-dlp` (`node`, `deno`, `bun` or `quickjs`)
  - missing runtime => yt-dlp fails with `HTTP Error 403: Forbidden` (not a YouTube block)

## Repository layout

```
yt-whisper-skill/
├── SKILL.md            # skill definition + agent operating rules
├── README.md           # this file
├── LICENSE             # MIT
├── CHANGELOG.md
├── .gitignore
├── .env.template       # optional runtime configuration (no secrets)
├── AGENTS.md           # guidance for coding agents working on this repo
├── scripts/
│   ├── install.sh      # one-shot setup (venv + deps + PATH copy)
│   └── yt-transcribe.sh# the runner
├── examples/           # real demo: transcript of a 19s video (see examples/README.md)
└── .venv/              # local toolchain (gitignored)
```

## Configuration

Optional, via environment variables (see `.env.template`). No secret is required by this skill;
tokens for other tooling live in a secrets store outside the repo and are never committed.

## Security

- No secrets in the repository. `.env*` is gitignored except `.env.template`.
- Transcripts are written under `~/Transcriptions/`, never inside the repo.

## License

MIT — see [LICENSE](LICENSE).
