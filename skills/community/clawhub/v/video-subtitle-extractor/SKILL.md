---
name: video-subtitle-extractor
description: |
  Cross-platform video subtitle extraction using multi-engine ASR (speech-to-text). Downloads audio from video URLs via yt-dlp, transcribes with SenseVoice / whisper.cpp / openai-whisper (default: SenseVoice Small for Chinese), and applies LLM-based text calibration for Chinese financial/technical content. Use when: (1) extracting subtitles from Bilibili, Xiaohongshu, YouTube, or any yt-dlp-supported platform, (2) the video has no built-in subtitles, (3) users say "下载字幕", "提取字幕", "语音转文字", "视频转文字", "字幕提取", "ASR转写", (4) needing to transcribe audio files to text, (5) working with Chinese-language video content requiring high-accuracy transcription. Automatically handles dependency installation (ffmpeg, yt-dlp, ASR backends) and model downloads.
---

# Video Subtitle Extractor 🎬→📝

Cross-platform multi-engine ASR subtitle extraction pipeline. Downloads audio from any yt-dlp-compatible video platform, transcribes with **SenseVoice / whisper.cpp / openai-whisper**, and applies LLM-based text calibration for Chinese content.

**Default engine**: SenseVoice Small (Alibaba FunASR) — ~1.5GB RAM, 234MB disk, 20× realtime speed, ~96% Chinese accuracy.

**Tested & verified** on Windows 11 with real Bilibili & Xiaohongshu videos.

## Quick Start

```bash
# One-command full pipeline (SenseVoice Small — default, blazing fast for Chinese)
python scripts/run.py <video_url> --output-dir ./output

# Use whisper.cpp GGML (even lighter, 2GB RAM)
python scripts/run.py <video_url> --backend whispercpp --model medium-q5_1

# Use openai-whisper (standard, 5GB RAM)
python scripts/run.py <video_url> --backend openai --model medium

# Download audio only
python scripts/download_audio.py <video_url> <output_dir>

# Download audio + video (keep both as middleware)
python scripts/download_audio.py <video_url> <output_dir> --save-video --video-quality 1080

# Transcribe existing audio with auto backend selection
python scripts/transcribe.py <audio_file> --backend auto --language zh

# Transcribe with specific backend
python scripts/transcribe.py <audio_file> --backend sensevoice --language zh
python scripts/transcribe.py <audio_file> --backend whispercpp --model medium-q5_1
python scripts/transcribe.py <audio_file> --backend openai --model medium
```

## When to Use This Skill

Use this skill when:
1. The video has **no built-in subtitles** (Bilibili, Xiaohongshu, YouTube, etc.)
2. You need **high-accuracy Chinese transcription** (~95% with medium model)
3. You want **multiple output formats** (TXT, SRT, VTT, JSON)
4. You need **LLM-assisted text calibration** for financial/technical terms
5. The user says: "下载字幕", "提取字幕", "语音转文字", "视频转文字", "字幕提取", "ASR转写"

## Workflow

### Step 0: Install Dependencies (once)

```bash
python scripts/install_deps.py
```

Auto-detects OS and installs: ffmpeg (winget/brew/apt), yt-dlp (pip), openai-whisper (pip). Handles Windows ffmpeg path detection even when not in PATH.

### Step 1: Download Audio

Run `scripts/download_audio.py <url> [output_dir]`.

Uses yt-dlp to extract the best available audio format (m4a preferred). Supports Bilibili, YouTube, and 1800+ yt-dlp-compatible platforms. The script automatically detects ffmpeg even when not in system PATH.

**Optional: Download video as middleware**

Add `--save-video` to persist the full video alongside audio:

```bash
python scripts/download_audio.py <url> --save-video --video-quality 1080
python scripts/run.py <url> --save-video --video-quality 720 --calibrate
```

`--video-quality` preset table:

| Preset | yt-dlp behaviour | Typical result |
|--------|------------------|----------------|
| `best` (default) | Highest available | 4K on YouTube, 480p on B站 (no login) |
| `1080` | ≤1080p, fallback gracefully | 1080p where available |
| `720` | ≤720p | Good balance for local storage |
| `480` | ≤480p | Minimum acceptable for reference |
| `360` | ≤360p | Extremely small files |
| *raw string* | Direct yt-dlp format selector | Full flexibility |

> **⚠️ B站 note**: Without login cookies, B站 caps at 480p. 720p+ requires `--cookies-from-browser`.

