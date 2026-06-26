TokenFlow — Convert files and URLs to structured text for AI consumption.

Supports: PDF, DOCX, XLSX, PPTX, HTML, CSV, JSON, XML, TXT, MD, audio (WAV, MP3, OGG, FLAC, M4A), ZIP. Images are extracted from PDFs only.

## Installation

Copy the `tokenflow/` skill directory to `~/.hermes/skills/`, then configure your API key.

## Authentication

If you already have an API key, set it in `~/.hermes/skills/tokenflow/config.json`:

```json
{ "apiKey": "your-api-key-here" }
```

If you don't have an API key, you can sign up directly from the CLI:

```bash
# Sign up (creates account + generates API key)
tokenflow signup --email you@example.com --password yourpassword

# Or sign in with existing credentials
tokenflow signin --email you@example.com --password yourpassword
```

Your API key will be saved automatically to the config file.

## Quota & Upgrades

TokenFlow operates on a tiered quota system (Free: 20 docs/mo, Pro: 500/mo, etc.). If you exceed your quota, the skill will return the original file unchanged and notify you. To upgrade your plan, visit: https://tokenflow.fly.dev
