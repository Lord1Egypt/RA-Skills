---
name: Compliance Management Platform
description: Multi-framework compliance assessment and management system for evaluating organizational adherence to security and regulatory standards.
---

# Overview

The Compliance Management Platform is a comprehensive API for conducting multi-framework compliance assessments across your organization. Built for security professionals, compliance officers, and enterprise teams, this platform enables systematic evaluation of controls against industry-standard frameworks including ISO 27001, NIST CSF, SOC 2, and more.

This tool streamlines the compliance assessment workflow by providing centralized access to framework definitions, control specifications, and assessment execution. Organizations can evaluate their security posture against multiple frameworks simultaneously, track responses to specific controls, and generate compliance reports that demonstrate adherence to regulatory and industry standards.

Ideal users include security teams implementing compliance programs, organizations preparing for audits or certifications, managed service providers supporting multiple clients, and enterprises managing multi-framework compliance obligations across diverse business units.

# Usage

**Request:** Perform a comprehensive compliance assessment against ISO 27001 and NIST frameworks.

```json
{
  "assessment": {
    "frameworks": ["ISO27001", "NIST_CSF"],
    "organizationProfile": {
      "name": "Acme Corporation",
      "industry": "Technology",
      "employees": 250,
      "dataClassification": "Confidential"
    },
    "controlResponses": {
      "A.5.1": {
        "implemented": true,
        "evidence": "Policy documented in InfoSec handbook",
        "status": "compliant"
      },
      "AC-1": {
        "implemented": true,
        "evidence": "Access control procedures established",
        "status": "compliant"
      }
    },
    "sessionId": "session_12345",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionId": "session_12345",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response:** Assessment results with compliance scores and gap analysis.

```json
{
  "assessmentId": "assessment_67890",
  "status": "completed",
  "frameworks": {
    "ISO27001": {
      "score": 78,
      "controlsAssessed": 114,
      "controlsCompliant": 89,
      "gaps": [
        {
          "controlId": "A.12.1",
          "title": "Cryptography",
          "severity": "high",
          "remediation": "Implement encryption standards across data at rest and in transit"
        }
      ]
    },
    "NIST_CSF": {
      "score": 82,
      "categories": {
        "Identify": 85,
        "Protect": 80,
        "Detect": 75,
        "Respond": 88,
        "Recover": 80
      }
    }
  },
  "timestamp": "2024-01-15T10:31:45Z",
  "expiresAt": "2024-04-15T10:31:45Z"
}
```

# Endpoints

## GET /

**Health Check Endpoint**

Verifies that the Compliance Management Platform API is operational and responsive.

**Parameters:** None

**Response:**
- `200 OK`: Service is operational

---

## POST /api/compliance/assess

**Perform Comprehensive Compliance Assessment**

Executes a multi-framework compliance assessment based on organization profile and control responses. Evaluates adherence to selected compliance frameworks and generates detailed gap analysis and remediation recommendations.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assessment` | ComplianceAssessment | Yes | Assessment object containing framework selection, organization profile, and control response data |
| `assessment.frameworks` | Array[String] | Yes | List of framework identifiers to assess against (e.g., "ISO27001", "NIST_CSF", "SOC2") |
| `assessment.organizationProfile` | Object | Yes | Organization metadata including name, industry, size, and data classification level |
| `assessment.controlResponses` | Object | Yes | Mapping of control IDs to implementation status, evidence, and compliance status |
| `assessment.sessionId` | String | Yes | Unique session identifier for tracking assessment context |
| `assessment.timestamp` | String | Yes | ISO 8601 timestamp of assessment creation |
| `sessionId` | String | Yes | Session identifier for request tracking and audit logging |
| `userId` | Integer or Null | No | Identifier of the user initiating the assessment |
| `timestamp` | String | Yes | ISO 8601 timestamp of the request |

**Response:**
- `200 OK`: Assessment completed successfully with results, scores, and gap analysis
- `422 Unprocessable Entity`: Validation error in request body (see HTTPValidationError schema)

---

## GET /api/compliance/frameworks

**Get List of All Supported Frameworks**

Retrieves metadata and descriptions for all supported compliance frameworks available on the platform.

**Parameters:** None

**Response:**
- `200 OK`: Array of framework objects with IDs, names, descriptions, and applicable industries

---

## GET /api/compliance/framework/{framework_id}

**Get Detailed Framework Information**

Retrieves comprehensive details about a specific compliance framework including objectives, scope, applicability, and implementation guidance.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `framework_id` | String | Yes | Unique identifier of the framework (e.g., "ISO27001", "NIST_CSF", "SOC2", "GDPR") |

**Response:**
- `200 OK`: Framework details including description, objectives, domains/categories, and references
- `422 Unprocessable Entity`: Invalid framework_id format or missing parameter

---

## GET /api/compliance/controls/{framework_id}

**Get All Controls for Specific Framework**

Retrieves the complete control catalog for a specified framework, including control IDs, titles, descriptions, and implementation guidance.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `framework_id` | String | Yes | Unique identifier of the framework (e.g., "ISO27001", "NIST_CSF", "SOC2", "GDPR") |

**Response:**
- `200 OK`: Array of control objects with IDs, titles, descriptions, categories, severity levels, and implementation details
- `422 Unprocessable Entity`: Invalid framework_id format or missing parameter

# Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

# About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

# References

- Kong Route: https://api.mkkpro.com/compliance/management-platform
- API Docs: https://api.mkkpro.com:8103/docs
