---
name: IR Readiness Assessment
description: Comprehensive evaluation of incident response capabilities with maturity scoring and phase-based assessment framework.
---

# Overview

The IR Readiness Assessment API provides organizations with a structured, comprehensive evaluation of their incident response capabilities. This tool enables security teams to benchmark their IR maturity against industry standards, identify capability gaps, and track improvement over time through scored assessments across defined IR phases.

Built for security professionals who need to understand and improve their organization's ability to detect, respond to, and recover from security incidents, this API delivers objective maturity scoring based on detailed questionnaire responses. The assessment framework covers the full incident response lifecycle and provides actionable insights aligned with NIST, SANS, and industry best practices.

Ideal users include Chief Information Security Officers (CISOs), incident response managers, security consultants, and organizations undergoing compliance audits or maturity improvement programs.

## Usage

### Example Request

```json
{
  "sessionId": "ir-assessment-2024-001",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "ir-assessment-2024-001",
    "timestamp": "2024-01-15T10:30:00Z",
    "responses": {
      "q1_preparation": 4,
      "q2_detection": 3,
      "q3_containment": 3,
      "q4_eradication": 2,
      "q5_recovery": 2,
      "q6_lessons_learned": 1,
      "q7_tools_integration": 4,
      "q8_team_training": 2
    }
  }
}
```

### Example Response

```json
{
  "sessionId": "ir-assessment-2024-001",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z",
  "maturityScore": 2.625,
  "maturityLevel": "Defined",
  "phaseScores": {
    "preparation": 4.0,
    "detection": 3.0,
    "containment": 3.0,
    "eradication": 2.0,
    "recovery": 2.0,
    "lessons_learned": 1.0
  },
  "assessment_summary": {
    "overall_maturity": "Defined",
    "strengths": ["Strong preparation capabilities", "Good detection mechanisms"],
    "gaps": ["Eradication processes need improvement", "Recovery procedures incomplete"],
    "recommendations": [
      "Develop formalized eradication procedures",
      "Enhance recovery plan documentation",
      "Increase team training frequency"
    ]
  },
  "complianceMapping": {
    "nist_csf": "Respond.RP",
    "iso27035": "Maturity Level 2"
  }
}
```

## Endpoints

### GET /

**Health Check Endpoint**

Verifies API availability and basic connectivity.

**Method:** `GET`

**Path:** `/`

**Parameters:** None

**Response:** JSON object confirming service status.

---

### POST /api/ir-assessment/evaluate

**Evaluate IR Readiness Assessment**

Processes assessment responses and returns comprehensive maturity scoring, phase-based breakdowns, gap analysis, and recommendations.

**Method:** `POST`

**Path:** `/api/ir-assessment/evaluate`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessionId` | string | Yes | Unique identifier for the assessment session |
| `userId` | integer | No | Identifier of the user conducting the assessment |
| `timestamp` | string | Yes | ISO 8601 timestamp of the assessment submission |
| `assessmentData` | object | Yes | Container for assessment response data |
| `assessmentData.sessionId` | string | Yes | Session identifier matching parent sessionId |
| `assessmentData.timestamp` | string | Yes | Timestamp of assessment data capture |
| `assessmentData.responses` | object | Yes | Key-value pairs where keys are question identifiers and values are integer scores (typically 1-5) |

**Response Schema:**

- `sessionId` (string): Assessment session identifier
- `userId` (integer, nullable): User who conducted the assessment
- `timestamp` (string): Response generation timestamp
- `maturityScore` (number): Overall maturity score (0-5 scale)
- `maturityLevel` (string): Maturity rating (e.g., "Initial", "Repeatable", "Defined", "Managed", "Optimized")
- `phaseScores` (object): Scores for each IR phase (preparation, detection, containment, eradication, recovery, lessons_learned)
- `assessment_summary` (object): Contains overall_maturity, strengths, gaps, and recommendations arrays
- `complianceMapping` (object): Alignment with NIST CSF and ISO 27035 maturity models

---

### GET /api/ir-assessment/phases

**Retrieve Phase Definitions**

Returns definitions of all IR phases included in the assessment framework.

**Method:** `GET`

**Path:** `/api/ir-assessment/phases`

**Parameters:** None

**Response Schema:**

JSON object containing phase definitions, including:

- Phase identifiers and names
- Description of scope and objectives for each phase
- Key control areas and evaluation criteria
- Typical timeline and resource requirements

---

### GET /api/ir-assessment/maturity-levels

**Retrieve Maturity Level Definitions**

Returns framework definitions for maturity levels and scoring thresholds.

**Method:** `GET`

**Path:** `/api/ir-assessment/maturity-levels`

**Parameters:** None

**Response Schema:**

JSON object containing:

- Maturity level names and identifiers
- Score ranges for each level
- Characteristics and capabilities at each maturity stage
- Progression pathways and typical improvement recommendations

---

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/security/ir-readiness
- **API Docs:** https://api.mkkpro.com:8107/docs
