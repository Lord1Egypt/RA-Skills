# VirusTotal Skill

Scan files, URLs, domains, and IP addresses for malware and threats using the [VirusTotal Public API v3](https://docs.virustotal.com/reference/overview).

Covers all free-tier endpoints: file upload/scanning, URL scanning, domain reports, IP address reports, and analysis status polling.

## ⚠️ Privacy Notice

**Submitted files, URLs, and artifacts are shared with VirusTotal and its security partners.** Do not upload proprietary, confidential, or regulated data. Prefer hash lookups for sensitive files. Always confirm before submitting.


## Features

- **File scanning:** Upload files (up to 32MB direct, 650MB via upload URL) or look up by hash
- **URL scanning:** Submit URLs for analysis, retrieve reports
- **Domain reports:** Reputation, WHOIS, DNS records, TLS certificates, engine verdicts
- **IP address reports:** AS owner, country, network, reputation, engine verdicts
- **Analysis polling:** Check scan status for async file/URL submissions
- **Agent-agnostic:** works with OpenClaw, Hermes, Claude, or standalone

## Setup

1. Get your free API key from https://www.virustotal.com/gui/my-apikey
2. Create the secrets file:
   ```bash
   mkdir -p ~/.openclaw/secrets
   echo 'VIRUSTOTAL_API_KEY=your_key_here' > ~/.openclaw/secrets/virustotal.env
   chmod 600 ~/.openclaw/secrets/virustotal.env
   ```
3. Install the skill (see [Agent Integration](#agent-integration) below)

## Agent Integration

This skill works with any agent framework. It provides a `SKILL.md` with complete API documentation and curl examples.

### OpenClaw (example)

1. Follow the [Setup](#setup) steps above
2. Install the skill:
   ```bash
   openclaw skills install virustotal3
   ```
   Or manually: clone/copy the `virustotal/` directory into your skills path (typically `~/.openclaw/skills/` or `~/workspace/skills/`).
3. Ask your assistant: "Scan this URL for malware" or "Check the reputation of 8.8.8.8"

### Other Agent Frameworks

Point your agent to `SKILL.md` as the entry point. Set `VIRUSTOTAL_SECRETS_FILE` if your secrets are stored elsewhere.

## Prerequisites

- **curl** — API requests (only dependency)

## Rate Limits

Free tier: **4 requests per minute** across all endpoints. The skill respects this and documents retry behaviour for HTTP 429 responses.

## Free vs Premium

This skill covers **public/free endpoints only**. Premium features (retrohunt, livehunt, YARA rules, bulk operations, priority processing) are not included and clearly marked in the documentation.

## Files

- `SKILL.md` — Complete skill documentation with all endpoints and curl examples
- `README.md` — This file
- `CHANGELOG.md` — Version history

## License

MIT-0 (MIT No Attribution)

## Author

arfonzo ([github.com/arf0nz0](https://github.com/arf0nz0))
