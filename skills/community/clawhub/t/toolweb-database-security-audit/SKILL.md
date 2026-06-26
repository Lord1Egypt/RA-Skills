---
name: Database Security Audit API
description: Comprehensive API for processing database security audits and generating detailed compliance reports across access control, encryption, network security, and backup domains.
---

# Overview

The Database Security Audit API is a backend service designed for organizations that need to systematically evaluate and document their database security posture. It processes security audit data across multiple control domains—including access control, encryption, network security, auditing, and backup—and generates comprehensive compliance reports that measure implementation against total security controls.

This API is ideal for security teams, compliance officers, database administrators, and organizations undergoing regulatory assessments (SOC 2, ISO 27001, HIPAA, PCI-DSS, etc.). It provides a structured method to collect, validate, and report on database security configurations in a standardized format.

The service maintains audit trails with session tracking and timestamps, enabling organizations to monitor security posture over time and demonstrate continuous compliance to internal and external stakeholders.

## Usage

**Example Request:**

```json
{
  "auditData": {
    "sessionId": "audit-session-2024-01-15-001",
    "timestamp": "2024-01-15T10:30:00Z",
    "totalControls": 50,
    "implementedControls": 45,
    "access_control": [
      "Role-based access control (RBAC) implemented",
      "Principle of least privilege enforced",
      "Service accounts use strong credentials"
    ],
    "encryption": [
      "Data at rest encrypted with AES-256",
      "TLS 1.3 enabled for data in transit",
      "Key management system in place"
    ],
    "network_security": [
      "Database isolated in secure VPC",
      "Firewall rules restrict database access",
      "Network segmentation implemented"
    ],
    "auditing": [
      "Query logging enabled",
      "Failed authentication attempts logged",
      "Administrative actions audited"
    ],
    "backup": [
      "Automated daily backups scheduled",
      "Backups tested monthly",
      "Off-site backup replication enabled"
    ],
    "additional": [
      "Vulnerability scanning quarterly",
      "Patch management process defined"
    ]
  },
  "sessionId": "audit-session-2024-01-15-001",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Example Response:**

```json
{
  "status": "success",
  "sessionId": "audit-session-2024-01-15-001",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z",
  "auditSummary": {
    "totalControls": 50,
    "implementedControls": 45,
    "compliancePercentage": 90.0,
    "controlsByDomain": {
      "access_control": 3,
      "encryption": 3,
      "network_security": 3,
      "auditing": 3,
      "backup": 3,
      "additional": 2
    }
  },
  "reportId": "report-2024-01-15-001",
  "processedAt": "2024-01-15T10:30:15Z"
}
```

## Endpoints

### GET /
**Health Check Endpoint**

Returns a simple health status response to verify API availability.

**Parameters:** None

**Response:**
- Status 200: JSON object confirming API is operational

---

### POST /api/database/audit
**Process Audit**

Processes database security audit data and generates a comprehensive compliance report. This is the primary endpoint for submitting audit findings and retrieving analysis.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| auditData | Object | Yes | Container object holding all audit control findings |
| auditData.sessionId | string | Yes | Unique identifier for this audit session |
| auditData.timestamp | string | Yes | ISO 8601 timestamp of audit execution |
| auditData.totalControls | integer | Yes | Total number of security controls evaluated |
| auditData.implementedControls | integer | Yes | Number of controls found to be implemented |
| auditData.access_control | array[string] | No | Array of access control findings and observations |
| auditData.encryption | array[string] | No | Array of encryption-related control findings |
| auditData.network_security | array[string] | No | Array of network security control findings |
| auditData.auditing | array[string] | No | Array of auditing and logging control findings |
| auditData.backup | array[string] | No | Array of backup and disaster recovery findings |
| auditData.additional | array[string] | No | Array of additional or custom control findings |
| sessionId | string | Yes | Session identifier (typically matches auditData.sessionId) |
| userId | integer | Yes | Numeric user ID of the audit initiator |
| timestamp | string | Yes | ISO 8601 timestamp of request submission |

**Response (200):**
- Audit report object containing compliance summary, control breakdown by domain, compliance percentage, and report reference ID

**Response (422):**
- Validation error detailing missing or improperly formatted required fields

---

### GET /health
**Detailed Health Check**

Provides extended health status information about the API service.

**Parameters:** None

**Response:**
- Status 200: JSON object with service health details (uptime, dependencies, version info)

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

- **Kong Route:** https://api.mkkpro.com/compliance/database-audit
- **API Docs:** https://api.mkkpro.com:8117/docs
