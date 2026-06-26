# Troubleshooting

Common issues and solutions for Super OCR。

## Installation Issues

### "Module not found: paddleocr"

**Solution:**
```bash
pip install paddleocr paddlepaddle
```

For macOS/Linux:
```bash
pip install paddleocr paddlepaddle
```

For Windows:
```bash
pip install paddleocr paddlepaddle
```

### "Tesseract not found"

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install tesseract-ocr
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

## Runtime Issues

### Low Confidence Results

If OCR results have low confidence:

1. **Enable verbose mode:**
   ```bash
   python scripts/main.py --image image.png --verbose
   ```

2. **Preprocess image manually:**
   ```python
   from super_ocr.preprocessing import preprocess_pipeline
   import cv2
   
   image = cv2.imread('input.png')
   processed = preprocess_pipeline(image, enhance=True, binarize=True)
   cv2.imwrite('processed.png', processed)
   ```

3. **Force PaddleOCR for better accuracy:**
   ```bash
   python scripts/main.py --image image.png --engine paddle
   ```

### Memory Issues (PaddleOCR)

PaddleOCR uses ~500MB memory。If you see memory errors:

1. **Use Tesseract instead:**
   ```bash
   python scripts/main.py --image image.png --engine tesseract
   ```

2. **Process images one by one:**
   ```bash
   for img in images/*.png; do
       python scripts/main.py --image "$img" --output results/
   done
   ```

### Batch Processing Too Slow

**Solutions:**

1. **Use Tesseract for speed:**
   ```bash
   python scripts/main.py --images ./images/*.png --engine tesseract --output ./results/
   ```

2. **Process in parallel:**
   ```bash
   # macOS/Linux
   find ./images -name "*.png" -print0 | xargs -0 -P 4 -I {} python scripts/main.py --image {} --output ./results/
   ```

3. **Initialize processor once, reuse:**
   ```python
   processor = OCRProcessor(engine='auto')
   
   for image in images:
       result = processor.extract(image)
       # Process result
   ```

## Configuration Issues

### Custom Configuration Not Loading

Create `config.yaml` in skill directory:

```yaml
default_engine: auto
confidence_threshold: 0.8
output_format: json
preprocess:
  denoise: true
  enhance_contrast: true
```

### Output Format Not Working

Check format name:
```bash
python scripts/main.py --image image.png --format json
python scripts/main.py --image image.png --format text
python scripts/main.py --image image.png --format structured
```

## Dependency Checker

Run the checker to diagnose issues:

```bash
python scripts/dependencies.py --check --verbose
python scripts/dependencies.py --install
python scripts/dependencies.py --guide
```

## Getting Help

If you encounter issues not covered here:

1. Enable verbose mode: `--verbose`
2. Check dependency status: `python scripts/dependencies.py --check`
3. Try force engine: `--engine tesseract` or `--engine paddle`
4. Report issue with:
   - Python version
   - OS
   - Command used
   - Error message