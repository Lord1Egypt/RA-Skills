# Changelog

All notable changes to the Screen Capture Hub skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-13

### Added
- Initial release of Screen Capture Hub skill
- Basic screen capture functionality using PIL/Pillow and pyautogui
- OCR text recognition support with pytesseract
- Screen analysis tools for finding text, colors, and edges
- Comprehensive documentation and usage examples
- Test scripts for validating environment and dependencies

### Features
- **Full screen capture**: Capture entire screen with single command
- **Region capture**: Capture specific screen areas with coordinates
- **OCR integration**: Extract text from screenshots in multiple languages
- **Screen analysis**: Find specific text, colors, and detect edges
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Easy installation**: Simple Python dependencies with clear installation instructions

### Technical Details
- Built with Python 3.8+
- Uses Pillow for image processing
- Integrates with pyautogui for screen interaction
- Supports Tesseract OCR for text recognition
- Includes OpenCV for advanced image analysis

### Dependencies
- Python 3.8 or higher
- Pillow >= 9.0.0
- pyautogui >= 0.9.0
- pytesseract >= 0.3.0 (optional for OCR)
- opencv-python >= 4.5.0 (optional for advanced analysis)
- numpy >= 1.20.0 (optional for advanced analysis)

## [0.1.0] - 2026-03-13

### Development Release
- Initial development and testing
- Basic functionality validation
- Documentation setup
- Package structure definition