**If download fails**: the video may require cookies. Try:
```bash
yt-dlp --cookies-from-browser chrome <url>
```

### Step 2: ASR Transcription (Multi-Backend)

Run `scripts/transcribe.py <audio> --backend <engine> --model <size> --language <lang>`.

Three backends, auto-selected by default (priority: SenseVoice → whisper.cpp → openai-whisper):

### 🥇 SenseVoice Small (default for Chinese)

| Property | Value |
|----------|-------|
| RAM | ~1.5GB |
| Disk | ~234MB |
| Speed | 20× realtime (CPU) |
| Chinese accuracy | ~96% 🏆 |
| Model source | ModelScope (auto-download, no VPN needed) |
| Install | `pip install funasr modelscope` |

> **Why SenseVoice?** Alibaba's FunASR engine, Chinese-optimized from the ground up. No HuggingFace download needed (uses ModelScope mirror in China). ~4× faster than openai-whisper medium on CPU, with comparable or better Chinese accuracy.

### 🥈 whisper.cpp (GGML quantized, CPU-optimized)

| Model | RAM | Disk | Speed | Quality | Best For |
|-------|-----|------|-------|---------|----------|
| `tiny-q5_1` | ~0.5GB | 32MB | fastest | low | Testing |
| `small-q5_1` | ~1GB | 466MB | fast | decent | Quick preview |
| `medium-q5_1` | ~2GB | 1.1GB | 3-5× faster than openai | **~95%** ⭐ | **Lightweight quality** |

> **Setup**: `pip install pywhispercpp` + download GGML model from huggingface.co/ggerganov/whisper.cpp → place in `~/.cache/whispercpp/`. See `--show-backends` for instructions.

### 🥉 openai-whisper (standard)

| Model | RAM | Disk | Speed | Quality | Best For |
|-------|-----|------|-------|---------|----------|
| `medium` | ~5GB | 1.42GB | ~165 fps | **~95%** | Standard |
| `large-v3` | ~10GB | 2.88GB | ~80 fps | ~97% | Best accuracy |
| `large-v3-turbo` | ~6GB | 1.6GB | ~120 fps | ~96% | Good balance |

> **Note**: `small` model removed (88-90% accuracy, superseded by SenseVoice). Use SenseVoice for light weight.

### Step 3: Rule-Based Calibration

After transcription, apply `calibrate.py` for mechanical corrections:

```bash
# Calibrate a raw .txt transcript
python scripts/calibrate.py <output_dir>/<video_title>.txt
# Output: <video_title>_calibrated.txt

# Skip traditional→simplified conversion (already simplified input)
python scripts/calibrate.py raw.txt --no-tradsimp
```

**Calibrate categories:** homophone fixes, financial terms, AI/tech company names, semiconductor/hardware terms, traditional→simplified (600+ chars).
For context-aware fixes (semantic errors, ambiguous names), use LLM review on top of rule-based output.
See `references/calibration_guide.md` for the full 80+ pattern library.

### Step 4: Deliver Results

Present the calibrated text. Always include:
- Model used (medium/large) and quality notes
- Any sections with low confidence or unclear audio
- Summary of corrections applied (counts by category)

## Intermediate Artifacts & Step-by-Step Reuse

Every pipeline stage saves its output to disk. All artifacts persist in `output_dir/` after the run — no data is lost between stages.

### Artifact Map

| Stage | Artifact | Format | Filename pattern | Reusable alone? |
|-------|----------|--------|------------------|-----------------|
| Step 1 | Audio | `.m4a` | `<video_title>.m4a` | ✅ `download_audio.py` |
| Step 1 | Video (optional) | `.mp4` | `<video_title>.mp4` | ✅ `download_audio.py --save-video` |
| Step 2 | Transcript (raw) | `.txt` `.srt` `.vtt` `.json` | `<video_title>.txt` | ✅ `transcribe.py` |
| Step 2 | Pipeline metadata | `.json` | `_pipeline_meta.json` | ✅ (reference only) |
| Step 3 | Transcript (calibrated) | `_calibrated.txt` | `<title>_calibrated.txt` | ✅ `calibrate.py` |

### Selective Reuse via `run.py` Flags

```bash
# Full pipeline (download + transcribe + calibrate)
python scripts/run.py <url> --calibrate --output-dir ./out

# Save video as middleware (downloads .m4a + .mp4)
python scripts/run.py <url> --save-video --calibrate --output-dir ./out

# Audio already exists → skip download, re-transcribe
python scripts/run.py <url> --skip-download --output-dir ./out

# Audio + transcript already exist → skip both, re-run calibration only
python scripts/run.py <url> --skip-download --skip-transcribe --calibrate --output-dir ./out
```

