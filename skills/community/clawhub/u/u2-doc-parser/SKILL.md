Name: u2-doc-parser
Description: Parse documents using UniDoc API for conversion to Markdown or JSON format. Supports both synchronous and asynchronous parsing with automatic status polling.

UniDoc Document Parser
======================

Overview
--------
Parse documents using UniDoc API for conversion to Markdown or JSON format. Supports both synchronous and asynchronous parsing with automatic status polling. Ideal for converting various document formats (PDF, DOC, DOCX, images) through a cloud-based API service.

**⚠️ Important Privacy Notice**
- This skill uploads your documents to an external API service: `https://unidoc.uat.hivoice.cn`
- Documents are transmitted over the internet and processed on third-party servers
- No authentication or API key is required for this UAT environment
- **Do not use** with sensitive, confidential, or private documents
- By using this skill, you acknowledge that your files will be uploaded to external servers

Prereqs / when to read references
---------------------------------
If you encounter API errors, network issues, or need to understand the API endpoints, read:
* `references/unidoc-notes.md`

Quick start (single document)
-----------------------------
```bash
# Output to terminal (default)
python scripts/unidoc_parse.py /path/to/file.pdf

# Save to file
python scripts/unidoc_parse.py /path/to/file.pdf --output result.md

# Convert to JSON format (async mode)
python scripts/unidoc_parse.py /path/to/file.docx --format json --mode async
```

Options
-------
* `--format md|json` (default: `md`)
  - Output format: Markdown or JSON
* `--mode sync|async` (default: `sync`)
  - Synchronous mode: waits for conversion to complete
  - Asynchronous mode: polls status until completion
* `--func METHOD` (default: `unisound`)
  - Conversion method/algorithm to use
* `--output FILE` (optional)
  - Save output to file instead of printing to terminal
  - When not specified, results are printed directly to stdout
* `--uid UUID` (optional)
  - Custom user ID (auto-generated if not provided)

Output
------
* **Default**: Prints converted content directly to terminal (stdout)
* **With --output**: Saves to specified file path
* Progress and error messages are sent to stderr
* Can be piped to other commands: `python scripts/unidoc_parse.py doc.pdf | grep "keyword"`

Notes
-----
* **Privacy**: Your documents are uploaded to UniDoc's UAT servers for processing
* **No authentication**: Current implementation does not require API keys or credentials
* **Network**: Requires internet connectivity to https://unidoc.uat.hivoice.cn
* **Supported formats**: PDF, DOC, DOCX, PNG, JPG, etc.
* **Async mode**: Polls every 1 second until completion (max 5 minutes)
* **Limits**: Max file size and rate limits depend on API service configuration
* **Recommendation**: For large files or batch processing, prefer async mode
* **Security**: Only use with non-sensitive test documents
