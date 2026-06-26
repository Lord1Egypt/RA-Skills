---
name: Chain of Custody Manager API
description: Generates forensic chain of custody HTML reports for evidence management and legal compliance.
---

# Overview

The Chain of Custody Manager API is a forensic documentation tool designed to generate compliant, legally-defensible chain of custody reports in HTML format. It serves law enforcement, digital forensics teams, corporate investigations, and legal departments that need to maintain rigorous evidence handling documentation for court admissibility and regulatory compliance.

This API automates the creation of formal custody chain documentation by organizing evidence metadata, handler information, timestamps, and integrity hashes into professional reports. Each report captures the complete lifecycle of evidence from collection through transfer, ensuring no breaks in the documented chain and protecting evidence integrity.

Ideal users include forensic examiners, incident response teams, corporate security practitioners, and legal professionals who must demonstrate proper evidence handling procedures in investigations, litigation, or regulatory audits.

# Usage

**Example Request:**

```json
{
  "reportData": {
    "caseInfo": {
      "caseNumber": "2024-INV-00145",
      "caseName": "Data Breach Investigation - Corp A",
      "investigator": "Detective John Smith",
      "organization": "Cyber Crimes Unit",
      "reportDate": "2024-01-15T10:30:00Z"
    },
    "evidenceItems": [
      {
        "evidenceId": "EV-2024-001",
        "evidenceType": "Hard Drive",
        "description": "Seagate 2TB external drive from suspect workstation",
        "collectionDate": "2024-01-10T14:22:00Z",
        "collectionLocation": "Building A, Floor 3, Room 301",
        "collectedBy": "Officer Jane Doe",
        "hashAlgorithm": "SHA-256",
        "hashValue": "a7f3c8e2d9b1f4e6c2a5d8f1b3e6a9c2d5e8f1b4a7c0d3e6f9a2b5c8e1f4",
        "custodyChain": [
          {
            "person": "Officer Jane Doe",
            "timestamp": "2024-01-10T14:22:00Z",
            "purpose": "Initial collection",
            "action": "Collected from workstation"
          },
          {
            "person": "Detective John Smith",
            "timestamp": "2024-01-10T16:45:00Z",
            "purpose": "Evidence intake",
            "action": "Received and logged into evidence management system"
          },
          {
            "person": "Forensic Tech Mike Johnson",
            "timestamp": "2024-01-12T09:15:00Z",
            "purpose": "Digital forensic examination",
            "action": "Imaged drive and verified hash"
          }
        ]
      }
    ],
    "sessionId": "sess-2024-001-xyz"
  },
  "sessionId": "sess-2024-001-xyz",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z",
  "userEmail": "john.smith@agency.gov",
  "userName": "jsmith"
}
```

**Example Response:**

```json
{
  "status": "success",
  "reportId": "RPT-2024-145-001",
  "htmlReport": "<!DOCTYPE html><html>...[complete HTML custody report]...</html>",
  "message": "Chain of Custody report generated successfully"
}
```

# Endpoints

## GET /

**Summary:** Root endpoint

**Description:** Returns API information and status.

**Parameters:** None

**Response:** JSON object with API metadata.

---

## POST /api/custody/generate

**Summary:** Generate Custody Report

**Description:** Generates a formatted Chain of Custody HTML report containing case information, evidence details, and custody chain history.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| reportData | object | Yes | Contains caseInfo, evidenceItems, and sessionId |
| reportData.caseInfo | object | Yes | Case metadata including caseNumber, caseName, investigator, organization, reportDate |
| reportData.caseInfo.caseNumber | string | Yes | Unique case identifier |
| reportData.caseInfo.caseName | string | Yes | Human-readable case name |
| reportData.caseInfo.investigator | string | Yes | Name of lead investigator |
| reportData.caseInfo.organization | string | Yes | Law enforcement or organizational unit |
| reportData.caseInfo.reportDate | string | Yes | ISO 8601 timestamp of report generation |
| reportData.evidenceItems | array | Yes | Array of EvidenceItem objects |
| reportData.evidenceItems[].evidenceId | string | Yes | Unique evidence identifier |
| reportData.evidenceItems[].evidenceType | string | Yes | Category of evidence (e.g., "Hard Drive", "Mobile Device", "Documents") |
| reportData.evidenceItems[].description | string | Yes | Detailed description of the evidence |
| reportData.evidenceItems[].collectionDate | string | Yes | ISO 8601 timestamp when evidence was collected |
| reportData.evidenceItems[].collectionLocation | string | Yes | Physical or logical location where evidence was collected |
| reportData.evidenceItems[].collectedBy | string | Yes | Name of person who collected the evidence |
| reportData.evidenceItems[].hashAlgorithm | string | Yes | Hash algorithm used (e.g., "SHA-256", "MD5") |
| reportData.evidenceItems[].hashValue | string | Yes | Computed hash value for integrity verification |
| reportData.evidenceItems[].custodyChain | array | Yes | Array of CustodyEntry objects documenting evidence transfers |
| reportData.evidenceItems[].custodyChain[].person | string | Yes | Name of person handling evidence |
| reportData.evidenceItems[].custodyChain[].timestamp | string | Yes | ISO 8601 timestamp of custody event |
| reportData.evidenceItems[].custodyChain[].purpose | string | Yes | Purpose of custody transfer (e.g., "Initial collection", "Examination") |
| reportData.evidenceItems[].custodyChain[].action | string | Yes | Description of action taken |
| reportData.sessionId | string | Yes | Session identifier within report data |
| sessionId | string | Yes | Session identifier for API request |
| userId | integer | Yes | Numeric user identifier making the request |
| timestamp | string | Yes | ISO 8601 timestamp of API request |
| userEmail | string | No | Email address of user (optional) |
| userName | string | No | Username of user (optional) |

**Response:**

```json
{
  "status": "success",
  "reportId": "string",
  "htmlReport": "string",
  "message": "string"
}
```

**Error Response (422):**

```json
{
  "detail": [
    {
      "loc": ["body", "fieldname"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

---

## GET /api/custody/health

**Summary:** Health Check

**Description:** Verifies API availability and operational status.

**Parameters:** None

**Response:** JSON object with health status and timestamp.

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

- **Kong Route:** https://api.mkkpro.com/compliance/chain-of-custody
- **API Docs:** https://api.mkkpro.com:8115/docs
