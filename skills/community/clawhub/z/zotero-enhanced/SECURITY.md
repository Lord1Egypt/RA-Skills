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
| WebDAV server | Optional file storage (user‑configured) | User‑supplied **https://** URL (plaintext `http://` is refused) |

No calls are made to unknown or untrusted endpoints.

## Data Handling
- **Credentials** are passed via environment variables (never hard‑coded).
- **WebDAV credentials are only sent over TLS**: every WebDAV script validates that `ZOTERO_WEBDAV_URL` starts with `https://` and refuses to run otherwise (no override).
- **The Zotero API key is only sent to Zotero‑controlled hosts**: attachment download URLs are validated against an allowlist (`https://*.zotero.org`) before the key is attached; the key is never sent to URLs taken verbatim from item metadata.
- **PDF content** is processed locally (`pdftotext`) for metadata extraction.
- **No persistent storage** of credentials or sensitive data. One exception: `delete_note.sh --backup` optionally writes note content to `~/.zotero-backup/` (directory mode 0700, files 0600) at the user's explicit request.
- **No network calls** beyond the explicitly listed academic APIs.

## Code Safety
- **No `eval`**, `base64` decoding, or obfuscated code.
- **No dynamic code generation** or shell injection.
- **All scripts run with `set -e` and `set -o pipefail`** for strict error handling.
- **Temporary files** are created in unpredictable per‑run directories (`mktemp -d`, mode 0700) and cleaned up via `EXIT` traps.
- **Archive safety**: downloaded zip archives are scanned for path‑traversal entries (`../`, absolute paths) before extraction; API‑provided filenames are stripped of path components before use in file paths.

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

*Last updated: 2026‑09‑16*