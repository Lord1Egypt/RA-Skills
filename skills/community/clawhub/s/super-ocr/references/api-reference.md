# API Reference for Super OCR

This document provides complete API documentation for using Super OCR as a Python library.

## Quick Start

```python
from super_ocr import OCRProcessor

# Auto mode (recommended)
processor = OCRProcessor(engine='auto')
result = processor.extract('image.png')

print(result['text'])
print(f"Confidence: {result['confidence']:.2%}")
print(f"Engine: {result['engine']}")
```

## OCRProcessor Class

### `__init__(engine: str = 'auto', verbose: bool = False)`

Initialize the OCR processor.

**Parameters:**
- `engine` (str): 'auto', 'tesseract', or 'paddle'. Default: 'auto'
- `verbose` (bool): Enable detailed logging. Default: False

### `extract(image_path: str) -> Dict`

Extract text from a single image.

**Parameters:**
- `image_path` (str): Path to the input image

**Returns:**
```python
{
    'text': str,                    # Extracted text
    'confidence': float,           # Confidence score (0.0 - 1.0)
    'engine': str,                 # 'tesseract' or 'paddle'
    'processing_time_ms': float,   # Processing time in milliseconds
    'error': Optional[str],        # Error message if failed
    'results': List[Dict],         # Detailed results (PaddleOCR only)
    'line_count': int              # Number of lines detected
}
```

### `batch_extract(image_paths: List[str]) -> List[Dict]`

Process multiple images.

**Parameters:**
- `image_paths` (List[str]): List of image file paths

**Returns:**
- List of result dictionaries (same structure as `extract()`)

## Engine Selection

### Auto Mode (Default)

The processor automatically selects the best engine based on:

1. **Image filename heuristics:**
   - `screenshot`, `snap`, `capture` → Tesseract
   - `menu`, `invoice`, `certificate`, `receipt` → PaddleOCR
   - Default → PaddleOCR (better accuracy)

2. **Quality fallback:**
   - If Tesseract returns low confidence, PaddleOCR is used

### Force Mode

You can explicitly choose an engine:

```python
# Force Tesseract
processor = OCRProcessor(engine='tesseract')

# Force PaddleOCR
processor = OCRProcessor(engine='paddle')
```

## Preprocessing

For advanced users, you can preprocess images before OCR:

```python
from super_ocr.preprocessing import preprocess_pipeline

# Load image
import cv2
image = cv2.imread('input.png')

# Preprocess
processed = preprocess_pipeline(
    image,
    denoise=True,
    enhance=True,
    binarize=True,
    deskew=True,
    resize_scale=2.0
)

# Save processed image
cv2.imwrite('processed.png', processed)
```

## Output Formats

The skill supports multiple output formats:

| Format | Description |
|--------|-------------|
| `text` | Clean extracted text only |
| `json` | Full JSON with metadata |
| `structured` | Human-readable formatted output |
| `verbose` | Debug information with confidence scores |

## Configuration

You can customize behavior by creating a `config.yaml`:

```yaml
default_engine: auto
confidence_threshold: 0.8
output_format: json
preprocess:
  denoise: true
  enhance_contrast: true
```

## Error Handling

```python
try:
    result = processor.extract('image.png')
    
    if result.get('error'):
        print(f"Error: {result['error']}")
    else:
        print(result['text'])
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## CLI Usage

```bash
# Single image
python scripts/main.py --image image.png

# Multiple images
python scripts/main.py --images ./images/*.png --output ./results

# Force engine
python scripts/main.py --image doc.png --engine paddle --verbose

# Different output format
python scripts/main.py --image img.png --format text
```