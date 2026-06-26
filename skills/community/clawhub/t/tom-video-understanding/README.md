# Video Understanding (Local Video Comprehension)

A skill for understanding video content using local AI models, supporting both audio transcription and image understanding.

## Model Installation

### Image Understanding - qwen3-vl:8b

**Windows:**
1. Download Ollama from https://ollama.com/download
2. Install and verify: `ollama --version`

**Pull the model:**
```bash
ollama pull qwen3-vl:8b
```

**macOS/Linux:**
```bash
brew install ollama  # or download from ollama.com
ollama pull qwen3-vl:8b
```

### Audio Recognition - FunASR

**Create conda environment:**
```bash
conda create -n asr-local python=3.11
conda activate asr-local
pip install funasr
```

**Note:** The FunASR model will be downloaded automatically on first use.

## Environment Requirements

- ffmpeg (in PATH)
- conda + Python 3.11
- Ollama (running)
- ~6GB VRAM for qwen3-vl:8b

## Directory Structure

```
video-understanding/
├── README.md          # This file (human guide)
├── SKILL.md           # AI execution guide
├── scripts/
│   └── ...            # Helper scripts if needed
└── assets/
    └── ...            # Templates/examples if needed
```

## Troubleshooting

**Ollama not running:**
```bash
ollama serve
```

**Model download slow:**
```bash
# Use a mirror if needed
OLLAMA_BASE_URL=https://example.com ollama pull qwen3-vl:8b
```

**FunASR model not found:**
- Models are auto-downloaded on first use
- Ensure internet connection for initial download

**Chinese audio not recognized:**
- FunASR Paraformer model is optimized for Chinese
- For English, consider Whisper via Ollama instead
