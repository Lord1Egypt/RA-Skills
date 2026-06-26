# Step-by-Step Guide

Complete tutorial for using Mistral OCR with practical examples.

> **Note:** All examples use curl (works on Windows, macOS, Linux via Git Bash).

## Quick Start

### 1. Get Your API Key

If you don't have a Mistral API key yet:

1. Go to [console.mistral.ai](https://console.mistral.ai/)
2. Create an account or sign in
3. Go to **API Keys** → **Create new key**
4. Copy your key

### 2. Use Your Key

**Easiest way:** Just tell the AI agent your key:
```
Convert this PDF to markdown. My Mistral API key is: your-key-here
```

**Or set environment variable:**
```bash
export MISTRAL_API_KEY="your-key-here"
```

### 3. Test It Works

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral-ocr-latest", "document": {"type": "document_url", "document_url": "https://arxiv.org/pdf/2201.04234"}}' \
  | head -50
```

---

## Example 1: PDF from URL → Markdown

**Scenario:** Convert a publicly accessible PDF to markdown.

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/report.pdf"
    }
  }' | jq -r '.pages[].markdown' > output.md

echo "Saved to output.md"
```

---

## Example 2: Local PDF → Markdown

**Scenario:** Convert a local PDF file using base64 data URL (works on all platforms):

```bash
BASE64=$(base64 -w0 document.pdf)

curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "data:application/pdf;base64,'"$BASE64"'"
    }
  }' | jq -r '.pages[].markdown' > output.md
```

---

## Example 3: Image → Text

**Scenario:** Extract text from an image URL.

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/screenshot.png"
    }
  }' | jq -r '.pages[].markdown'
```

---

## Example 4: Local Image → Text

**Scenario:** Extract text from a local image using base64 data URL.

```bash
BASE64=$(base64 -w0 image.png)

curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "image_url",
      "image_url": "data:image/png;base64,'"$BASE64"'"
    }
  }' | jq -r '.pages[].markdown'
```

**Note:** Use the correct MIME type for your image:
- PNG: `data:image/png;base64,...`
- JPG: `data:image/jpeg;base64,...`
- WEBP: `data:image/webp;base64,...`

---

## Example 5: Multi-page PDF

**Scenario:** Convert a multi-page PDF and combine all pages.

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/multipage.pdf"
    }
  }' | jq -r '.pages[] | "## Page \(.index + 1)\n\n\(.markdown)\n\n---\n"' > full_document.md
```

---

## Example 6: Extract Tables (HTML format)

**Scenario:** Get tables in proper HTML format.

```bash
curl -s "https://api.mistral.ai/v1/ocr" \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-ocr-latest",
    "document": {
      "type": "document_url",
      "document_url": "https://example.com/spreadsheet.pdf"
    },
    "table_format": "html"
  }' | jq -r '.pages[].markdown'
```

---

## Example 7: Batch Processing Multiple Files

**Scenario:** Process all PDFs in a folder.

```bash
mkdir -p output

for pdf in *.pdf; do
  echo "Processing: $pdf"
  BASE64=$(base64 -w0 "$pdf")

  curl -s "https://api.mistral.ai/v1/ocr" \
    -H "Authorization: Bearer $MISTRAL_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "mistral-ocr-latest",
      "document": {"type": "document_url", "document_url": "data:application/pdf;base64,'"$BASE64"'"}
    }' | jq -r '.pages[].markdown' > "output/${pdf%.pdf}.md"
done

echo "Done! Check output/ folder"
```

---

## Common Issues & Solutions

### Issue: "jq: command not found"

**Recommended:** Use node instead (more universal):
```bash
node -e "const r=JSON.parse(require('fs').readFileSync('/tmp/response.json')); console.log(r.pages.map(p=>p.markdown).join('\n\n'))"
```

Or use python:
```bash
python -c "import sys,json; print(json.load(sys.stdin)['pages'][0]['markdown'])"
```

### Issue: "base64: invalid option -- 'w'"

On macOS, use:
```bash
base64 -i file.pdf    # instead of base64 -w0
```

### Issue: URL fetch error (3310)

The URL might not be publicly accessible. Use base64 encoding for local files instead.

### Issue: Large file timeout

For very large files (>50 pages), consider:
1. Splitting the PDF first
2. Using the Batch API for better rates
3. Processing pages individually

---

## Tips for Best Results

1. **Document Quality**
   - Higher resolution = better results
   - Ensure good contrast
   - Avoid skewed or rotated pages

2. **Supported Languages**
   - Works with dozens of languages
   - Best results with Latin scripts, English
   - Supports Arabic, Chinese, Hindi, and more

3. **Tables**
   - Use `"table_format": "html"` for complex tables
   - OCR 3 handles colspan/rowspan correctly

4. **Handwriting**
   - Mistral OCR 3 improved handwriting recognition
   - Still best with printed text

---

## Next Steps

- See [formats.md](formats.md) for JSON and structured output options
- See [pdf-to-markdown.md](pdf-to-markdown.md) for advanced PDF handling
- Check Mistral docs at [docs.mistral.ai](https://docs.mistral.ai/capabilities/document_ai)