`run.py` auto-detects existing artifacts by matching the audio filename base. It will warn and fall back to downloading/transcribing if no match is found.

### Standalone Scripts

Each stage has an independent entry point:

```bash
# Stage 1: Download audio only
python scripts/download_audio.py <url> [output_dir] [filename]

# Stage 1: Download audio + video at 720p (standalone)
python scripts/download_audio.py <url> [output_dir] --save-video --video-quality 720

# Stage 2: Transcribe existing audio
python scripts/transcribe.py <audio.m4a> --model medium --language zh --output-dir ./out

# Stage 3: Calibrate raw transcript (rule-based only)
python scripts/calibrate.py <raw.txt> [--output <path>] [--no-tradsimp]
```

### Typical Reuse Scenarios

**Scenario A — Change model, keep audio**
```bash
# Already have .m4a from previous run
python scripts/run.py <url> --skip-download --model large-v3 --output-dir ./out
```

**Scenario B — Change language, keep audio + transcript**
```bash
# Have both .m4a and .txt; just recalibrate
python scripts/run.py <url> --skip-download --skip-transcribe --calibrate --language en --output-dir ./out
```

**Scenario C — Batch calibrate multiple transcripts**
```bash
# Apply calibration to all raw .txt files in a directory
Get-ChildItem .\out\*.txt | Where-Object { $_.Name -notmatch '_calibrated' } | ForEach-Object {
    python scripts/calibrate.py $_.FullName
}
```

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Bilibili | ✅ | Audio-only streams available without login. 720P+ video needs cookies. |
| Xiaohongshu | ✅ | Full support via `XiaoHongShu` extractor. Short links (xhslink.com) auto-resolved. No cookies needed. |
| YouTube | ✅ | Full support. Cookies may improve format selection. |
| Douyin/TikTok | ⚠️ | Requires login cookies (`--cookies-from-browser` or `--cookies cookies.txt`). No cookies = download fails. |
| All yt-dlp sites | ✅ | 1800+ supported platforms |

## Extending with New ASR Models

`scripts/transcribe.py` is designed for backend extensibility:

1. Add model info to `ALL_MODELS` dict
2. Implement `transcribe_<backend>()` function
3. Add CLI flag in argparse
4. Add backend to `detect_backends()`

**Available backends**: sensevoice (✅ production), whispercpp (✅ code ready, GGML model manual), openai (✅ production)

**Backend auto-selection**: When `--backend auto` (default), the engine picks the best available backend in priority order:
1. **SenseVoice** — Chinese-optimized, fastest, lightest
2. **whisper.cpp** — CPU-optimized, quantized models
3. **openai-whisper** — general purpose, most compatible

## Troubleshooting

| Problem | Solution |
|---------|----------|
| SIGKILL / ffmpeg FileNotFoundError | ffmpeg not in PATH. Script auto-detects 7 common install locations (winget, scoop, chocolatey, manual). If ffmpeg is elsewhere, add its directory to system PATH. |
| yt-dlp download fails | Update yt-dlp: `pip install -U yt-dlp`. Try with cookies. |
| "No subtitles found" | Expected. This skill uses ASR, not built-in captions. |
| ffmpeg not found | Run `install_deps.py` (handles Windows non-PATH detection). |
| GPU not utilized | openai-whisper CPU-only by default. SenseVoice also runs on CPU. whisper.cpp uses AVX/SSE SIMD on CPU. |
| `funasr` import error | `pip install funasr modelscope` — SenseVoice backend dependency. |
| `pywhispercpp` import error | `pip install pywhispercpp` — whisper.cpp backend dependency. |
| GGML model not found | Download from huggingface.co/ggerganov/whisper.cpp → place in `~/.cache/whispercpp/`. Or use `--backend sensevoice` instead. |
| WDAC/AppLocker blocks torch DLL | Use `pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu` (CPU-only, signed). Also: `pip install numpy==2.0.2`. |
| HuggingFace blocked (China) | SenseVoice uses ModelScope (no VPN needed). For whisper.cpp GGML, use a VPN to download models once. |

## Performance Benchmarks (Tested)

