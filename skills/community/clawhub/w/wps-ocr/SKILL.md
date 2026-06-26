---
name: wps-ocr
description: A lightweight, high-performance file parsing tool that can quickly and accurately extract text, handwritten text, formulas, tables, documents and seals from files into Markdown structure. It supports various common file scenarios such as scanned documents, screenshots and regular photos, and is compatible with multiple file formats including JPG, PNG, BMP, HEIF and WEBP, making it an efficient tool for text digitization.

metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      pip:
        - requests
    required_env_vars:
      - WPS_OCR_ACCESS_KEY
    allowed_domains:
      - aiwrite.wps.cn
    security_notes: "Requires WPS OCR credentials via environment variables. No credential hardcoding. Enforces domain allowlist in code."
---

# 🧭 Must-Read Before Use (30 Seconds)

> [!WARNING]
> **⚠️ Important Privacy & Data Flow Notice**
> - **Service Interaction Required**: This skill will send the file you provide to the official Kingsoft Office server (aiwrite.wps.cn) for recognition.
> - **Data Visibility**: Kingsoft Office services will access and process the content of your file.
> - **This skill supports local file uploads, and will only verify the file type without performing any verification on the path.**

✅ **Recommended Method: Environment Variables (Permission-Free, Instant Effect, Webchat-Friendly)**
```bash
# Run in the terminal (effective immediately for the current session):
export WPS_OCR_ACCESS_KEY="your_client_access_key"
```

```bash
# Append the credential to the ~/.openclaw/env file
echo 'export WPS_OCR_ACCESS_KEY="your_client_access_key"' >> ~/.openclaw/env
```

> [!TIP] **🔧 How to obtain the key?**
> - Get your API key: https://aiwrite.wps.cn/pdf/parse/accesskey/

✅ Environment Dependency Check
Make sure the required libraries are installed:
```bash
pip install requests
```

# 🎯 Skill Execution Guide

## 1. Applicable Scenarios
Invoke this skill when the user’s intent includes any of the following:
- Sends a file and asks “What text is this?”, “Extract text”, or “Convert to text”.
- Uploads document screenshots, invoices, business cards, photos, or scanned files with mixed Chinese and English text to be recognized.
- Needs to translate or edit the file content (text extraction is a required first step).

## 2. Execution Actions
Once it is confirmed that text extraction is required, perform the following operations immediately:
Input Processing:
Obtain the file resource provided by the user (using a download link: url or a local file: path).
Command Execution:
Call the Python script for recognition. If the current environment supports command-line execution, construct the command as follows:

```bash
# use file download URL:
python3 skills/wps-ocr/scripts/wps_ocr.py --url <URL>
# use local file:
python3 skills/wps-ocr/scripts/wps_ocr.py --path <LOCAL-PATH>
```

# Execution Flow
## 1. File Acquisition
The file will be sent to Kingsoft Office Cloud Service, which will download the file provided by the user.
## 2. File Validation
Verify that the file is in a supported format.
## 3. Recognize File Content
Identify elements such as text, images, tables, formulas, and other content in the file, and extract the text.
⚠️ Note: Image elements will be returned as placeholders; file elements will not be returned.
## 4. Return Results to the User
On success: Return all recognized text (concatenated into one string) and detailed detection information.
On failure: Return error messages (e.g., "No text detected in the file", "API call failed", etc.).

# OCR API Usage Notes
This skill relies on the WPS-OCR parsing and recognition capabilities hosted on Kingsoft Cloud Service. The current version is a free trial. To ensure stable operation, the cloud service enforces rate limiting. The service will reject requests under high concurrency; please use it appropriately.
To experience the full features, visit the [demo platform](https://aiwrite.wps.cn/pdf/parse/web/]).