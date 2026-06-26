# Screenshot Commands

Capture window screenshots.

## ⚠️ Warning

Screenshots capture all visible content, which may include sensitive information. Close sensitive applications before taking screenshots.

## Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `screenshot` | Capture window screenshot | `--window-id`, `--output`, `--x`, `--y`, `--width`, `--height`, `--dry-run` |

## Usage

```powershell
# Capture entire window
screenshot --window-id <id> --output shot.png

# Save as BMP
screenshot --window-id <id> --output shot.bmp

# Capture rectangular region
screenshot --window-id <id> --output region.png --x 100 --y 50 --width 300 --height 200

# Preview mode
screenshot --window-id <id> --output shot.png --dry-run
```

## Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `--window-id` | Window handle | Yes |
| `--output` | Output file path (`.png` or `.bmp`) | Yes |
| `--x` | Left offset (window-relative) | No (region capture) |
| `--y` | Top offset (window-relative) | No (region capture) |
| `--width` | Region width | No (region capture) |
| `--height` | Region height | No (region capture) |
| `--dry-run` | Preview mode | No |

## Rectangular Region

When all four region parameters (`--x`, `--y`, `--width`, `--height`) are provided, only the specified region is captured. All four must be provided together.

**Coordinate origin**: Window's top-left corner (excluding title bar border).

## Output Format

### Full Window

```json
{
  "ok": true,
  "code": "OK",
  "message": "screenshot executed",
  "data": {
    "window_id": "123456",
    "output": "artifacts\\shot.png"
  }
}
```

### Rectangular Region

```json
{
  "ok": true,
  "code": "OK",
  "message": "screenshot executed",
  "data": {
    "window_id": "123456",
    "output": "artifacts\\region.png",
    "rect": {
      "x": 100,
      "y": 50,
      "width": 300,
      "height": 200
    }
  }
}
```

### Preview Mode

```json
{
  "ok": true,
  "code": "DRY_RUN",
  "message": "screenshot preview generated",
  "data": {
    "window_id": "123456",
    "output": "artifacts\\shot.png"
  }
}
```

## Dependencies

- `Pillow`: `pip install Pillow`
