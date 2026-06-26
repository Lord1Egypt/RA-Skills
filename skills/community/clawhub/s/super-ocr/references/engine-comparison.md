# Engine Comparison

## Tesseract vs PaddleOCR

| Feature | Tesseract | PaddleOCR |
|---------|-----------|-----------|
| **Accuracy** | 90-95% | 98%+ |
| **Chinese Support** | Good | Excellent |
| **Speed** | ~200ms init, ~50ms/img | ~3s init, ~500ms/img |
| **Memory** | ~100MB | ~500MB |
| **Dependencies** | `pytesseract + cv2 + PIL` | `paddleocr + paddlepaddle` |
| **Best For** | Quick extraction, English | High accuracy, Chinese docs |

## When to Use Which

### Use Tesseract When:
- ✅ Extracting text from screenshots
- ✅ Processing English-only documents
- ✅ Need fast OCR (-web scraping, quick验证)
- ✅ Limited memory environment

### Use PaddleOCR When:
- ✅ Processing Chinese documents
- ✅ Need high accuracy (98%+)
- ✅ Working with complex layouts（tables, forms）
- ✅ Critical data extraction (invoices, contracts)

## Performance Comparison

| Task | Tesseract | PaddleOCR | Improvement |
|------|-----------|-----------|-------------|
| Screenshot text | ~70ms | ~600ms | Tesseract faster |
| Chinese menu | ~200ms | ~550ms | - |
| Invoice extraction | ~180ms | ~520ms | - |
| Certificate OCR | ~250ms | ~580ms | PaddleOCR more accurate |

## Quality Comparison

### Example: Chinese Restaurant Menu

**Tesseract (confidence: 88%)**
```
北京烤鸭
宫保鸡丁
麻婆豆腐...
```

**PaddleOCR (confidence: 99%)**
```
北京烤鸭
宫保鸡丁
麻婆豆腐
...
```

### Example: English Invoice

**Tesseract (confidence: 92%)**
```
Invoice #12345
Date: 2024-03-05
Amount: $199.99
```

**PaddleOCR (confidence: 98%)**
```
Invoice #12345
Date: 2024-03-05
Amount: $199.99
```

## Recommendation

- **General use**: Auto mode (PaddleOCR by default for quality)
- **Speed-critical**: Force Tesseract
- **Chinese critical**: Force PaddleOCR
- **Production**: Auto mode with fallback to PaddleOCR for low confidence