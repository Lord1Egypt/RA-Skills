---
name: sharepoint-by-altf1be
description: "Secure SharePoint file operations and Office document intelligence via Microsoft Graph API — certificate auth, Sites.Selected, read/write Word (mammoth), Excel (exceljs), PowerPoint (jszip), PDF (pdf-parse)."
homepage: https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint
metadata:
  {"openclaw": {"emoji": "📁", "requires": {"env": ["SP_TENANT_ID", "SP_CLIENT_ID", "SP_CERT_PATH", "SP_SITE_ID"]}, "primaryEnv": "SP_TENANT_ID"}}
---

# SharePoint by @altf1be

Interact with SharePoint document libraries via Microsoft Graph API using certificate-based authentication.

## Setup

1. Create an Entra app with `Sites.Selected` permission and certificate auth
2. Grant site-level write access via Microsoft Graph PowerShell
3. Set environment variables (or create `.env` in `{baseDir}`):

```
SP_TENANT_ID=your-azure-tenant-id
SP_CLIENT_ID=your-app-client-id
SP_CERT_PATH=/path/to/certificate.pem
SP_SITE_ID=your-sharepoint-site-id
SP_DRIVE_ID=optional-specific-drive-id
```

4. Install dependencies: `cd {baseDir} && npm install`

## Commands

### File operations

```bash
# Show site and drive info
node {baseDir}/scripts/sharepoint.mjs info

# List files in library root
node {baseDir}/scripts/sharepoint.mjs list

# List files in a subfolder
node {baseDir}/scripts/sharepoint.mjs list --path "Meeting Notes/2026"

# Read file content (extracts text from Office formats)
node {baseDir}/scripts/sharepoint.mjs read --path "Report.docx"

# Upload a file
node {baseDir}/scripts/sharepoint.mjs upload --local ./report.docx --remote "Reports/Q1-2026.docx"

# Search for files
node {baseDir}/scripts/sharepoint.mjs search --query "quarterly review"

# Create folder
node {baseDir}/scripts/sharepoint.mjs mkdir --path "Meeting Notes/2026"

# Delete (requires --confirm flag)
node {baseDir}/scripts/sharepoint.mjs delete --path "Drafts/old-file.txt" --confirm
```

### Coauthoring (checkout/checkin)

```bash
# Safe edit: checkout → upload modified file → checkin (recommended)
node {baseDir}/scripts/sharepoint.mjs edit --path "Report.docx" --local ./modified.docx --comment "Updated summary"

# Check out a file (lock for exclusive editing)
node {baseDir}/scripts/sharepoint.mjs checkout --path "Report.docx"

# Check in a file (unlock + publish)
node {baseDir}/scripts/sharepoint.mjs checkin --path "Report.docx" --comment "Reviewed and approved"

# Get an edit link to open in Office Online
node {baseDir}/scripts/sharepoint.mjs edit-link --path "Report.docx"
```

## Supported Office formats

The `read` command extracts text content from:
- `.docx` → full text extraction via mammoth
- `.xlsx` → sheet names + cell data via exceljs
- `.pptx` → slide text extraction via jszip
- `.pdf` → text extraction via pdf-parse
- `.txt` / `.md` → raw content

Output is plain text suitable for AI processing (summarization, reformatting, action item extraction).

## Dependencies

- `@azure/identity` — certificate-based Azure AD authentication
- `@microsoft/microsoft-graph-client` — Microsoft Graph API client
- `mammoth` — Word document text extraction
- `exceljs` — Excel spreadsheet parsing
- `jszip` — PowerPoint XML extraction
- `pdf-parse` — PDF text extraction
- `commander` — CLI framework
- `dotenv` — environment variable loading

## Security

- Certificate auth only (no client secrets, no passwords)
- `Sites.Selected` permission (access limited to one SharePoint site)
- Path traversal prevention: `../` is rejected
- Delete requires explicit `--confirm` flag
- No tokens or secrets printed to stdout
- File size limit: configurable max (default 50MB)

## Full setup guide

For complete setup from scratch (Entra app, certificate, Sites.Selected, Key Vault):
See the [GitHub repository](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint) README.

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪
X: [@altf1be](https://x.com/altf1be)
