# OCR Setup for Screenshot Search

## Tools

### textsnip (CLI)
Fast, lightweight OCR for macOS.

**Install:**
```bash
brew install textsnip
```

**Usage:**
```bash
# OCR a single image
textsnip -i screenshot.png

# OCR multiple files
textsnip -i ~/Desktop/Screenshot*.png

# Pipe to grep for search
textsnip -i ~/Desktop/Screenshot*.png | grep -i "error"
```

### EasyOCR (Python)
More accurate, supports multiple languages.

**Install:**
```bash
pip install easyocr
```

**Usage:**
```python
import easyocr
reader = easyocr.Reader(['en'])
result = reader.readtext('screenshot.png')
for (bounds, text, prob) in result:
    print(text)
```

### macOS Built-in (Live Text)
- **Cmd+Shift+4** then drag to select
- Text is auto-copied to clipboard
- Works in Preview app: select text tool

## Performance Tips

- **textsnip**: Fast for batch operations, good accuracy
- **EasyOCR**: Slower but better for complex layouts
- **Live Text**: Best for one-off captures

## Indexing Strategy

For large screenshot collections, build an index:
```bash
# One-time index creation
for f in ~/Pictures/Screenshots/*.png; do
  textsnip -i "$f" >> ~/Pictures/Screenshots/ocr-index.txt
done

# Search index
grep -i "invoice" ~/Pictures/Screenshots/ocr-index.txt
```
