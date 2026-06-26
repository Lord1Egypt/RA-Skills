---
name: slide-to-video-converter
description: "End-to-end pipeline for converting PPT/PPTX/PDF slides with speaker notes into narrated MP4 videos. Defaults to Edge TTS (Microsoft free online API) for universal compatibility. Supports three TTS modes: Edge TTS (default), Qwen3-TTS (local GPU acceleration), and HTTP service. Features audio validation, auto-synced subtitles, batch processing, and PPTX support via LibreOffice conversion. Input: PPT/PPTX/PDF file + JSON subtitles. Output: High-quality MP4 video with narration and subtitles. Use when users want to: (1) Automate video creation from presentations, (2) Generate training/lecture videos with TTS, (3) Batch produce slide-based content, (4) Create videos with consistent quality control, (5) Convert PPTX files to video."
---

# Slide to Video Converter

Complete end-to-end pipeline for converting PPT/PPTX/PDF slides with speaker notes into high-quality narrated MP4 videos with auto-synced subtitles.

## Architecture

### 3-Stage Pipeline with Audio Validation

```
Stage 1: Audio Generation & Validation
┌─────────────────────────────────────────────────────────┐
│ PPTX/PDF → Images (png)                                 │
│ Script → TTS → Audio → STT Validation → Validated Audio│
└─────────────────────────────────────────────────────────┘

Stage 2: Per-Slide Video Composition
┌─────────────────────────────────────────────────────────┐
│ Image + Validated Audio + Subtitle → Individual MP4      │
└─────────────────────────────────────────────────────────┘

Stage 3: Final Video Assembly
┌─────────────────────────────────────────────────────────┐
│ Merge All Slide Videos → final.mp4                      │
└─────────────────────────────────────────────────────────┘
```

### TTS Mode Support
- **Edge TTS (Default)**: Free online API, no local model required
- **Qwen3-TTS**: Local GPU acceleration (Apple Silicon)
- **HTTP Service**: Independent TTS server for multi-client usage

### PPTX Support
- **PPTX → PDF → PNG**: Optimized conversion path using LibreOffice for best quality
- **Fallback Method**: Python-pptx based conversion when LibreOffice not available
- **Auto-detection**: Automatically uses PPTX if PDF not available

## Workflow

### Step 1: Prepare Inputs

Require two inputs from the user:

1. **Slide file**: PPT/PPTX or PDF. Supports automatic PPTX conversion:
   - **PPTX**: Uses LibreOffice for high-quality conversion (recommended)
   - **PDF**: Direct conversion using pdf2image
   - **Auto-detection**: Automatically uses PPTX if PDF not available

2. **Speaker notes**: A JSON file with per-page narration. See [references/script-format.md](references/script-format.md) for the expected format.

### Step 2: Install Dependencies

```bash
# System dependencies
brew install poppler ffmpeg libreoffice   # macOS (add libreoffice for PPTX support)
# apt install poppler-utils ffmpeg libreoffice   # Linux

# Python dependencies
pip install -U mlx-audio soundfile numpy edge-tts pdf2image Pillow moviepy python-pptx

# Optional: HTTP service dependencies
pip install fastapi uvicorn python-multipart
```

### Step 3: Run Pipeline (Default: Edge TTS)

**Default Mode: Edge TTS** - Free online API (recommended for universal compatibility)
```bash
python scripts/pipeline.py
```

**PPTX Support Options:**
```bash
# Use PPTX file (if both PDF and PPTX exist)
python scripts/pipeline.py --use-pptx

# Force PPTX conversion even if PDF exists
python scripts/pipeline.py --use-pptx --force-audio

# PPTX with fallback method (no LibreOffice required)
python scripts/pipeline.py --use-pptx --fallback
```

**Alternative TTS Modes:**

**Edge TTS** - Free online API, no local model required (default)
```bash
python scripts/pipeline.py --tts-edge
```

**HTTP Service** - Independent TTS server for multi-client usage
```bash
# Start TTS server
python scripts/tts_server.py &
# Run pipeline
python scripts/pipeline.py --tts-http
```

**Qwen3-TTS** - Local GPU acceleration
```bash
python scripts/pipeline.py --tts-direct
```

### Step 4: Run Pipeline

```bash
# Full pipeline with audio validation
python scripts/pipeline.py

# Specific slides only
python scripts/pipeline.py --slides 1-5

# Fast preview mode (lower quality, quicker)
python scripts/pipeline.py --fast

# Skip image generation (use existing)
python scripts/pipeline.py --skip-images

# Force regenerate audio
python scripts/pipeline.py --force-audio

# Skip audio validation (use existing audio as-is)
python scripts/pipeline.py --skip-validation

# Custom validation threshold
python scripts/pipeline.py --threshold 0.7 --max-retries 3
```

### Step 5: Customize

Edit `config.json` to adjust:
- **Edge TTS**: voice, rate, volume
- **Video**: fps, codec
- **Image**: dpi, resolution
- **Subtitle**: font, size, color, position

## Available TTS Voices

### Edge TTS Voices (Default - Online API)
| Voice | Gender | Style |
|-------|--------|-------|
| `serena` | Female | Warm, natural (default) |
| `chelsea` | Female | Professional, clear |
| `max` | Male | Authoritative, deep |
| `brian` | Male | Friendly, energetic |

### Edge TTS Chinese Voices (Online API)
| Voice | Gender | Style |
|-------|--------|-------|
| `zh-CN-YunyangNeural` | Male | Professional news anchor (default) |
| `zh-CN-XiaoxiaoNeural` | Female | Warm, natural |
| `zh-CN-YunjianNeural` | Male | Energetic sports |
| `zh-CN-XiaoyiNeural` | Female | Lively cartoon |
| `zh-CN-YunxiNeural` | Male | Sunny, cheerful |

List all Edge voices: `edge-tts --list-voices | grep zh-CN`

## Key Design Decisions

- **Three TTS Modes**: Support for Qwen3-TTS (local GPU), Edge TTS (online), and HTTP service - flexibility for different use cases
- **Audio Validation Pipeline**: STT-based quality control ensures TTS output matches original text (configurable threshold)
- **Per-Slide Processing**: Independent audio/video generation for each slide enables partial regeneration and parallel processing
- **Smart Subtitle Sync**: Text segmentation at sentence boundaries with proportional time allocation based on character count
- **Zero-Reencoding Merge**: FFmpeg concat demuxer for fast video assembly without quality loss
- **GPU Acceleration**: Apple Silicon Metal support for fast local TTS inference (~3 seconds per page)
- **Quality Control**: Multi-stage validation including duration checks, silent audio detection, and similarity scoring

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
