---
name: Supply Chain Management Roadmap
description: Professional platform that generates personalized Supply Chain Management career roadmaps based on user assessment data and experience level.
---

# Overview

The Supply Chain Management Roadmap API is a professional career development platform designed to help individuals and organizations build structured learning paths in supply chain management. By analyzing user experience, current skills, and career goals, the API generates personalized roadmaps that guide professionals through specialization options and curated learning resources.

This platform serves supply chain professionals at all levels—from entry-level coordinators seeking foundational knowledge to experienced managers pursuing advanced specializations. Organizations can integrate this API to support employee development programs, while individual professionals benefit from data-driven career guidance tailored to their unique background and objectives.

The API provides both personalized roadmap generation and access to comprehensive specialization and learning path catalogs, making it an essential tool for anyone serious about advancing their supply chain management career.

## Usage

### Generate a Personalized Roadmap

**Request:**
```json
{
  "assessmentData": {
    "experience": {
      "yearsInSCM": 3,
      "currentRole": "Supply Chain Coordinator",
      "industryBackground": "Manufacturing"
    },
    "skills": {
      "inventory_management": "intermediate",
      "demand_planning": "beginner",
      "supplier_management": "intermediate",
      "data_analytics": "beginner"
    },
    "goals": {
      "targetRole": "Supply Chain Manager",
      "timeframe": "12 months",
      "focusAreas": ["demand_planning", "cost_reduction"]
    },
    "sessionId": "sess_12345abcde",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionId": "sess_12345abcde",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Response:**
```json
{
  "roadmapId": "rm_987654xyz",
  "userId": 42,
  "sessionId": "sess_12345abcde",
  "personalizedRoadmap": {
    "recommendedSpecializations": [
      {
        "name": "Demand Planning & Forecasting",
        "priority": "high",
        "estimatedDuration": "3 months",
        "relevanceScore": 0.92
      },
      {
        "name": "Cost Optimization & Analytics",
        "priority": "high",
        "estimatedDuration": "2 months",
        "relevanceScore": 0.88
      }
    ],
    "learningSequence": [
      {
        "phase": 1,
        "title": "Demand Planning Fundamentals",
        "duration": "4 weeks",
        "resources": ["course_demand_101", "course_forecasting_basics"],
        "milestones": ["Complete forecasting methods module", "Hands-on planning exercise"]
      },
      {
        "phase": 2,
        "title": "Advanced Analytics for SCM",
        "duration": "6 weeks",
        "resources": ["course_data_analytics_scm", "tool_excel_advanced"],
        "milestones": ["Data visualization project", "Cost reduction analysis"]
      }
    ],
    "estimatedCompletionTime": "12 weeks",
    "careerOutcomes": [
      "Qualify for Senior Coordinator positions",
      "Prepare for Supply Chain Manager interviews",
      "Lead demand planning initiatives"
    ]
  },
  "generatedAt": "2024-01-15T10:30:45Z"
}
```

## Endpoints

### GET /

**Method:** GET  
**Path:** `/`  
**Description:** Health check endpoint to verify API availability and connectivity.

**Parameters:** None

**Response:**
```json
{
  "status": "operational",
  "version": "1.0.0"
}
```

---

### POST /api/scm/roadmap

**Method:** POST  
**Path:** `/api/scm/roadmap`  
**Description:** Generate a personalized Supply Chain Management career roadmap based on user assessment data, experience level, skills inventory, and career goals.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| assessmentData | object | Yes | Core assessment data containing experience, skills, goals, session ID, and timestamp |
| assessmentData.experience | object | No | User's professional experience details (years in SCM, current role, industry background) |
| assessmentData.skills | object | No | Current skill proficiencies mapped by skill type |
| assessmentData.goals | object | No | Career objectives, target roles, and focus areas |
| assessmentData.sessionId | string | Yes | Unique session identifier for tracking this assessment |
| assessmentData.timestamp | string | Yes | ISO 8601 timestamp when assessment was created |
| sessionId | string | Yes | Session identifier linking the request to user context |
| userId | integer or null | No | Optional user ID for personalized tracking and history |
| timestamp | string | Yes | ISO 8601 timestamp when the request was made |

**Response Schema:**
```json
{
  "roadmapId": "string",
  "userId": "integer or null",
  "sessionId": "string",
  "personalizedRoadmap": {
    "recommendedSpecializations": [
      {
        "name": "string",
        "priority": "string",
        "estimatedDuration": "string",
        "relevanceScore": "number"
      }
    ],
    "learningSequence": [
      {
        "phase": "integer",
        "title": "string",
        "duration": "string",
        "resources": ["string"],
        "milestones": ["string"]
      }
    ],
    "estimatedCompletionTime": "string",
    "careerOutcomes": ["string"]
  },
  "generatedAt": "string"
}
```

**Status Codes:**
- `200 OK` - Roadmap successfully generated
- `422 Unprocessable Entity` - Validation error in request body

---

### GET /api/scm/specializations

**Method:** GET  
**Path:** `/api/scm/specializations`  
**Description:** Retrieve all available supply chain management specialization paths and tracks.

**Parameters:** None

**Response Schema:**
```json
{
  "specializations": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "level": "string",
      "requiredSkills": ["string"],
      "courseCount": "integer",
      "estimatedHours": "integer"
    }
  ],
  "totalCount": "integer"
}
```

**Status Codes:**
- `200 OK` - Specializations list retrieved successfully

---

### GET /api/scm/learning-paths

**Method:** GET  
**Path:** `/api/scm/learning-paths`  
**Description:** Retrieve all available structured learning paths for supply chain management career development.

**Parameters:** None

**Response Schema:**
```json
{
  "learningPaths": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "targetRole": "string",
      "difficulty": "string",
      "duration": "string",
      "courseSequence": [
        {
          "sequence": "integer",
          "courseId": "string",
          "courseName": "string",
          "duration": "string"
        }
      ],
      "prerequisiteSkills": ["string"],
      "successMetrics": ["string"]
    }
  ],
  "totalPaths": "integer"
}
```

**Status Codes:**
- `200 OK` - Learning paths list retrieved successfully

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

- **Kong Route:** https://api.mkkpro.com/career/supply-chain-mgmt
- **API Docs:** https://api.mkkpro.com:8190/docs
