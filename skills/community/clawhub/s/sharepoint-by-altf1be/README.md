# openclaw-skill-sharepoint

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-green.svg)](https://nodejs.org/)
[![SharePoint](https://img.shields.io/badge/SharePoint-Online-blue.svg?logo=microsoftsharepoint)](https://www.microsoft.com/en-us/microsoft-365/sharepoint/)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://clawhub.ai)
[![ClawHub](https://img.shields.io/badge/ClawHub-sharepoint--by--altf1be-orange)](https://clawhub.ai/skills/sharepoint-by-altf1be)
[![Security](https://img.shields.io/badge/Security_Scan-Benign-green)](https://clawhub.ai/skills/sharepoint-by-altf1be)
[![GitHub last commit](https://img.shields.io/github/last-commit/ALT-F1-OpenClaw/openclaw-skill-sharepoint)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint/commits/main)
[![GitHub issues](https://img.shields.io/github/issues/ALT-F1-OpenClaw/openclaw-skill-sharepoint)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint/issues)
[![GitHub stars](https://img.shields.io/github/stars/ALT-F1-OpenClaw/openclaw-skill-sharepoint)](https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint/stargazers)

OpenClaw skill for Microsoft SharePoint — secure file operations and Office document intelligence via Microsoft Graph API with certificate-based authentication (`Sites.Selected`).

By [Abdelkrim BOUJRAF](https://www.alt-f1.be) / ALT-F1 SRL, Brussels 🇧🇪 🇲🇦

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Setup](#setup)
- [Commands](#commands)
- [Supported File Formats](#supported-file-formats)
- [Security](#security)
- [ClawHub](#clawhub)
- [License](#license)
- [Author](#author)
- [Contributing](#contributing)

## Features

### SharePoint file operations
- **list** — browse files and folders in a SharePoint library
- **read** — download and extract text from Office documents (`.docx`, `.xlsx`, `.pptx`, `.pdf`, `.txt`, `.md`)
- **upload** — upload files to SharePoint
- **search** — find files by name
- **mkdir** — create folders
- **delete** — remove files (requires explicit `--confirm` flag)

### Office document intelligence (AI-powered via OpenClaw)
- **Meeting notes** — clean up raw notes into professional Word documents
- **Summarize** — business or technical summaries of any document
- **Action items** — extract action items into Excel trackers
- **Presentations** — generate PowerPoint slides from notes or reports

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ALT-F1-OpenClaw/openclaw-skill-sharepoint.git
cd openclaw-skill-sharepoint

# 2. Install
npm install

# 3. Configure
cp .env.example .env
# Edit .env with your tenant ID, app client ID, cert path, site ID

# 4. Use
node scripts/sharepoint.mjs list
node scripts/sharepoint.mjs read --path "Report.docx"
node scripts/sharepoint.mjs upload --local ./report.docx --remote "Reports/Q1-2026.docx"
```

## Setup

### Prerequisites

- Node.js 18+
- Microsoft Entra app registration with:
  - `Sites.Selected` application permission (admin-consented)
  - Certificate-based authentication (no client secret)
  - Site-level grant (`read` or `write`) on target SharePoint site
- Certificate (`.pfx` or `.key` + `.crt`) accessible to OpenClaw

See [references/setup-guide.md](references/setup-guide.md) for the full step-by-step secure setup guide.

## Commands

See [SKILL.md](./SKILL.md) for full command reference.

### Usage with OpenClaw

Once installed as a skill, you can use natural language:

> "List files in SharePoint"

> "Read the meeting notes from today"

> "Upload this report to SharePoint"

> "Summarize the quarterly review from a business perspective"

## Supported File Formats

| Format | Read | Write | Library |
|--------|------|-------|---------|
| `.docx` (Word) | ✅ | ✅ | `mammoth` / `docx` |
| `.xlsx` (Excel) | ✅ | ✅ | `exceljs` |
| `.pptx` (PowerPoint) | ✅ | ✅ | `pptxgenjs` |
| `.pdf` | ✅ | — | `pdf-parse` |
| `.txt` / `.md` | ✅ | ✅ | native |

## Security

This skill follows an **extreme security** approach:

- **Certificate-based auth only** — no client secrets, no passwords
- **`Sites.Selected`** — app can only access one specific SharePoint site
- **Dedicated app registration** — single-tenant, single-purpose
- **Isolated site** — target library is in a dedicated SharePoint site
- **Code-level controls** — path validation, size limits, operation allowlists
- **No tokens in logs** — all sensitive data is redacted
- **Delete requires explicit `--confirm` flag**

## ClawHub

Published as: `sharepoint-by-altf1be`

```bash
clawhub install sharepoint-by-altf1be
```

## License

MIT — see [LICENSE](./LICENSE)

## Author

Abdelkrim BOUJRAF — [ALT-F1 SRL](https://www.alt-f1.be), Brussels 🇧🇪 🇲🇦
- GitHub: [@abdelkrim](https://github.com/abdelkrim)
- X: [@altf1be](https://x.com/altf1be)

## Contributing

Contributions welcome! Please open an issue or PR.
