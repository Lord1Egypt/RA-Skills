# CLI Reference

Use `scripts/image_helper.py` as the only entry point.

## Syntax

```bash
python scripts/image_helper.py <input> [operations] [-o output | --base64]
```

## Input Modes

- `--input-mode auto`: Prefer this default. Treat the input as a file path if it exists; otherwise try data URI or raw base64.
- `--input-mode path`: Force file-path interpretation.
- `--input-mode base64`: Force raw base64 interpretation.
- `--input-mode data-uri`: Force `data:image/...;base64,...` interpretation.

## Output Modes

- `-o output.png`: Write the processed image to a file.
- `--base64`: Print the processed image as base64.
- No transformation is required when the only goal is passthrough output, such as converting a file path directly to base64.

## Operations

### Rotate

```bash
--rotate 90
--rotate -15
--rotate 180
```

Positive angles rotate counter-clockwise.

### Crop

Use a semantic preset first:

```bash
--crop-preset center
--crop-preset bottom-right
```

Use coordinates only when the exact box is known:

```bash
--crop 100,100,500,400
```

Use percentages when coordinates are unstable but a rough region is known:

```bash
--crop-pct 25,25,50,50
```

### Scale

```bash
--scale-preset x2
--scale-preset x3
--scale 1.5
```

### Enhance

```bash
--auto-enhance
--contrast 1.5 --sharpness 2.0
--brightness 1.1 --contrast 1.3
```

`--auto-enhance` is the fastest default for OCR cleanup. Manual controls are better when the image needs a specific adjustment.

### Pipeline JSON

Use `--pipeline` when another tool or script needs to supply a sequence programmatically.

```bash
--pipeline "[{\"op\":\"crop\",\"preset\":\"center\"},{\"op\":\"scale\",\"factor\":2}]"
```

`op` and `type` are both accepted as the operation key.

## Examples

```bash
# Rotate, crop, zoom, then emit base64 for re-analysis
python scripts/image_helper.py screenshot.png --rotate 5 --crop-preset center --scale-preset x2 --base64

# Force raw base64 input and return a cropped detail
python scripts/image_helper.py "<base64>" --input-mode base64 --crop-preset center --scale-preset x2 --base64

# Convert a file path directly to base64 with no image edits
python scripts/image_helper.py image.png --base64
```