| Video Duration | Model | Backend | Time | RAM Peak | Accuracy |
|---------------|-------|---------|------|----------|----------|
| 7m 49s (Bilibili) | SenseVoice Small | sensevoice | ~20s | ~1.5GB | **~96%** 🏆 |
| 9m 30s (Bilibili) | medium-q5_1 | whispercpp | ~2m | ~2GB | ~95% |
| 9m 30s (Bilibili) | medium | openai | ~4m | ~5GB | ~95% |
| 23m (Bilibili) | SenseVoice Small | sensevoice | ~60s | ~1.5GB | **~96%** 🏆 |
| 23m (Bilibili) | medium | openai | ~12m | ~5GB | ~95% |

Tested on Windows 11, Intel i7, 16GB RAM. Performance may vary by CPU speed.

## Changelog

### v2.0.0 — Multi-Engine ASR
- **New**: SenseVoice Small backend (Alibaba FunASR) — default engine, ~1.5GB RAM, 20× realtime, ~96% Chinese accuracy
- **New**: whisper.cpp GGML backend via pywhispercpp — CPU-optimized quantized models (0.5-2GB RAM)
- **New**: `--backend` parameter (`auto`/`sensevoice`/`whispercpp`/`openai`)
- **New**: `transcribe.py --show-backends` diagnostic command
- **New**: Auto-backend detection and fallback chain (SenseVoice → whisper.cpp → openai-whisper)
- **Remove**: `small` model from openai-whisper (superseded by SenseVoice)
- **Remove**: faster-whisper stub (CTranslate2 — WDAC incompatibility, never actually worked)
- **Improve**: transcriber architecture — clean backend dispatch, shared output writer
- **Improve**: Chinese-optimized default path (SenseVoice Small via ModelScope, no VPN needed)

### v1.0.8
- **New**: Semiconductor / hardware domain calibration rules (30+ patterns) — 韬定律→道定律, 全站协同→全栈协同, 量子碎穿→量子隧穿, 吸片→芯片, 奈米→纳米, etc.
- **Improve**: Huawei 道定律 video now correctly calibrated (0→26 pattern corrections, ~98% accuracy)
- **Fix**: Douyin/TikTok platform note — clearly states cookies requirement

### v1.0.7
- **New**: `--video-quality` parameter — presets best/2160/1440/1080/720/480/360 + raw yt-dlp format support
- **New**: `find_artifacts_in_dir()` replaces `find_audio_in_dir()` — caches both .m4a AND .mp4 on `--skip-download --save-video`
- **Change**: Video download format selector now uses `height<=` filters (graceful fallback) instead of hardcoded mp4-only
- **Improve**: `download_video()` now reports which quality preset is in use
- **Improve**: Artifact map includes video (.mp4) with quality column
- **Improve**: SKILL.md adds `--video-quality` usage table and B站 login caveats

### v1.0.6
- **New**: `--save-video` flag — download and persist full video (.mp4) alongside audio
- **New**: `download_video()` function in download_audio.py (standalone: `--save-video`)
- **Improve**: Artifact map now includes video (.mp4) as first-class middleware
- **Improve**: `_pipeline_meta.json` includes `video_path` for full traceability

### v1.0.5
- **Remove**: `small` model from all backends (88-90% accuracy, too poor for production)
- **Change**: Default model locked to `medium` (was medium in code, but docs still promoted small)
- **Improve**: Model table and benchmarks now medium-only baseline

### v1.0.2
- **New**: Xiaohongshu (小红书) platform support — yt-dlp `XiaoHongShu` extractor
- **New**: Short link auto-resolution (xhslink.com → full URL via redirect)
- **Improve**: Platform support table now lists 小红书 explicitly
- **Improve**: Quick Start examples include xhslink.com usage

### v1.0.1
- **Fix**: Expanded ffmpeg search paths from 3→7 (winget/scoop/chocolatey/ProgramFiles(x86))
- **Fix**: `ensure_deps()` now injects ffmpeg into `os.environ['PATH']` on success
- **Fix**: SIGKILL troubleshooting updated — root cause is ffmpeg PATH, not OOM
- **Improve**: Auto-detect GPU (`torch.cuda.is_available()`) for fp16 support
- **Improve**: `verbose=True` for real-time transcription progress visibility
- **Improve**: More accurate error messages in dependency checks

### v1.0.0
- Initial release: download (yt-dlp) + transcribe (whisper) + calibrate (LLM) pipeline
- 7 ffmpeg install path auto-detection
- Multi-format output (TXT, SRT, VTT, JSON)
- Platform support: Bilibili, YouTube, all yt-dlp sites