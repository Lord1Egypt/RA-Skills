# Troubleshooting

## PDF extraction fails or produces poor results

- **Cause**: PDF is scanned images (not text-based) or has complex formatting
- **Solutions**:
  - Ensure PDF is text-based, not scanned images
  - Try OCR tools for scanned documents (e.g., `tesseract`)
  - Manually edit the extracted JSON data to fix issues
  - Check that the PDF uses standard fonts and encoding

## HTML generation fails

- **Cause**: Invalid JSON format, missing required fields, or corrupted file
- **Solutions**:
  - Validate JSON structure using a JSON validator
  - Ensure `personal.name` field exists
  - Verify file is UTF-8 encoded
  - Check error messages for specific field names

## PDF export fails

- **Cause**: PDF generation tools not installed
- **Solutions**:
  - Install Playwright (preferred): `pip install playwright && playwright install chromium`
  - Or install pdfkit: `pip install pdfkit` and `brew install wkhtmltopdf`
  - Verify installation by running the tool's test command

## Theme or CSS not found

- **Cause**: Theme files are missing from assets directory
- **Solutions**:
  - Check that `assets/templates/base.html` exists
  - Verify CSS exists in `assets/css/` for the requested theme
  - Use `--theme modern` as fallback

## Invalid email format error

- **Cause**: Email address doesn't follow standard format
- **Solutions**:
  - Ensure email follows format: `user@domain.com`
  - Remove special characters or spaces
