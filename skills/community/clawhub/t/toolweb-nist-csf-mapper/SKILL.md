# NIST CSF Mapper

Map your organization's current security controls and tooling to the NIST Cybersecurity Framework (CSF) 2.0. Provide your company profile, existing security tools, and control posture — get back a function-by-function CSF coverage report, gap analysis, maturity tier rating, and a prioritized improvement roadmap across all six CSF functions: Govern, Identify, Protect, Detect, Respond, and Recover.

---

## Usage

```json
{
  "tool": "nist_csf_mapper",
  "input": {
    "company_size": "Medium",
    "industry": "Financial Services",
    "current_tools": ["Palo Alto Firewall", "CrowdStrike EDR", "Splunk SIEM", "Tenable Nessus", "AWS Backup", "KnowBe4"],
    "has_firewall": true,
    "has_antivirus": true,
    "has_backup_system": true,
    "has_monitoring": true,
    "has_incident_response": false,
    "has_access_controls": true,
    "has_data_encryption": true,
    "has_vulnerability_scanning": true,
    "has_security_training": true,
    "has_business_continuity": false,
    "regulatory_requirements": ["PCI DSS", "GDPR", "RBI Guidelines"]
  }
}
```

---

## Parameters

All fields are **required**.

### Company Profile

| Field | Type | Description |
|-------|------|-------------|
| `company_size` | string | `Small`, `Medium`, `Large`, `Enterprise` |
| `industry` | string | Industry vertical (e.g., `Financial Services`, `Healthcare`, `Manufacturing`, `Technology`, `Retail`, `Energy`) |
| `current_tools` | array of strings | Security tools currently deployed. Examples: `Palo Alto Firewall`, `CrowdStrike EDR`, `Splunk SIEM`, `Tenable Nessus`, `Okta`, `CyberArk`, `AWS Security Hub`, `KnowBe4`, `Veeam Backup` |
| `regulatory_requirements` | array of strings | Applicable regulations/frameworks. Examples: `PCI DSS`, `HIPAA`, `GDPR`, `SOC 2`, `ISO 27001`, `NIST 800-53`, `RBI Guidelines`, `SEBI` |

### Control Posture (boolean flags)

| Field | Type | Description |
|-------|------|-------------|
| `has_firewall` | boolean | Network firewall deployed and actively managed |
| `has_antivirus` | boolean | Antivirus/EDR solution in place across endpoints |
| `has_backup_system` | boolean | Automated data backup system operational |
| `has_monitoring` | boolean | Security monitoring / SIEM solution active |
| `has_incident_response` | boolean | Formal incident response plan documented and tested |
| `has_access_controls` | boolean | Identity and access management controls implemented |
| `has_data_encryption` | boolean | Data encryption at rest and in transit enforced |
| `has_vulnerability_scanning` | boolean | Regular vulnerability scanning conducted |
| `has_security_training` | boolean | Security awareness training program in place |
| `has_business_continuity` | boolean | Business continuity and disaster recovery plan exists |

---

## What You Get

- **CSF function-by-function coverage** — maturity score across Govern, Identify, Protect, Detect, Respond, Recover
- **NIST CSF Tier rating** — overall tier assessment (Tier 1 Partial → Tier 4 Adaptive)
- **Subcategory gap map** — which specific CSF subcategories (e.g., ID.AM-1, PR.AC-3) are covered, partial, or missing
- **Tool-to-CSF mapping** — how your existing tools map to CSF functions and subcategories
- **Regulatory crosswalk** — how CSF gaps align to your stated compliance requirements
- **Prioritized improvement roadmap** — Quick Wins (0–30 days), Short-term (30–90 days), Strategic (90+ days)
- **Executive summary** — board-ready posture summary with tier rating and top risks

---

## Example Output

```json
{
  "organization": "Acme Financial",
  "csf_version": "NIST CSF 2.0",
  "overall_tier": "Tier 2 — Risk Informed",
  "overall_score": 68,
  "function_scores": {
    "govern": { "score": 55, "tier": "Tier 2", "gaps": 3 },
    "identify": { "score": 70, "tier": "Tier 2", "gaps": 2 },
    "protect": { "score": 80, "tier": "Tier 3", "gaps": 1 },
    "detect": { "score": 75, "tier": "Tier 3", "gaps": 1 },
    "respond": { "score": 40, "tier": "Tier 1", "gaps": 4 },
    "recover": { "score": 35, "tier": "Tier 1", "gaps": 3 }
  },
  "tool_mapping": [
    { "tool": "Palo Alto Firewall", "csf_functions": ["Protect (PR.AC, PR.PT)"] },
    { "tool": "CrowdStrike EDR", "csf_functions": ["Detect (DE.CM)", "Respond (RS.AN)"] },
    { "tool": "Splunk SIEM", "csf_functions": ["Detect (DE.CM, DE.AE)", "Respond (RS.AN)"] },
    { "tool": "Tenable Nessus", "csf_functions": ["Identify (ID.RA)", "Protect (PR.IP)"] }
  ],
  "critical_gaps": [
    "No incident response plan — RS.RP-1, RS.CO-1 not met",
    "No business continuity plan — RC.RP-1, RC.CO-3 not met",
    "Govern function weak — GV.OC, GV.RM subcategories not addressed",
    "No formal asset inventory process — ID.AM-1, ID.AM-2 partial"
  ],
  "regulatory_crosswalk": {
    "PCI_DSS": ["Requirement 12.10 (IR plan)", "Requirement 12.3 (risk assessment)"],
    "GDPR": ["Article 32 (security measures)", "Article 33 (breach notification)"]
  },
  "quick_wins": [
    "Document and approve Incident Response Plan (14 days)",
    "Create asset inventory register using existing SIEM data (7 days)",
    "Define cybersecurity roles and responsibilities in a RACI matrix (10 days)"
  ]
}
```

---

## API Reference

**Base URL:** `https://portal.toolweb.in/apis/compliance/nist-csf-mapper`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/nist-mapping` | POST | Map security controls to NIST CSF 2.0 and generate gap report |

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

**ToolWeb.in** — 200+ security APIs, CISSP & CISM certified, built for enterprise compliance practitioners.

Platforms: Pay-per-run · API Gateway · MCP Server · OpenClaw · RapidAPI · YouTube

- 🌐 [toolweb.in](https://toolweb.in)
- 🔌 [portal.toolweb.in](https://portal.toolweb.in)
- 🤖 [hub.toolweb.in](https://hub.toolweb.in) (MCP Server)
- 🦞 [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- ⚡ [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- 📺 [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)
