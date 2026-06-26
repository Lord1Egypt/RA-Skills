---
name: universal-extractor
description: Extract clean text from URLs, articles, documents, and files. Four extraction micro-services. Use when you need to pull content from web pages, PDFs, or any file format.
---

# Universal Extractor

Four extraction services — URL to text, article to summary, document to JSON.

## Services

### /clean-url — URL to Clean Text
Strip ads, nav, footers. Get the content.
```
POST /x402s/clean-url
Body: {"url": "https://example.com/article"}
Response: {"text": "...", "title": "...", "author": "...", "word_count": 1234}
Price: $0.001 USDC
```

### /extract-article — Article + Summary
Full article extraction with optional LLM summary.
```
POST /x402s/extract-article
Body: {"url": "https://...", "summarize": true}
Response: {"title": "...", "text": "...", "summary": "...", "author": "...", "date": "..."}
Price: $0.005 USDC
```

### /extract-document — Document to Text
Base64-encoded PDF/DOCX/TXT to structured text.
```
POST /x402s/extract-document
Body: {"content": "<base64>", "filename": "report.pdf"}
Response: {"text": "...", "word_count": 5678}
Price: $0.002 USDC
```

### /extract-file — Any File to Text
Universal file-to-text extraction.
```
POST /x402s/extract-file
Body: {"content": "<base64>", "filename": "data.csv"}
Response: {"text": "...", "word_count": 234}
Price: $0.002 USDC
```

## Payment
x402 protocol — USDC on Base. No API keys needed.
