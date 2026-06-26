# ISO 27001 Policy Generator

Generate tailored ISO 27001 information security policies for your organization. Provide your company profile, infrastructure context, and compliance requirements — get back a complete set of ready-to-use policy documents aligned to ISO/IEC 27001:2022 controls. Covers all Annex A domains including access control, cryptography, supplier relationships, incident management, and more.

---

## Usage

```json
{
  "tool": "iso27001_policy_generator",
  "input": {
    "company_name": "Vertex Technologies Pvt Ltd",
    "company_size": "Medium",
    "industry": "Financial Services",
    "country": "India",
    "has_existing_policies": false,
    "policy_types": [
      "Information Security Policy",
      "Access Control Policy",
      "Acceptable Use Policy",
      "Incident Response Policy",
      "Data Classification Policy"
    ],
    "compliance_requirements": ["ISO 27001", "RBI Guidelines", "GDPR"],
    "business_locations": ["Mumbai", "Bangalore", "Singapore"],
    "it_infrastructure": ["On-premise Servers", "AWS Cloud", "SaaS Applications", "VPN"],
    "data_types": ["Customer PII", "Financial Records", "Employee Data", "Intellectual Property"],
    "third_party_vendors": true,
    "remote_work": true,
    "cloud_services": true,
    "mobile_devices": true,
    "data_retention_years": 7
  }
}
```

---

## Parameters

All fields are **required**.

### Company Profile

| Field | Type | Description |
|-------|------|-------------|
| `company_name` | string | Name of the organization |
| `company_size` | string | `Small`, `Medium`, `Large`, `Enterprise` |
| `industry` | string | Industry vertical (e.g., Financial Services, Healthcare, Technology, Retail) |
| `country` | string | Primary country of operation |
| `has_existing_policies` | boolean | Whether the organization already has some security policies in place |
| `data_retention_years` | integer | Number of years data must be retained per regulatory/business requirement |

### Policy Scope

| Field | Type | Description |
|-------|------|-------------|
| `policy_types` | array of strings | Specific policies to generate. Examples: `Information Security Policy`, `Access Control Policy`, `Acceptable Use Policy`, `Cryptography Policy`, `Incident Response Policy`, `Business Continuity Policy`, `Supplier Security Policy`, `Data Classification Policy`, `Change Management Policy`, `Physical Security Policy` |
| `compliance_requirements` | array of strings | Regulations/frameworks to align with. Examples: `ISO 27001`, `GDPR`, `SOC 2`, `PCI DSS`, `HIPAA`, `RBI Guidelines`, `SEBI` |
| `business_locations` | array of strings | Cities/countries where the organization operates |

### Infrastructure Context

| Field | Type | Description |
|-------|------|-------------|
| `it_infrastructure` | array of strings | Infrastructure components in use. Examples: `On-premise Servers`, `AWS Cloud`, `Azure`, `GCP`, `SaaS Applications`, `VPN`, `Active Directory`, `Kubernetes` |
| `data_types` | array of strings | Types of data handled. Examples: `Customer PII`, `Financial Records`, `Employee Data`, `Health Records`, `Intellectual Property`, `Source Code` |
| `third_party_vendors` | boolean | Whether third-party vendors have access to systems or data |
| `remote_work` | boolean | Whether remote/hybrid work is practised |
| `cloud_services` | boolean | Whether cloud services are used |
| `mobile_devices` | boolean | Whether mobile devices are used to access company systems or data |

---

## What You Get

- **Complete policy documents** — fully drafted, organization-specific ISO 27001 policies ready for review and adoption
- **Annex A control mapping** — each policy mapped to relevant ISO 27001:2022 Annex A controls
- **Multi-framework alignment** — policies cross-referenced with your stated compliance requirements (GDPR, PCI DSS, SOC 2, etc.)
- **Scope and applicability statements** — tailored to your infrastructure, locations, and workforce model
- **Review and approval guidance** — suggested review cycles, ownership assignments, and version control notes
- **Implementation checklist** — step-by-step actions to operationalize each policy

---

## Example Output

```json
{
  "organization": "Vertex Technologies Pvt Ltd",
  "policies_generated": 5,
  "iso27001_version": "ISO/IEC 27001:2022",
  "policies": [
    {
      "title": "Information Security Policy",
      "annex_a_controls": ["5.1", "5.2", "5.3"],
      "compliance_alignment": ["ISO 27001", "GDPR Article 32"],
      "sections": [
        "Purpose and Scope",
        "Management Commitment",
        "Roles and Responsibilities",
        "Policy Statements",
        "Enforcement and Review"
      ],
      "review_cycle": "Annual",
      "owner": "Chief Information Security Officer"
    },
    {
      "title": "Access Control Policy",
      "annex_a_controls": ["8.2", "8.3", "8.4", "8.5", "8.6"],
      "compliance_alignment": ["ISO 27001", "RBI Guidelines", "GDPR"],
      "sections": [
        "Access Request and Approval",
        "Privileged Access Management",
        "Password Requirements",
        "Remote Access Controls",
        "Access Review and Revocation"
      ],
      "review_cycle": "Annual",
      "owner": "IT Security Manager"
    }
  ],
  "implementation_checklist": [
    "Assign policy owners for each document",
    "Schedule management review and sign-off",
    "Publish to internal knowledge base/intranet",
    "Conduct workforce awareness training",
    "Set calendar reminders for annual review"
  ]
}
```

---

## API Reference

**Base URL:** `https://portal.toolweb.in/apis/compliance/iso27001-policy`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/iso27001-policies` | POST | Generate ISO 27001 policy documents |

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
