# SOC 2 Readiness Checker

Evaluate your organization's readiness for a SOC 2 Type I or Type II audit across all five Trust Services Criteria — Security, Availability, Processing Integrity, Confidentiality, and Privacy. Provide your current control posture and get back a readiness score, gap analysis, and a prioritized remediation roadmap to achieve audit-ready status.

---

## Usage

```json
{
  "tool": "soc2_readiness_checker",
  "input": {
    "company_size": "Medium",
    "industry": "SaaS / Technology",
    "cloud_services": ["AWS", "Google Workspace", "Snowflake", "Salesforce"],
    "has_policies": true,
    "access_controls": true,
    "encryption_at_rest": true,
    "encryption_in_transit": true,
    "backup_procedures": true,
    "incident_response_plan": false,
    "vendor_management": false,
    "employee_training": false,
    "logging_monitoring": true,
    "change_management": false
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
| `industry` | string | Industry vertical (e.g., `SaaS / Technology`, `Financial Services`, `Healthcare`, `E-commerce`) |
| `cloud_services` | array of strings | Cloud platforms and SaaS tools in use. Examples: `AWS`, `Azure`, `GCP`, `Google Workspace`, `Microsoft 365`, `Snowflake`, `Salesforce`, `Okta` |

### Control Posture (boolean flags)

| Field | Type | Description |
|-------|------|-------------|
| `has_policies` | boolean | Formal information security policies documented and in effect |
| `access_controls` | boolean | Role-based access control and least-privilege enforced |
| `encryption_at_rest` | boolean | Data encrypted at rest across storage systems |
| `encryption_in_transit` | boolean | Data encrypted in transit (TLS/HTTPS enforced) |
| `backup_procedures` | boolean | Documented and tested data backup and recovery procedures |
| `incident_response_plan` | boolean | Formal incident response plan exists and has been tested |
| `vendor_management` | boolean | Third-party vendor risk management program in place |
| `employee_training` | boolean | Regular security awareness training conducted for all staff |
| `logging_monitoring` | boolean | Centralized logging and real-time security monitoring active |
| `change_management` | boolean | Formal change management process for systems and infrastructure |

---

## What You Get

- **Overall SOC 2 readiness score** — percentage score with readiness tier (Not Ready / Partially Ready / Nearly Ready / Audit Ready)
- **Trust Services Criteria breakdown** — gap analysis per TSC: Security (CC), Availability (A), Processing Integrity (PI), Confidentiality (C), Privacy (P)
- **Control gap list** — exactly which controls are missing or insufficient
- **Audit type recommendation** — whether to pursue Type I first or go directly to Type II
- **Prioritized remediation roadmap** — Immediate (0–30 days), Short-term (30–90 days), Long-term (90+ days)
- **Estimated time to audit readiness** — realistic timeline based on current posture
- **Evidence collection checklist** — what artifacts auditors will request

---

## Example Output

```json
{
  "company": "Acme SaaS Inc.",
  "overall_readiness_score": 61,
  "readiness_tier": "Partially Ready",
  "audit_type_recommendation": "Achieve Type I first (target: 90 days), then Type II",
  "estimated_time_to_ready": "3-4 months",
  "tsc_scores": {
    "security_cc": { "score": 70, "gaps": 2 },
    "availability": { "score": 80, "gaps": 1 },
    "processing_integrity": { "score": 50, "gaps": 2 },
    "confidentiality": { "score": 60, "gaps": 1 },
    "privacy": { "score": 40, "gaps": 2 }
  },
  "critical_gaps": [
    "No incident response plan — CC7.3, CC7.4 non-compliant",
    "No vendor management program — CC9.2 non-compliant",
    "No security awareness training — CC1.4 non-compliant",
    "No change management process — CC8.1 non-compliant"
  ],
  "immediate_actions": [
    "Draft and approve Incident Response Plan (14 days)",
    "Implement vendor risk questionnaire for all third parties (21 days)",
    "Schedule and complete first security awareness training cycle (30 days)"
  ],
  "evidence_checklist": [
    "Access control configuration screenshots",
    "Encryption settings documentation",
    "Backup test results (last 90 days)",
    "Security policy sign-off records",
    "Audit log samples"
  ]
}
```

---

## API Reference

**Base URL:** `https://portal.toolweb.in/apis/compliance/soc2-readiness`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/soc2-assessment` | POST | Run full SOC 2 readiness assessment |

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
