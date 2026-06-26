---
name: SABSA Security Architecture Assessment
description: Professional enterprise security architecture maturity analysis platform based on the SABSA framework.
---

# Overview

The SABSA Security Architecture Assessment tool provides comprehensive evaluation of enterprise security architecture maturity using the industry-standard Sherwood Applied Business Security Architecture (SABSA) framework. Designed for security architects, enterprise security leaders, and governance professionals, this platform delivers detailed assessments across multiple architectural layers and dimensions.

This tool enables organizations to measure their security architecture maturity, identify capability gaps, and establish roadmaps for security program enhancement. By analyzing organizational assets, processes, people, locations, motivations, and temporal factors across SABSA layers, the assessment provides actionable insights aligned with business objectives and compliance requirements.

Ideal users include Chief Information Security Officers (CISOs), security architects, enterprise risk managers, compliance officers, and organizations seeking structured approaches to security architecture governance and maturity benchmarking.

## Usage

### Sample Request

```json
{
  "sessionId": "session-2024-001-abc",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "session-2024-001-abc",
    "timestamp": "2024-01-15T10:30:00Z",
    "layers": {
      "contextual": {
        "assets": [
          {
            "name": "Customer Data Repository",
            "classification": "Confidential",
            "value": "Critical"
          }
        ],
        "motivation": [
          {
            "objective": "Data Protection",
            "priority": "High"
          }
        ],
        "process": [
          {
            "name": "Data Encryption Process",
            "status": "Implemented"
          }
        ],
        "people": [
          {
            "role": "Data Steward",
            "count": 5,
            "trained": true
          }
        ],
        "location": [
          {
            "datacenter": "Primary US East",
            "compliance": "SOC 2"
          }
        ],
        "time": [
          {
            "phase": "Operational",
            "duration": "24/7"
          }
        ]
      },
      "conceptual": {
        "assets": [],
        "motivation": [],
        "process": [],
        "people": [],
        "location": [],
        "time": []
      }
    }
  }
}
```

### Sample Response

```json
{
  "status": "success",
  "sessionId": "session-2024-001-abc",
  "assessmentId": "assess-2024-001-xyz",
  "timestamp": "2024-01-15T10:30:45Z",
  "maturityScores": {
    "contextual": {
      "overall": 3.2,
      "assets": 3.5,
      "motivation": 3.0,
      "process": 3.1,
      "people": 2.8,
      "location": 3.3,
      "time": 3.0
    },
    "conceptual": {
      "overall": 2.1,
      "assets": 2.0,
      "motivation": 2.2,
      "process": 2.1,
      "people": 2.0,
      "location": 2.0,
      "time": 2.0
    }
  },
  "recommendations": [
    {
      "layer": "contextual",
      "dimension": "people",
      "finding": "Security awareness training coverage at 80%",
      "priority": "High",
      "action": "Expand training program to achieve 100% coverage"
    }
  ],
  "gaps": [
    {
      "layer": "conceptual",
      "dimension": "process",
      "gap": "Absence of formal security architecture review process",
      "impact": "Medium"
    }
  ]
}
```

## Endpoints

### GET /
Health check endpoint for service availability verification.

**Method:** GET  
**Path:** `/`  
**Description:** Returns service status and availability confirmation.

**Parameters:** None

**Response:**
- **200 OK**: Service is operational
  - Content-Type: `application/json`
  - Schema: Empty object `{}`

---

### POST /api/sabsa/assessment
Generate a comprehensive SABSA security architecture assessment based on provided organizational data.

**Method:** POST  
**Path:** `/api/sabsa/assessment`  
**Description:** Generates detailed maturity assessment across SABSA framework layers and dimensions.

**Request Body Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessionId` | string | Yes | Unique identifier for the assessment session |
| `userId` | integer \| null | No | User identifier for audit and tracking purposes |
| `timestamp` | string | Yes | ISO 8601 timestamp of assessment initiation |
| `assessmentData` | object | Yes | Core assessment data containing layer evaluations |
| `assessmentData.sessionId` | string | Yes | Session identifier matching parent sessionId |
| `assessmentData.timestamp` | string | Yes | Assessment timestamp (ISO 8601 format) |
| `assessmentData.layers` | object | Yes | Multi-dimensional layer data (keys: layer names, values: LayerData objects) |
| `assessmentData.layers[layer].assets` | array | No | Asset inventory objects (default: empty array) |
| `assessmentData.layers[layer].motivation` | array | No | Business motivation and objectives objects (default: empty array) |
| `assessmentData.layers[layer].process` | array | No | Process and procedure objects (default: empty array) |
| `assessmentData.layers[layer].people` | array | No | Personnel and role objects (default: empty array) |
| `assessmentData.layers[layer].location` | array | No | Geographic and physical location objects (default: empty array) |
| `assessmentData.layers[layer].time` | array | No | Temporal and lifecycle phase objects (default: empty array) |

**Response:**
- **200 OK**: Assessment generated successfully
  - Content-Type: `application/json`
  - Schema: Assessment results with maturity scores, findings, and recommendations
- **422 Validation Error**: Request validation failed
  - Content-Type: `application/json`
  - Schema: HTTPValidationError containing validation error details

---

### GET /api/sabsa/framework
Retrieve SABSA framework reference information and structure.

**Method:** GET  
**Path:** `/api/sabsa/framework`  
**Description:** Returns framework definitions, layer descriptions, dimensions, and architectural principles.

**Parameters:** None

**Response:**
- **200 OK**: Framework information retrieved successfully
  - Content-Type: `application/json`
  - Schema: SABSA framework structure including layers, dimensions, and reference documentation

---

### GET /api/sabsa/maturity-levels
Retrieve maturity level definitions and progression criteria.

**Method:** GET  
**Path:** `/api/sabsa/maturity-levels`  
**Description:** Returns maturity level scale, definitions, characteristics, and assessment criteria.

**Parameters:** None

**Response:**
- **200 OK**: Maturity levels retrieved successfully
  - Content-Type: `application/json`
  - Schema: Maturity level definitions (typically levels 0-5) with descriptions and assessment thresholds

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

- **Kong Route:** https://api.mkkpro.com/compliance/sabsa-architecture
- **API Docs:** https://api.mkkpro.com:8102/docs
