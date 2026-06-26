---
name: rapid-ocr-reader
version: 1.0.0
owner: rendaixue-byte
description: Extract text from images using OCR (Optical Character Recognition). Use this skill when you need to read text content from images, screenshots, photos, or any image file. Supports Chinese and English text with high accuracy. Triggers when user sends an image and asks to read/extract/identify text from it, or when you receive an image that contains text you need to understand.
license: MIT
---

# Image Reader - OCR Text Extraction

A high-performance OCR skill for extracting text from images. Powered by RapidOCR with PP-OCRv4 models, supporting Chinese and English text recognition.

## Features

- Multi-language: Chinese (simplified/traditional), English, and mixed text
- High accuracy: PP-OCRv4 model with >95% accuracy on typical screenshots
- Structured output: Text with confidence scores and bounding boxes
- Image info: Dimensions, format, and color mode included
- Fast: CPU-only, no GPU required

## Quick Start

```bash
python scripts/read_image.py /path/to/image.jpg
```

## Usage Examples

### Extract text from a screenshot

```bash
python scripts/read_image.py screenshot.png
```

### JSON Output

The script outputs structured JSON:

```json
{
  "success": true,
  "text": "Full extracted text",
  "lines": [
    {
      "text": "Individual line",
      "confidence": 0.98,
      "box": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    }
  ],
  "line_count": 5,
  "image_info": {
    "format": "PNG",
    "size": [1920, 1080],
    "mode": "RGB"
  }
}
```

## Requirements

```bash
pip install rapidocr onnxruntime pillow
```

First run will download OCR models (~50MB) automatically.

## Common Use Cases

- UI Screenshots: Extract text from app/website screenshots
- Document Photos: Read text from photographed documents
- Diagrams: Extract labels and annotations
- Receipts: Parse receipt/invoice data

## Output Fields

| Field | Type | Description |
|-------|------|-------------|
| success | bool | Whether OCR succeeded |
| text | string | All extracted text |
| lines | array | Individual text lines with metadata |
| line_count | int | Number of text lines detected |
| image_info | object | Image metadata |

## Technical Details

- Engine: RapidOCR (ONNX Runtime backend)
- Models: PP-OCRv4 (detection + recognition)
- Languages: Chinese, English (auto-detected)
- Performance: ~1-2 seconds per image on CPU

## License

MIT License

Third-party dependencies:
- RapidOCR - Apache 2.0 License
- ONNX Runtime - MIT License
