---
name: Security Posture Maturity Assessment
description: Professional multi-dimensional security maturity evaluation platform that assesses organizational security across eight critical domains.
---

# Overview

The Security Posture Maturity Assessment API provides a comprehensive, professional-grade evaluation framework for measuring organizational security maturity across multiple dimensions. This platform enables security teams, compliance officers, and enterprise architects to systematically assess their security posture against industry-standard maturity levels and identify gaps in critical security domains.

The tool evaluates eight essential security domains: Network Security, Cloud Security, Endpoint Security, Identity & Access Management, Data Security, Application Security, Physical Security, and Governance & Compliance. Each domain is rated on a 1-5 maturity scale, providing granular visibility into organizational security strengths and weaknesses.

This API is ideal for enterprises conducting security audits, preparing for compliance assessments, benchmarking against industry standards, and developing strategic security improvement roadmaps. Organizations can track maturity progression over time and generate actionable intelligence for board-level and operational security governance.

# Usage

## Sample Request

```json
{
  "assessmentData": {
    "network_security": 3,
    "cloud_security": 2,
    "endpoint_security": 4,
    "identity_access": 3,
    "data_security": 2,
    "application_security": 3,
    "physical_security": 4,
    "governance_compliance": 2
  },
  "sessionId": "sess_20240115_acme_corp",
  "userId": 12847,
  "timestamp": "2024-01-15T14:30:00Z"
}
```

## Sample Response

```json
{
  "assessmentId": "assess_67890abcdef",
  "organizationScore": 2.875,
  "maturityLevel": "Managed",
  "timestamp": "2024-01-15T14:30:15Z",
  "domainScores": {
    "network_security": {
      "score": 3,
      "maturityLevel": "Defined",
      "status": "Moderate"
    },
    "cloud_security": {
      "score": 2,
      "maturityLevel": "Repeatable",
      "status": "Below Target"
    },
    "endpoint_security": {
      "score": 4,
      "maturityLevel": "Managed",
      "status": "Strong"
    },
    "identity_access": {
      "score": 3,
      "maturityLevel": "Defined",
      "status": "Moderate"
    },
    "data_security": {
      "score": 2,
      "maturityLevel": "Repeatable",
      "status": "Below Target"
    },
    "application_security": {
      "score": 3,
      "maturityLevel": "Defined",
      "status": "Moderate"
    },
    "physical_security": {
      "score": 4,
      "maturityLevel": "Managed",
      "status": "Strong"
    },
    "governance_compliance": {
      "score": 2,
      "maturityLevel": "Repeatable",
      "status": "Below Target"
    }
  },
  "recommendations": [
    {
      "domain": "cloud_security",
      "priority": "High",
      "action": "Implement cloud security baseline controls and automation"
    },
    {
      "domain": "data_security",
      "priority": "High",
      "action": "Establish data classification and encryption standards"
    }
  ]
}
```

# Endpoints

## GET /

**Health Check Endpoint**

Verifies API service availability and health status.

**Method:** GET  
**Path:** `/`

**Parameters:** None

**Response:**
- **Status 200:** Service operational (JSON object)

---

## POST /api/maturity/assess

**Generate Maturity Assessment**

Generates a comprehensive security maturity assessment based on provided domain scores and organizational context.

**Method:** POST  
**Path:** `/api/maturity/assess`

**Request Body Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `assessmentData` | AssessmentData object | Yes | Container for all eight security domain scores |
| `assessmentData.network_security` | Integer (1-5) | Yes | Network Security maturity score |
| `assessmentData.cloud_security` | Integer (1-5) | Yes | Cloud Security maturity score |
| `assessmentData.endpoint_security` | Integer (1-5) | Yes | Endpoint Security maturity score |
| `assessmentData.identity_access` | Integer (1-5) | Yes | Identity & Access Management maturity score |
| `assessmentData.data_security` | Integer (1-5) | Yes | Data Security maturity score |
| `assessmentData.application_security` | Integer (1-5) | Yes | Application Security maturity score |
| `assessmentData.physical_security` | Integer (1-5) | Yes | Physical Security maturity score |
| `assessmentData.governance_compliance` | Integer (1-5) | Yes | Governance & Compliance maturity score |
| `sessionId` | String | Yes | Unique session identifier for tracking |
| `userId` | Integer | No | User identifier (optional) |
| `timestamp` | String | Yes | ISO 8601 formatted timestamp of assessment |

**Response:**
- **Status 200:** Assessment generated successfully (JSON object with domain scores, overall maturity level, and recommendations)
- **Status 422:** Validation error in request body (missing required fields or invalid score ranges)

---

## GET /api/maturity/domains

**Get Security Domains**

Retrieves the complete list of available security domains and their definitions.

**Method:** GET  
**Path:** `/api/maturity/domains`

**Parameters:** None

**Response:**
- **Status 200:** JSON array of security domain definitions including domain name, description, and assessment criteria

---

## GET /api/maturity/levels

**Get Maturity Levels**

Retrieves definitions and characteristics of each maturity level used in assessments.

**Method:** GET  
**Path:** `/api/maturity/levels`

**Parameters:** None

**Response:**
- **Status 200:** JSON object containing maturity level definitions (e.g., Initial, Repeatable, Defined, Managed, Optimized) with descriptions and requirements for each level

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

- **Kong Route:** https://api.mkkpro.com/security/security-posture-maturity
- **API Docs:** https://api.mkkpro.com:8121/docs
