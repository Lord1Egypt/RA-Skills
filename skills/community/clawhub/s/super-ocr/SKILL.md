---
name: super-ocr
description: "Production-grade OCR with intelligent engine selection. Tesseract (lightweight, fast) and PaddleOCR (high accuracy, Chinese-optimized). Use when extracting text from images, processing Chinese documents, needing confidence scores, or working with mixed Chinese/English content."
---

# Super OCR

## Overview

Super OCR is a production-grade optical character recognition tool that intelligently selects the best engine for your needs:

- **Tesseract Engine**: Lightweight, fast (~200-500ms), perfect for simple text extraction
- **PaddleOCR Engine**: High accuracy (98%+), optimized for Chinese, ideal for complex documents

## Engine Selection Strategy

### Auto Mode (Default)
The skill automatically selects the optimal engine:

| Scenario | Selected Engine | Why |
|----------|----------------|-----|
| Simple text, English only | Tesseract | Faster, lighter dependency |
| Chinese content, high accuracy needed | PaddleOCR | Better Chinese support, 98%+ accuracy |
| Low confidence from Tesseract | PaddleOCR (fallback) | Quality assurance |

### Force Mode
Users can explicitly choose an engine:
- `--engine tesseract` - Use Tesseract only
- `--engine paddle` - Use PaddleOCR only
- `--engine auto` - Auto-select (default)

## Quick Start

### Installation

This skill requires the following dependencies:
- **PaddleOCR** (for Chinese text recognition - 98%+ accuracy)
- **Tesseract** (for fast English text recognition)
- **OpenCV** (for image preprocessing)

#### Option 1: Install with pip (all-in-one)
```bash
pip install paddleocr paddlepaddle pytesseract pillow opencv-python numpy
```

#### Option 2: Install dependencies manually

**macOS:**
```bash
# Tesseract
brew install tesseract

# PaddleOCR
pip install paddleocr paddlepaddle
```

**Ubuntu/Debian:**
```bash
# Tesseract
sudo apt update && sudo apt install tesseract-ocr

# PaddleOCR
pip install paddleocr paddlepaddle
```

**Windows:**
```bash
# Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
pip install paddleocr paddlepaddle pytesseract pillow opencv-python numpy
```

### Usage

```bash
# Auto mode (recommended) - runs all available engines
cd path/to/super-ocr
python scripts/main.py --image path/to/image.png

# Force Tesseract only
python scripts/main.py --image document.jpg --engine tesseract

# Force PaddleOCR (high accuracy Chinese)
python scripts/main.py --image chinese_menu.png --engine paddle

# Run all engines (macOS only: Tesseract + PaddleOCR + MacVision)
python scripts/main.py --image complex_doc.png --engine all

# Batch processing with output directory
python scripts/main.py --images ./images/*.png --output ./results --verbose

# Check dependencies and auto-install
python scripts/dependencies.py --check --install
```

## Structuring This Skill

This skill uses a **capabilities-based** structure with multiple execution modes:

1. **Engine Selection Logic** - Intelligent decision making
2. **OCR Execution** - Unified interface for different engines
3. **Post-processing** - Standardized output formatting
4. **Validation & Fallback** - Quality assurance

## Core Capabilities

### 1. Intelligent Engine Selection

The skill includes a decision tree that analyzes:

- Image characteristics (contrast, text size)
- Language patterns (Chinese character detection)
- User requirements (speed vs accuracy)

See `scripts/engine_selector.py` for implementation details.

### 2. Dual Engine Support

**Tesseract Engine** (`scripts/tesseract_ocr.py`):
- Fast preprocessing pipeline
- PSM mode 6 for uniform text blocks
- Confidence scoring per word
- Language detection

**PaddleOCR Engine** (`scripts/paddle_ocr.py`):
- State-of-art? SN (East text detection)
- Crnn recognition with LSTM
- Confidence scores per character
- Table detection support

### 3. Output Formats

Supports multiple output formats:

| Format | Content | Use Case |
|--------|---------|----------|
| Text only | Clean extracted text | Simple search/grep |
| Structured | Text + positions | Data extraction |
| JSON | Full metadata + confidence | API integration |
| Verbose | Debug info | Quality assurance |

### 4. Quality Guarantees

- Confidence thresholds (configurable, default 80%)
- Low-confidence alerts for manual review
- \Fallback processing for failed OCRs

## Resources

### scripts/

- `main.py` - Main entry point, CLI interface (supports multi-engine)
- `dependencies.py` - Auto-install and validation
- `output_formatter.py` - Multiple output format support
- `engine/` - OCR engine implementations
  - `selector.py` - Intelligent engine selection logic
  - `tesseract.py` - Tesseract engine wrapper
  - `paddle.py` - PaddleOCR engine wrapper
  - `macvision.py` - macOS Vision OCR (macOS only)
- `preprocessing/` - Image preprocessing utilities
  - `preprocessor.py` - Denoising, enhancement, binarization

### dependencies.py (Key Feature)

The `dependencies.py` module handles:

- Dependency detection (`paddleocr`, `paddlepaddle`, `pytesseract`, `cv2`)
- Auto-install on missing dependencies
- version checking
- OS-specific installation commands
- Clear error messages with troubleshooting steps

Use this when setting up a new environment with `python scripts/dependencies.py --check --install`

## Advanced Features

### Custom Configuration

Create `config.yaml` for persistent settings:

```yaml
default_engine: auto
confidence_threshold: 0.8
output_format: json
preprocess:
  denoise: true
  enhance_contrast: true
```

### Batch Processing

Process multiple images:

```bash
python scripts/ocr.py --images ./images/*.png --output ./results
```

### API Mode

Use as a Python library:

```python
from super_ocr import OCRProcessor

processor = OCRProcessor(engine='auto')
result = processor.extract('image.png')
print(result.text)
print(result.confidence)
```

## Anti-Patterns

- ❌ Using PaddleOCR for every image (overhead for simple cases)
- ❌ ignoring confidence scores (quality matters)
- ❌ Biases (always prefering one engine)
- ❌ Skipping preprocessing (quality impact)

## Performance Notes

| Engine | Init Time | Per-Image | Memory | Best For |
|--------|-----------|-----------|----------|----------|
| Tesseract | ~200ms | ~50ms | ~100MB | Quick extraction |
| PaddleOCR | ~3s | ~500ms | ~500MB | High accuracy |

Initialize once, reuse processor for batch processing.