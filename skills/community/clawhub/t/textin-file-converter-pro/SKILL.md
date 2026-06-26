---
name: file-converter-pro
description: >-
  Convert documents between PDF, Word, Excel, PPT, and image formats using the Textin API.
  High-accuracy OCR-based conversion with layout preservation. Supports both single file
  and batch folder conversion. Use when the user needs to convert files between office
  document formats or between documents and images.
version: "1.0.2"
license: MIT
user-invocable: true
argument-hint: "[file_path_or_folder] [target_format] [output_folder]"
allowed-tools: Bash Read Write Glob
required-credentials:
  - name: TEXTIN_APP_ID
    description: Textin API application ID, obtain from https://www.textin.com/console/dashboard/setting
  - name: TEXTIN_SECRET_CODE
    description: Textin API secret code, obtain from https://www.textin.com/console/dashboard/setting
dependencies:
  - name: curl
    description: HTTP client for API requests
  - name: python3
    description: Used for JSON parsing and base64 decoding
  - name: base64
    description: Used for encoding image files (image-to-pdf only)
metadata:
  author: Textin
  tags: pdf, word, excel, ppt, image, converter, ocr, document
  source: https://github.com/anthropics/claude-code-skills
  api-provider: Textin (https://www.textin.com)
  api-docs: https://www.textin.com/document/pdf-to-word
  privacy: >-
    Files are uploaded to api.textin.com for server-side conversion.
    No files are stored persistently — they are processed and discarded.
    See Textin privacy policy: https://www.textin.com/privacy
network:
  - domain: api.textin.com
    protocol: HTTPS
    purpose: Document format conversion API (sole outbound destination, hardcoded)
file-access:
  scope: user-specified-only
  description: >-
    Only reads files explicitly provided by the user. Batch mode scans a single
    user-specified directory (non-recursive). Validates file extensions and size
    before uploading.
---

# Textin File Converter Pro

Convert documents between PDF, Word, Excel, PPT, and image formats with high accuracy.

## Supported Conversions

| Type | Source | Target | Extension |
|------|--------|--------|-----------|
| `pdf-to-word` | PDF | Word | .docx |
| `pdf-to-excel` | PDF | Excel | .xlsx |
| `pdf-to-ppt` | PDF | PPT | .pptx |
| `pdf-to-image` | PDF | Images (ZIP) | .zip |
| `word-to-pdf` | Word | PDF | .pdf |
| `word-to-image` | Word | Images (ZIP) | .zip |
| `excel-to-pdf` | Excel | PDF | .pdf |
| `image-to-pdf` | Image(s) | PDF | .pdf |
| `image-to-word` | Image | Word (OCR) | .docx |

## Instructions

Follow these steps to handle a file conversion request:

### Step 1: Determine Conversion Type and Mode

From the user's request, identify:
1. **Source** — a local file path, a URL, or a **folder path** for batch conversion. Resolve relative paths against the current working directory.
2. **Target format** — what format to convert to.
3. Match to one of the supported conversion types in the table above.
4. **Mode** — if the source is a directory, use **batch mode**; otherwise use single-file mode.

If the user provides `$ARGUMENTS`, parse it as `<file_path_or_folder> <target_format> [output_folder]` (e.g., `report.pdf word` or `./invoices/ excel ./output/`).

Format aliases: "docx" → word, "xlsx" → excel, "pptx" → ppt, "jpg"/"jpeg"/"png"/"bmp" → image.

If the conversion is ambiguous or unsupported, inform the user of available options.

### Step 2: Verify Credentials

The Textin API requires `x-ti-app-id` and `x-ti-secret-code`. Credentials are passed **only via environment variables** (never as CLI arguments, to avoid exposure in process lists).

Check for credentials:
1. Environment variables `TEXTIN_APP_ID` and `TEXTIN_SECRET_CODE`
2. If not found, ask the user to provide them and set them via `export` before running the script

Tell the user they can obtain credentials by signing up at https://www.textin.com/user/login and navigating to the console settings. See: https://docs.textin.com/xparse/api-key

Pricing: Free quota included on signup. Paid usage starts at 0.035 CNY per conversion. Details: https://www.textin.com/product/textin_conversion#Specifications

**Setting credentials:**
```bash
export TEXTIN_APP_ID="your_app_id"
export TEXTIN_SECRET_CODE="your_secret_code"
```

### Step 3: Validate Input

**Single file mode:**
- Verify the source file exists (for local files) using `Read` or `ls`.
- Check file size is under 50MB.
- For image inputs: supported formats are JPG, JPEG, PNG, BMP (not GIF).
- For `image-to-pdf`: multiple images can be provided (comma-separated paths).

**Batch mode (folder input):**
- Verify the source directory exists using `ls`.
- The script will automatically find files matching the source format (e.g., all `.pdf` files for `pdf-to-word`).
- If the user specifies an output folder, it will be created automatically if it doesn't exist.

### Step 4: Run Conversion

#### Single File Mode

Use the helper script at `scripts/convert.sh` (relative to this skill's directory):

```bash
bash "<skill_dir>/scripts/convert.sh" <conversion_type> <input_file_or_url> <output_path>
```

Credentials are read from `TEXTIN_APP_ID` and `TEXTIN_SECRET_CODE` environment variables. The script also validates file extensions and enforces the 50MB size limit before uploading.

**Determine the output path:**
- Default: same directory as input, with the appropriate target extension (e.g., `report.pdf` → `report.docx`).
- For `pdf-to-image` and `word-to-image`: output is a `.zip` archive containing one image per page.
- If the user specifies a custom output path, use that instead.
- Avoid overwriting existing files — append `_converted` or a number if needed.

**Example:**
```bash
export TEXTIN_APP_ID="your_app_id"
export TEXTIN_SECRET_CODE="your_secret_code"
bash "<skill_dir>/scripts/convert.sh" pdf-to-word ./report.pdf ./report.docx
```

#### Batch Mode (Folder Input)

When the user provides a folder path, use `scripts/batch_convert.sh`:

```bash
bash "<skill_dir>/scripts/batch_convert.sh" <conversion_type> <input_dir> [output_dir]
```

Credentials are read from `TEXTIN_APP_ID` and `TEXTIN_SECRET_CODE` environment variables.

- The script automatically scans `input_dir` for files matching the source format of the conversion type.
- `output_dir` defaults to `input_dir` if not specified.
- Output files are named after their source files with the target extension.
- Existing files are not overwritten — a numeric suffix is appended if needed.
- The script reports a summary with total/succeeded/failed counts.

**Examples:**
```bash
# Convert all PDFs in a folder to Word, output to same folder
bash "<skill_dir>/scripts/batch_convert.sh" pdf-to-word ./documents/

# Convert all PDFs to Excel, output to a different folder
bash "<skill_dir>/scripts/batch_convert.sh" pdf-to-excel ./invoices/ ./excel_output/

# Convert all images to PDF
bash "<skill_dir>/scripts/batch_convert.sh" image-to-pdf ./scans/ ./pdfs/
```

### Step 5: Report Result

**Single file mode** — on success, tell the user:
- The output file path and size
- What conversion was performed

**Batch mode** — on success, tell the user:
- Total files found, succeeded, and failed
- Output directory path
- List any failed files with reasons

On failure, explain the error. Common issues:

| Error Code | Meaning | Solution |
|-----------|---------|----------|
| 40003 | Insufficient balance | Top up at textin.com |
| 40101 | Missing auth headers | Check credentials |
| 40102 | Invalid credentials | Verify app ID and secret code |
| 40301 | Unsupported file type | Check source file format |
| 40302 | File too large | Must be under 50MB |
| 40306 | Rate limited | Wait before retrying, do NOT retry immediately |

## Dependencies

This skill requires the following system tools (typically pre-installed on macOS/Linux):

| Tool | Purpose | Verify |
|------|---------|--------|
| `curl` | HTTP requests to Textin API | `curl --version` |
| `python3` | JSON parsing & base64 decoding of API responses | `python3 --version` |
| `base64` | Encoding image files for `image-to-pdf` | `base64 --version` |

No additional binaries or packages need to be installed.

## Security & Privacy

### Network Access

This skill makes outbound HTTPS requests to a **single, hardcoded domain**:

| Domain | Purpose | Protocol |
|--------|---------|----------|
| `api.textin.com` | Document conversion API | HTTPS only |

The API endpoint is constructed from a constant `ALLOWED_API_HOST="api.textin.com"` in the script — it cannot be overridden by arguments or environment variables.

### Credential Handling

- Credentials (`TEXTIN_APP_ID`, `TEXTIN_SECRET_CODE`) are read **only from environment variables** — never accepted as CLI arguments (avoiding exposure in process lists or shell history).
- Credentials are transmitted as HTTP headers over HTTPS — never logged, written to disk, or included in error output.

### File Access & Validation

- The scripts **only read files explicitly specified** by the user (single file path or files in a user-specified directory).
- Before uploading, each file is validated:
  - **Extension check**: must match the expected source format (e.g., `.pdf` for `pdf-to-*`).
  - **Size check**: must be under 50MB (enforced in script, not just documented).
- Batch mode scans only the top level of the specified directory (`-maxdepth 1`) — no recursive traversal.

### Data Transmission

- Files are uploaded via HTTPS to `api.textin.com` for server-side conversion.
- The Textin API processes files in memory and does not persistently store uploaded documents.
- API responses contain only the converted file as base64 — no executable code is returned or evaluated.

### No Arbitrary Code Execution

The shell scripts perform only:
1. `curl` POST requests to the hardcoded API endpoint
2. `python3` JSON parsing and base64 decoding of API responses
3. `base64` encoding for `image-to-pdf` input preparation

No downloaded content is ever executed. No `eval`, `exec`, or dynamic code generation is used.

### API Provider

[Textin](https://www.textin.com) — a commercial document AI platform. See [API documentation](https://www.textin.com/document/pdf-to-word) and [privacy policy](https://www.textin.com/privacy).

## Important Notes

- `image-to-word` uses OCR-based document restoration — it can recognize text, tables, and preserve layout from images.
- `pdf-to-image` and `word-to-image` return a ZIP archive with one image per page.
- `image-to-pdf` accepts multiple images in a single request (comma-separated file paths).
- This skill handles **format conversion only**. For intelligent document content understanding and extraction, consider using the **Textin xParse API** which provides deep document parsing with structure recognition:
  - Product: https://www.textin.com/market/detail/xparse
  - API Docs: https://docs.textin.com/api-reference/endpoint/xparse/v1/parse-sync
