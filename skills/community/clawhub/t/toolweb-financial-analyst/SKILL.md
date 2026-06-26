---
name: Financial Analyst Roadmap
description: Professional career roadmap platform that generates personalized learning paths and specialization recommendations for aspiring financial analysts.
---

# Overview

The Financial Analyst Roadmap API is a comprehensive career development platform designed to guide professionals through structured pathways to becoming a financial analyst. It leverages personalized assessment data to create tailored roadmaps that align with individual experience levels, skill sets, and career aspirations.

This platform is ideal for career changers, recent graduates, and working professionals seeking to transition into or advance within financial analysis roles. The API provides intelligent roadmap generation based on user assessment inputs, while also offering curated learning paths and specialization options that reflect current industry standards and requirements.

Whether you're just starting your financial analysis journey or looking to specialize in a particular domain, this API delivers actionable guidance, structured learning recommendations, and clear progression milestones to achieve your career goals.

## Usage

**Example Request:**

```json
{
  "assessmentData": {
    "experience": {
      "yearsInFinance": 2,
      "currentRole": "Accounting Assistant",
      "industryBackground": "Healthcare"
    },
    "skills": {
      "excel": "intermediate",
      "sqlKnowledge": false,
      "financialModeling": "beginner",
      "businessAcumen": "intermediate"
    },
    "goals": {
      "targetRole": "Senior Financial Analyst",
      "targetTimeframe": "24 months",
      "preferredSpecialization": "Corporate Finance"
    },
    "sessionId": "sess_abc123def456",
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "sessionId": "sess_abc123def456",
  "userId": 42,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

**Example Response:**

```json
{
  "roadmapId": "roadmap_xyz789",
  "userId": 42,
  "specialization": "Corporate Finance",
  "estimatedDuration": "18-24 months",
  "phases": [
    {
      "phase": 1,
      "title": "Foundation Building",
      "duration": "3-4 months",
      "keyTopics": [
        "Advanced Excel & VBA",
        "Financial Statement Analysis",
        "Time Value of Money"
      ],
      "certifications": ["Microsoft Excel Expert"],
      "estimatedHours": 120
    },
    {
      "phase": 2,
      "title": "Core Competencies",
      "duration": "4-5 months",
      "keyTopics": [
        "Financial Modeling",
        "Valuation Methods",
        "Budgeting & Forecasting"
      ],
      "certifications": ["CFA Level 1"],
      "estimatedHours": 200
    },
    {
      "phase": 3,
      "title": "Specialization Track",
      "duration": "5-6 months",
      "keyTopics": [
        "M&A Analysis",
        "Corporate Valuation",
        "Capital Structure"
      ],
      "certifications": [],
      "estimatedHours": 180
    }
  ],
  "recommendedLearningResources": [
    {
      "type": "online_course",
      "platform": "Coursera",
      "title": "Financial Modeling and Valuation"
    },
    {
      "type": "certification",
      "provider": "CFA Institute",
      "title": "Chartered Financial Analyst Level 1"
    }
  ],
  "nextMilestones": [
    "Master Advanced Excel within 60 days",
    "Complete Financial Statement Analysis course within 120 days"
  ],
  "createdAt": "2025-01-15T10:30:00Z"
}
```

## Endpoints

### Health Check

**GET** `/`

Verifies the API service is operational and responding.

**Parameters:** None

**Response Shape:**
```
200 OK: Health status object
```

---

### Generate Roadmap

**POST** `/api/finance/roadmap`

Generates a personalized Financial Analyst career roadmap based on user assessment data including experience level, current skills, and career goals.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| assessmentData | AssessmentData object | Yes | User assessment containing experience, skills, and goals with sessionId and timestamp |
| sessionId | string | Yes | Unique session identifier for tracking the request |
| userId | integer or null | No | Optional user identifier for persistent profile tracking |
| timestamp | string | Yes | ISO 8601 formatted timestamp of the request |

**AssessmentData Schema:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| experience | object | No | User's professional experience details (default: {}) |
| skills | object | No | Current skill inventory and proficiency levels (default: {}) |
| goals | object | No | Career goals and aspirations (default: {}) |
| sessionId | string | Yes | Session identifier for correlation |
| timestamp | string | Yes | ISO 8601 formatted timestamp |

**Response Shape:**
```
200 OK: Roadmap object with phases, milestones, and learning resources
422 Unprocessable Entity: Validation error details
```

---

### Get Specializations

**GET** `/api/finance/specializations`

Retrieves all available specialization paths within financial analysis (e.g., Corporate Finance, Investment Analysis, Risk Management, Financial Planning).

**Parameters:** None

**Response Shape:**
```
200 OK: Array of specialization objects with descriptions and requirements
```

---

### Get Learning Paths

**GET** `/api/finance/learning-paths`

Retrieves all curated learning paths available in the platform, including prerequisites, duration, and outcome metrics.

**Parameters:** None

**Response Shape:**
```
200 OK: Array of learning path objects with structured curriculum details
```

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

- Kong Route: https://api.mkkpro.com/career/financial-analyst
- API Docs: https://api.mkkpro.com:8187/docs
