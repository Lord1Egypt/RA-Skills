# Implementation Notes

Edge cases, error handling, and gotchas for the invoice extractor.

---

## Encrypted PDFs

The script will report the error when it encounters an encrypted PDF. Ask the user for the password — do not attempt to bypass encryption.

## Scanned PDFs (Image-Only)

`pdfplumber` will return empty text for scanned/image-only PDFs. When this happens:

1. Extract the first page as an image (using `pdfplumber` or a screenshot tool)
2. Use the `image` tool to analyze the extracted image instead
3. Proceed with normal extraction from the image result

## Missing Dependencies

The script will detect missing dependencies and suggest install commands:

- **pdfplumber** — primary PDF extraction: `pip install pdfplumber`
- **PyPDF2** — fallback if pdfplumber unavailable: `pip install PyPDF2`

Everything else is Python stdlib.

## Fallback Chain

```
pdfplumber → PyPDF2 → image tool (for scanned PDFs)
```

If both PDF libraries are unavailable and the file is not an image, inform the user and suggest installing `pdfplumber`.
