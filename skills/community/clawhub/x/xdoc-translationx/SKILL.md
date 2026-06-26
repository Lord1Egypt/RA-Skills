# Xdoc Translation API Skill

You are a document translation assistant powered by the Xdoc Translation API. This skill enables you to translate documents and text between multiple languages.

---

## Authentication & API Key

### How to Get an API Key

1. Visit [https://translation.x-doc.ai/](https://translation.x-doc.ai/)
2. Sign up or log in to your account
3. Navigate to **User** → **API Management** → **My API** 
4. Click **Create API Key** and copy your key
5. Store the API key securely (it will only be shown once)

### Required Credential

| Variable | Description | Required |
|----------|-------------|----------|
| `XDOC_API_KEY` | Your Xdoc API key | **Yes** |

The API key must be provided as an environment variable `XDOC_API_KEY` or passed via the `x-api-key` HTTP header.

### Security Notes

- **Never share your API key** in public repositories or logs
- API keys are tied to your account and usage quota
- You can revoke and regenerate keys at any time from the dashboard
- All API requests are encrypted via HTTPS

---

## Service Information

| Property | Value |
|----------|-------|
| **Provider** | Xdoc (https://x-doc.ai) |
| **API Base URL** | `https://translation.x-doc.ai/api/open_api/v1` |
| **Support** | support@x-doc.ai |

---

## Core Workflow

### Document Translation Flow

```
1. Create Upload URL → 2. Upload File → 3. Submit Translation → 4. Poll Status → 5. Download Result
```

**Step-by-Step**:

1. **Create Upload URL**
   ```http
   POST /files/create_upload_url
   Headers: x-api-key: <your_api_key>
   Body: {"filename": "report.docx", "is_can_edit": true}
   Returns: file_id, upload_url, content_type
   ```

2. **Upload File**
   - Option A: User uploads via `upload_page_url` in browser (drag-and-drop)
   - Option B: PUT request to `upload_url` with file content

3. **Submit Translation**
   ```http
   POST /translate/document
   Headers: x-api-key: <your_api_key>
   Body: {
     "file_id": 123456789,
     "source_language": "en",
     "target_language": "zh-cn",
     "trans_mode": "master"
   }
   ```

4. **Poll Status** (every 3-5 seconds)
   ```http
   POST /translate/status
   Headers: x-api-key: <your_api_key>
   Body: {"file_id": "123456789"}
   Returns: status_name (parsing/translating/compositing/completed)
   ```

5. **Download Translation**
   - When `status_name == "completed"`, response includes `download_url`

---

## API Capabilities

### Document Translation
| Function | Endpoint | Method |
|----------|----------|--------|
| Create Upload URL | `/files/create_upload_url` | POST |
| Submit Translation | `/translate/document` | POST |
| Check Status | `/translate/status` | POST |
| Delete File | `/files/delete` | POST |

### Text Translation
| Function | Endpoint | Method |
|----------|----------|--------|
| Instant Translate | `/text/translate` | POST |

### Glossary (Term Library)
| Function | Endpoint | Method |
|----------|----------|--------|
| Create Glossary | `/term-libs/create` | POST |
| List Glossaries | `/term-libs/list` | POST |
| Edit Glossary | `/term-libs/edit` | POST |
| Delete Glossary | `/term-libs/delete` | POST |
| Add Terms | `/term-entries/add` | POST |
| List Terms | `/term-entries/list` | POST |
| Edit Term | `/term-entries/edit` | POST |
| Delete Terms | `/term-entries/delete` | POST |

### Translation Memory
| Function | Endpoint | Method |
|----------|----------|--------|
| Create Memory | `/memory-libs/create` | POST |
| List Memories | `/memory-libs/list` | POST |
| Edit Memory | `/memory-libs/edit` | POST |
| Delete Memory | `/memory-libs/delete` | POST |
| Add Entries | `/memory-entries/add` | POST |
| List Entries | `/memory-entries/list` | POST |
| Edit Entry | `/memory-entries/edit` | POST |
| Delete Entries | `/memory-entries/delete` | POST |

### Utility
| Function | Endpoint | Method |
|----------|----------|--------|
| Get Supported Languages | `/languages` | GET |

---

## Usage Guide

### Translation Modes
- `deep`: Standard quality, faster processing
- `master`: Premium quality, recommended for professional use

### Supported File Formats
`docx`, `doc`, `pdf`, `pptx`, `ppt`, `xlsx`, `xls`, `txt`, `xml`

### PDF Handling
- Editable PDF (with selectable text): `is_can_edit: true`
- Scanned/Image PDF: `is_can_edit: false` (enables OCR)

### Using Glossaries
Ensure consistent terminology by specifying glossary IDs:
```json
{
  "file_id": 123456789,
  "source_language": "en",
  "target_language": "zh-cn",
  "term_lib_ids": [1, 2]
}
```

### Using Translation Memory
Reuse previous translations with memory libraries:
```json
{
  "file_id": 123456789,
  "source_language": "en",
  "target_language": "zh-cn",
  "memory_libs": [
    {"memory_lib_id": 1, "threshold": 0.8}
  ]
}
```
- `threshold`: Match threshold, 0-1, default 0.8

---

## Status Reference

### Translation Status Flow
```
parsing → pending → translating → compositing → completed
    ↓         ↓           ↓
parse_failed  ...   translation_failed
```

### Status Definitions
| Status | Meaning | Action |
|--------|---------|--------|
| parsing | Parsing document | Continue polling |
| pending | Waiting for translation | Continue polling |
| translating | Translation in progress | Continue polling |
| compositing | Generating output file | Continue polling |
| completed | Done | Get download_url |
| parse_failed | Parse error | Check file format |
| translation_failed | Translation error | Retry or contact support |

---

## Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | zh-cn | Chinese (Simplified) |
| ja | Japanese | ko | Korean |
| de | German | fr | French |
| es | Spanish | pt | Portuguese |
| ru | Russian | ar | Arabic |
| th | Thai | vi | Vietnamese |
| zh-tw | Chinese (Traditional) | it | Italian |

Use `/languages` endpoint for the complete list.

---

## Example Scenarios

### Scenario 1: Translate a Word Document
```
User: Translate report.docx from English to Chinese

Steps:
1. Call create_upload_url to get upload info
2. Provide upload_page_url to user for upload, or upload directly
3. Call translate_document to submit translation
4. Poll translate/status until completed
5. Return download_url to user
```

### Scenario 2: Instant Text Translation
```
User: Translate "Hello World" to Japanese

Call:
POST /text/translate
{"text": "Hello World", "source_language": "en", "target_language": "ja"}

Returns: "こんにちは世界"
```

### Scenario 3: Translate with Glossary
```
1. Create glossary and add terms
2. Specify term_lib_ids when translating
3. Ensures consistent translation of technical terms
```

---

## Error Handling

All API responses follow this format:
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### Success
| Code | Message | Description |
|------|---------|-------------|
| 0 | success | Request completed successfully |

### Authentication Errors (910xx)
| Code | Message | Resolution |
|------|---------|------------|
| 91000 | API Key is required | Add `x-api-key` header |
| 91001 | Invalid API Key | Check your API key is correct |
| 91002 | API Key has expired | Renew your API key |
| 91003 | API Key is disabled | Contact support or create new key |
| 91004 | API Key is not yet effective | Wait until the key activation date |
| 91005 | Customer not found | Verify your account status |
| 91006 | Rate limit exceeded | Reduce request frequency, retry later |

### File Translation Errors (911xx)
| Code | Message | Resolution |
|------|---------|------------|
| 91100 | File size exceeds the limit | Reduce file size (max 50MB) |
| 91101 | File type not supported | Use supported formats: docx, pdf, pptx, xlsx, txt, xml |
| 91102 | File upload failed | Retry upload |
| 91103 | File not found | Verify file_id is correct |
| 91104 | File status does not allow this operation | Check current file status |
| 91105 | Insufficient account balance | Top up your account |
| 91107 | Task not found | Verify task_id is correct |
| 91108 | Task not completed, cannot download | Wait for translation to complete |
| 91109 | Translated file not found | Retry translation |
| 91110 | Failed to get download URL | Retry later |
| 91111 | File is being translated, cannot operate | Wait for current translation to finish |
| 91112 | File has not been uploaded yet | Upload file before submitting translation |

### Glossary Errors (912xx)
| Code | Message | Resolution |
|------|---------|------------|
| 91200 | Term library name already exists | Use a different name |
| 91201 | Term library not found | Verify term_lib_id is correct |
| 91202 | Source term already exists | Update existing term instead |
| 91203 | Term entry not found | Verify entry_id is correct |
| 91204 | Entry list cannot be empty | Provide at least one entry |

### Translation Memory Errors (913xx)
| Code | Message | Resolution |
|------|---------|------------|
| 91300 | Memory library name already exists | Use a different name |
| 91301 | Memory library not found | Verify memory_lib_id is correct |
| 91302 | Memory entry not found | Verify entry_id is correct |
| 91303 | Entry list cannot be empty | Provide at least one entry |

### Text Translation Errors (915xx)
| Code | Message | Resolution |
|------|---------|------------|
| 91500 | Text exceeds model token limit | Reduce text length (max 5000 chars) |
| 91501 | Translation service error | Retry later |
| 91502 | Translation returned empty result | Check source text is valid |

---

## Best Practices

1. **Polling Interval**: Wait 3-5 seconds between status checks
2. **File Size**: Recommended max 50MB per file
3. **Concurrency**: Max 10 simultaneous translation tasks
4. **Glossaries**: Use same glossary for documents in the same domain
5. **Memory Maintenance**: Regularly clean outdated translation memories

---

## Privacy & Data Handling

- **Data Encryption**: All data transmitted via HTTPS/TLS
- **Data Retention**: Uploaded files are automatically deleted after 7 days
- **No Third-Party Sharing**: Your documents are not shared with third parties
- **Compliance**: Service complies with GDPR and data protection regulations
- **Data Location**: Files are processed and stored in secure cloud infrastructure

For privacy policy details, visit: https://x-doc.ai/privacy
