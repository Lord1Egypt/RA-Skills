---
name: RPA Developer Roadmap
description: Professional RPA Developer Career Roadmap Platform for UiPath and BluePrism automation technologies.
---

# Overview

The RPA Developer Roadmap is a professional career guidance platform designed to help developers transition into or advance within Robotic Process Automation (RPA) development using industry-leading tools like UiPath and BluePrism. This platform generates personalized learning and development roadmaps based on individual experience levels, current skill assessments, and career goals.

The platform provides intelligent career path recommendations by analyzing your technical background, existing RPA competencies, and professional objectives. It delivers structured, actionable guidance tailored to your current position in the RPA development journey, whether you're a beginner seeking foundational knowledge or an experienced developer aiming for specialized expertise.

Ideal users include software developers transitioning to RPA, automation engineers looking to formalize their skills, IT professionals pursuing career advancement in process automation, and organizations developing internal RPA talent pipelines.

# Usage

## Sample Request

```json
{
  "sessionId": "session-12345-abc",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "session-12345-abc",
    "timestamp": "2024-01-15T10:30:00Z",
    "experience": {
      "yearsInIT": 5,
      "automationBackground": false,
      "previousRPAExposure": "none"
    },
    "skills": {
      "programming": "intermediate",
      "databaseKnowledge": "basic",
      "processAnalysis": "beginner"
    },
    "goals": {
      "targetRole": "RPA Developer",
      "preferredTool": "UiPath",
      "timelineMonths": 6
    }
  }
}
```

## Sample Response

```json
{
  "roadmapId": "roadmap-uuid-789",
  "userId": 42,
  "generatedAt": "2024-01-15T10:30:15Z",
  "recommendedPath": {
    "currentLevel": "intermediate",
    "targetLevel": "professional",
    "estimatedDuration": "6 months"
  },
  "phases": [
    {
      "phase": 1,
      "title": "RPA Fundamentals",
      "duration": "4 weeks",
      "topics": [
        "RPA Concepts and Benefits",
        "UiPath Studio Basics",
        "Process Analysis Fundamentals"
      ]
    },
    {
      "phase": 2,
      "title": "Core Development Skills",
      "duration": "8 weeks",
      "topics": [
        "Workflow Design Patterns",
        "UI Automation Techniques",
        "Data Manipulation and Variables"
      ]
    },
    {
      "phase": 3,
      "title": "Advanced Techniques",
      "duration": "6 weeks",
      "topics": [
        "Exception Handling",
        "Integration with Enterprise Systems",
        "Performance Optimization"
      ]
    }
  ],
  "resources": [
    {
      "type": "course",
      "title": "UiPath Certified Associate Developer",
      "provider": "UiPath Academy",
      "difficulty": "intermediate"
    },
    {
      "type": "documentation",
      "title": "UiPath Studio User Guide",
      "provider": "UiPath Official"
    }
  ],
  "milestones": [
    {
      "month": 2,
      "objective": "Complete first automation project"
    },
    {
      "month": 4,
      "objective": "Pass UiPath Associate Certification"
    },
    {
      "month": 6,
      "objective": "Develop production-ready automation solution"
    }
  ]
}
```

# Endpoints

## GET /

**Summary:** Root

**Description:** Root endpoint

**Parameters:** None

**Response:** 
- **Status:** 200 OK
- **Content-Type:** application/json
- **Schema:** Empty JSON object

---

## GET /health

**Summary:** Health Check

**Description:** Health check endpoint to verify API availability and operational status

**Parameters:** None

**Response:**
- **Status:** 200 OK
- **Content-Type:** application/json
- **Schema:** Empty JSON object

---

## POST /api/rpa/roadmap

**Summary:** Generate Roadmap

**Description:** Generate personalized RPA developer roadmap based on assessment data, experience level, and career goals

**Parameters:**

| Name | Type | Required | Location | Description |
|------|------|----------|----------|-------------|
| assessmentData | object | Yes | body | Assessment data object containing experience, skills, and goals information |
| assessmentData.experience | object | No | body | Object detailing professional background and automation experience |
| assessmentData.skills | object | No | body | Object describing current technical skill levels |
| assessmentData.goals | object | No | body | Object specifying career objectives and target roles |
| assessmentData.sessionId | string | Yes | body | Unique identifier for the assessment session |
| assessmentData.timestamp | string | Yes | body | ISO 8601 formatted timestamp of assessment |
| sessionId | string | Yes | body | Unique identifier for the current session |
| userId | integer or null | No | body | Unique identifier for the user; null if anonymous |
| timestamp | string | Yes | body | ISO 8601 formatted timestamp of the request |

**Request Body Schema:**
```json
{
  "assessmentData": {
    "experience": {},
    "skills": {},
    "goals": {},
    "sessionId": "string",
    "timestamp": "string"
  },
  "sessionId": "string",
  "userId": 0,
  "timestamp": "string"
}
```

**Response:**
- **Status:** 200 OK
- **Content-Type:** application/json
- **Schema:** Personalized roadmap object containing phases, learning resources, and milestones

**Error Responses:**
- **Status:** 422 Unprocessable Entity
- **Content-Type:** application/json
- **Description:** Validation error occurred with request parameters
- **Schema:** HTTPValidationError containing array of ValidationError objects with location, message, and error type

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

- **Kong Route:** https://api.mkkpro.com/career/rpa-developer
- **API Docs:** https://api.mkkpro.com:8068/docs
