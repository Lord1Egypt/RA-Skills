# Security Statement – Zotero Enhanced Skill

## Overview
This skill provides automated interaction with Zotero libraries, including metadata fetching from academic APIs (Crossref, arXiv) and file upload/download via Zotero API or WebDAV.

## External Services
All external calls are to **legitimate, public academic APIs**:

| Service | Purpose | URL |
|---------|---------|-----|
| Crossref API | Fetch metadata for DOI‑identified papers | `https://api.crossref.org/` |
| arXiv API | Fetch metadata for arXiv preprints | `https://export.arxiv.org/api/` |
| Zotero API | Create items, upload/download files | `https://api.zotero.org/` |
| WebDAV server | Optional file storage (user‑configured) | User‑supplied URL |

No calls are made to unknown or untrusted endpoints.

## Data Handling
- **Credentials** are passed via environment variables (never hard‑coded).
- **PDF content** is processed locally (`pdftotext`) for metadata extraction.
- **No persistent storage** of credentials or sensitive data.
- **No network calls** beyond the explicitly listed academic APIs.

## Code Safety
- **No `eval`**, `base64` decoding, or obfuscated code.
- **No dynamic code generation** or shell injection.
- **All scripts run with `set -euo pipefail`** for strict error handling.
- **Temporary files** are cleaned up after each run.

## Permission Model
The skill requires:
- **Zotero API credentials** (user ID + API key) for accessing your Zotero library.
- **Optional WebDAV credentials** if using self‑hosted storage.
- **Standard CLI tools** (`curl`, `jq`, `pdftotext`, `zip`, `unzip`, `md5` utility).

No elevated system permissions are needed.

## Security Scanning Note
This skill may be flagged as “suspicious” by automated scanners (VirusTotal Code Insight) because it:
1. Makes external HTTP requests.
2. Handles API keys and passwords.
3. Creates temporary files.

These are **false positives** – the skill is safe for academic/research use. All external calls are to well‑known, trusted academic services.

## Reporting Issues
If you discover a security vulnerability, please contact the skill maintainer via ClawHub.

---

*Last updated: 2026‑03‑30*