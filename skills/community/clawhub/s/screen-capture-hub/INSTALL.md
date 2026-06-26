# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Quick Installation

1. **Install Python dependencies:**

```bash
pip install pillow pyautogui
```

2. **For OCR functionality (optional):**

```bash
pip install pytesseract
```

3. **For advanced image analysis (optional):**

```bash
pip install opencv-python numpy
```

## Tesseract OCR Installation

### Windows
1. Download Tesseract OCR installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. During installation, check "Add to PATH" or add the installation directory to your system PATH manually
4. Default installation path: `C:\Program Files\Tesseract-OCR\`

### macOS
```bash
brew install tesseract
```

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng
sudo apt-get install tesseract-ocr-chi-sim  # For Chinese
```

## Verification

Run the test script to verify installation:

```bash
python scripts/test_screenshot.py
```

## Troubleshooting

### Common Issues

1. **"No module named 'pyautogui'"**
   - Make sure you have Python installed correctly
   - Try: `python -m pip install --user pyautogui`

2. **Screenshots show black screen**
   - Run as administrator (Windows)
   - Check application permissions

3. **Tesseract not found**
   - Ensure Tesseract is installed and in PATH
   - Or specify the path manually in your script:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

4. **Permission errors**
   - On macOS/Linux, you may need to grant screen recording permissions
   - On Windows, run as administrator

## Development Installation

For development, install all dependencies including development tools:

```bash
pip install -r requirements.txt
```

## Updating

To update to the latest version:

```bash
pip install --upgrade pillow pyautogui pytesseract opencv-python numpy
```