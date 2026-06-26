# MITRE ATT&CK Technique Mapper

Map threat descriptions, incident reports, or security observations to MITRE ATT&CK techniques and tactics. Submit free-text describing attacker behavior or upload a security report file — get back matched ATT&CK technique IDs, tactic categories, kill chain position, detection guidance, and mitigation recommendations.

---

## Usage

This endpoint uses `multipart/form-data` — not JSON. Submit either a text description (`input`) or a file upload (`file`), or both together.

### Option 1 — Text Input

```bash
curl -X POST https://portal.toolweb.in/apis/security/mitre-attack-mapper/map-technique \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "input=Attacker used spearphishing email with malicious Office macro to gain initial access, then ran PowerShell to enumerate local users and dump credentials from LSASS memory"
```

### Option 2 — File Upload

```bash
curl -X POST https://portal.toolweb.in/apis/security/mitre-attack-mapper/map-technique \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "file=@incident_report.pdf"
```

### Option 3 — Text + File Combined

```bash
curl -X POST https://portal.toolweb.in/apis/security/mitre-attack-mapper/map-technique \
  -H "X-API-Key: YOUR_API_KEY" \
  -F "input=Focus on lateral movement and credential access techniques" \
  -F "file=@threat_intel_report.txt"
```

---

## Parameters

Request content type: `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input` | string | ❌ | Free-text description of attacker behavior, threat intelligence, or incident details. Default: empty string |
| `file` | binary file | ❌ | Upload a security report, threat intel document, SIEM alert export, or incident log (PDF, TXT, DOCX, CSV) |

> At least one of `input` or `file` should be provided for a meaningful result.

### What to put in `input`

Describe attacker behavior in plain language or paste raw threat intelligence. Examples:

- Incident narrative: *"Attacker gained access via phishing, established persistence using a scheduled task, and exfiltrated data to an external FTP server"*
- SIEM alert text: *"Suspicious PowerShell execution with encoded command, parent process: winword.exe"*
- Threat actor TTP summary: *"APT group used living-off-the-land binaries, disabled Windows Defender via registry modification, and moved laterally using PsExec"*
- CVE description: *"Exploit of public-facing application via SQL injection to achieve remote code execution"*

### What to upload as `file`

- Incident response reports (PDF, DOCX)
- Threat intelligence bulletins (PDF, TXT)
- SIEM/EDR alert exports (CSV, TXT)
- Penetration test findings (PDF, DOCX)
- Malware analysis reports (TXT, PDF)

---

## What You Get

- **Matched ATT&CK techniques** — technique IDs (e.g., T1566.001), names, and confidence scores
- **Tactic mapping** — which kill chain phase each technique belongs to (Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Exfiltration, Command & Control, Impact)
- **ATT&CK Navigator layer** — exportable technique coverage for visualization
- **Detection guidance** — log sources, SIEM queries, and indicators to look for per technique
- **Mitigation recommendations** — ATT&CK M-series mitigations mapped to each identified technique
- **Threat actor association** — known APT groups or threat actors that use the identified technique combination

---

## Example Output

```json
{
  "techniques_identified": 4,
  "confidence": "High",
  "mapped_techniques": [
    {
      "technique_id": "T1566.001",
      "technique_name": "Phishing: Spearphishing Attachment",
      "tactic": "Initial Access",
      "confidence": 0.95,
      "detection": "Monitor email gateway logs for Office documents with macros; alert on winword.exe spawning child processes",
      "mitigations": ["M1049 - Antivirus/Antimalware", "M1031 - Network Intrusion Prevention", "M1017 - User Training"]
    },
    {
      "technique_id": "T1059.001",
      "technique_name": "Command and Scripting Interpreter: PowerShell",
      "tactic": "Execution",
      "confidence": 0.92,
      "detection": "Enable PowerShell ScriptBlock logging (Event ID 4104); alert on encoded commands (-EncodedCommand)",
      "mitigations": ["M1049 - Antivirus/Antimalware", "M1038 - Execution Prevention", "M1026 - Privileged Account Management"]
    },
    {
      "technique_id": "T1087.001",
      "technique_name": "Account Discovery: Local Account",
      "tactic": "Discovery",
      "confidence": 0.88,
      "detection": "Monitor for net user, whoami /all, Get-LocalUser execution",
      "mitigations": ["M1028 - Operating System Configuration"]
    },
    {
      "technique_id": "T1003.001",
      "technique_name": "OS Credential Dumping: LSASS Memory",
      "tactic": "Credential Access",
      "confidence": 0.97,
      "detection": "Monitor for lsass.exe memory access (Sysmon Event ID 10); alert on procdump, mimikatz, Task Manager targeting lsass",
      "mitigations": ["M1043 - Credential Access Protection", "M1028 - Operating System Configuration", "M1026 - Privileged Account Management"]
    }
  ],
  "threat_actor_associations": ["APT29", "FIN7", "Lazarus Group"],
  "kill_chain_coverage": ["Initial Access", "Execution", "Discovery", "Credential Access"]
}
```

---

## API Reference

**Base URL:** `https://portal.toolweb.in/apis/security/mitre-attack-mapper`

| Endpoint | Method | Content-Type | Description |
|----------|--------|--------------|-------------|
| `/map-technique` | POST | `multipart/form-data` | Map text or file to MITRE ATT&CK techniques |

**Authentication:** Pass your API key as `X-API-Key` header or `mcp_api_key` argument via MCP.

---

## Pricing

| Plan | Daily Limit | Monthly Limit | Price |
|------|-------------|---------------|-------|
| Free | 5 / day | 50 / month | $0 |
| Developer | 20 / day | 500 / month | $39 |
| Professional | 200 / day | 5,000 / month | $99 |
| Enterprise | 100,000 / day | 1,000,000 / month | $299 |

---

## About

**ToolWeb.in** — 200+ security APIs, CISSP & CISM certified, built for enterprise security practitioners.

Platforms: Pay-per-run · API Gateway · MCP Server · OpenClaw · RapidAPI · YouTube

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in) (MCP Server)
- 🦞 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- ⚡ [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)
