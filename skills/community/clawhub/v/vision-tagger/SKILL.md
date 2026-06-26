---
name: vision-tagger
description: Tag and annotate images using Apple Vision framework (macOS only). Detects faces, bodies, hands, text (OCR), barcodes, objects, scene labels, and saliency regions. Use for image analysis, photo tagging, posture monitoring, or any task requiring computer vision on images.
homepage: https://clawhub.ai/skills/vision-tagger
metadata: {"clawdbot":{"emoji":"👁️","requires":{"os":"macos","bins":["swiftc","python3"]},"install":[{"id":"xcode","kind":"shell","command":"xcode-select --install","label":"Install Xcode CLI tools"},{"id":"pillow","kind":"shell","command":"pip3 install Pillow","label":"Install Pillow"}]}}
---

# Vision Tagger

macOS-native image analysis using Apple's Vision framework. All processing is local — no cloud APIs, no API keys needed.

## Requirements

- macOS 12+ (Monterey or later)
- Xcode Command Line Tools
- Python 3 with Pillow

## Setup (one-time)

```bash
# Install Xcode CLI tools if needed
xcode-select --install

# Install Pillow
pip3 install Pillow

# Compile the Swift binary
cd scripts/
swiftc -O -o image_tagger image_tagger.swift
```

## Usage

### Analyze image → JSON

```bash
./scripts/image_tagger /path/to/photo.jpg
```

Output includes:
- `faces` — bounding boxes, roll/yaw/pitch, landmarks (eyes, nose, mouth)
- `bodies` — 18 skeleton joints with confidence scores
- `hands` — 21 joints per hand (left/right)
- `text` — OCR results with bounding boxes
- `labels` — scene classification (desk, outdoor, clothing, etc.)
- `barcodes` — QR codes, UPC, etc.
- `saliency` — attention and objectness regions

### Annotate image with boxes

```bash
python3 scripts/annotate_image.py photo.jpg output.jpg
```

Draws colored boxes:
- 🟢 Green: faces
- 🟠 Orange: body skeleton
- 🟣 Magenta: hands
- 🔵 Cyan: text regions
- 🟡 Yellow: rectangles/objects
- Scene labels at bottom

### Python integration

```python
import subprocess, json

def analyze(path):
    r = subprocess.run(['./scripts/image_tagger', path], capture_output=True, text=True)
    return json.loads(r.stdout[r.stdout.find('{'):])

tags = analyze('photo.jpg')
print(tags['labels'])  # [{'label': 'desk', 'confidence': 0.85}, ...]
print(tags['faces'])   # [{'bbox': {...}, 'confidence': 0.99, 'yaw': 5.2}]
```

## Example JSON Output

```json
{
  "dimensions": {"width": 1920, "height": 1080},
  "faces": [{"bbox": {"x": 0.3, "y": 0.4, "width": 0.15, "height": 0.2}, "confidence": 0.99, "roll": -2, "yaw": 5}],
  "bodies": [{"joints": {"head_joint": {"x": 0.5, "y": 0.7, "confidence": 0.9}, "left_shoulder": {...}}, "confidence": 1}],
  "hands": [{"chirality": "left", "joints": {"VNHLKWRI": {"x": 0.4, "y": 0.3, "confidence": 0.85}}}],
  "text": [{"text": "HELLO", "confidence": 0.95, "bbox": {...}}],
  "labels": [{"label": "outdoor", "confidence": 0.88}, {"label": "sky", "confidence": 0.75}],
  "saliency": {"attentionBased": [{"x": 0.2, "y": 0.1, "width": 0.6, "height": 0.8}]}
}
```

## Detection Capabilities

| Feature | Details |
|---------|---------|
| Faces | Bounding box, confidence, roll/yaw/pitch angles, 76-point landmarks |
| Bodies | 18 joints: head, neck, shoulders, elbows, wrists, hips, knees, ankles |
| Hands | 21 joints per hand, left/right chirality |
| Text (OCR) | Recognized text with confidence and bounding boxes |
| Labels | 1000+ scene/object categories (clothing, furniture, outdoor, etc.) |
| Barcodes | QR, UPC, EAN, Code128, PDF417, Aztec, DataMatrix |
| Saliency | Attention-based and objectness-based regions |

## Use Cases

- **Photo tagging** — Auto-tag photos with detected objects/scenes
- **Posture monitoring** — Track face/body position for ergonomics
- **Document scanning** — Extract text from images
- **Security** — Detect people in camera feeds
- **Accessibility** — Describe image contents
