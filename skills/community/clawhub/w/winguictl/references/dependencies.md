# Dependencies

Install dependencies in a virtual environment from trusted package indexes, pin known-good versions where possible, and review dependency provenance before use.

## Quick Install

### Core dependencies (required)

```powershell
pip install -r assets/requirements.txt
```

### Optional dependencies (image matching)

```powershell
pip install -r assets/requirements-optional.txt
```

## Package Details

| Package | Install | Required | Description |
|---------|---------|----------|-------------|
| Python 3.10+ | — | Yes | Runtime |
| pywinauto | `pip install pywinauto` | Yes | Windows GUI automation (core dependency) |
| pywin32 | `pip install pywin32` | Yes | Win32 API Pythonic wrapper (win32gui/win32api/win32con/win32ui) |
| comtypes | `pip install comtypes` | Yes | COM interface support for UIA |
| Pillow | `pip install Pillow` | Yes | Image processing |
| wx-ocr | `pip install wx-ocr` | No | Self-contained WeChat OCR, no external dependencies |
| opencv-python | `pip install opencv-python` | No | Image template matching |
| numpy | `pip install numpy` | No | Array operations for OpenCV |
