---
name: Nutrition & Dietetics Roadmap
description: Professional career roadmap platform for Nutrition & Dietetics with personalized learning paths and specialization guidance.
---

# Overview

The Nutrition & Dietetics Roadmap is a professional career development platform designed to guide aspiring and practicing nutrition and dietetics professionals through their career journey. This API-driven platform generates personalized roadmaps based on individual assessment data, including experience, skills, and career goals.

The platform provides comprehensive guidance through multiple specialization paths and curated learning resources. Whether you're starting your nutrition career, seeking specialization, or planning professional advancement, this roadmap tool adapts to your unique profile and delivers actionable next steps aligned with industry standards and best practices.

Ideal users include nutrition students, registered dietitian nutritionists (RDNs), healthcare professionals transitioning into nutrition roles, and career counselors supporting nutrition professionals in structured professional development planning.

## Usage

### Example: Generate Personalized Nutrition Roadmap

**Sample Request:**

```json
{
  "assessmentData": {
    "experience": {
      "yearsInField": 3,
      "currentRole": "Clinical Dietitian",
      "previousRoles": ["Food Service Supervisor"]
    },
    "skills": {
      "clinical": "Advanced",
      "research": "Intermediate",
      "management": "Beginner",
      "technology": "Intermediate"
    },
    "goals": {
      "primary": "Specialize in renal nutrition",
      "timeline": "18 months",
      "careerShift": "From clinical to specialized practice"
    },
    "sessionId": "sess_a1b2c3d4e5f6",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionId": "sess_a1b2c3d4e5f6",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Sample Response:**

```json
{
  "roadmapId": "rm_7k9m2n5p8q1r",
  "userId": 12345,
  "specialization": "Renal Nutrition",
  "timelineMonths": 18,
  "phases": [
    {
      "phase": 1,
      "title": "Foundation Strengthening",
      "duration": "3 months",
      "objectives": [
        "Complete advanced renal physiology module",
        "Review current literature on kidney disease management",
        "Obtain specialty certification preparation materials"
      ],
      "resources": [
        {
          "type": "Course",
          "title": "Advanced Renal Pathophysiology",
          "provider": "Academy of Nutrition and Dietetics",
          "duration": "40 hours"
        },
        {
          "type": "Certification",
          "title": "Certified Nutrition Support Clinician (CNSC) prep",
          "provider": "ASPEN",
          "duration": "Self-paced"
        }
      ]
    },
    {
      "phase": 2,
      "title": "Specialized Skill Development",
      "duration": "6 months",
      "objectives": [
        "Develop advanced renal nutrition counseling skills",
        "Gain experience in dialysis management",
        "Complete mentorship under renal nutrition specialist"
      ],
      "resources": [
        {
          "type": "Mentorship",
          "title": "1-on-1 Renal RDN Mentorship",
          "duration": "6 months"
        },
        {
          "type": "Clinical Practice",
          "title": "Dialysis Center Clinical Hours",
          "duration": "200 hours"
        }
      ]
    },
    {
      "phase": 3,
      "title": "Certification & Credentialing",
      "duration": "9 months",
      "objectives": [
        "Complete renal nutrition specialty certification exam",
        "Document case studies for credentialing",
        "Establish specialized practice credentials"
      ],
      "resources": [
        {
          "type": "Certification",
          "title": "Board Certified Specialist in Renal Nutrition (CSR)",
          "provider": "CDRB",
          "duration": "Exam-based"
        }
      ]
    }
  ],
  "skillGaps": [
    {
      "skill": "Advanced Renal Disease Management",
      "currentLevel": "Intermediate",
      "targetLevel": "Advanced",
      "priority": "High"
    },
    {
      "skill": "Research & Evidence Synthesis",
      "currentLevel": "Intermediate",
      "targetLevel": "Advanced",
      "priority": "Medium"
    }
  ],
  "nextSteps": [
    "Enroll in Advanced Renal Pathophysiology course",
    "Schedule consultation with renal nutrition mentor",
    "Register for CNSC certification preparation"
  ],
  "estimatedCompletionDate": "2025-07-15",
  "generatedAt": "2024-01-15T10:30:00Z"
}
```

## Endpoints

### GET /

**Health Check Endpoint**

Verifies platform availability and API responsiveness.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | N/A | N/A | No parameters required |

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### POST /api/nutrition/roadmap

**Generate Personalized Roadmap**

Generates a customized Nutrition & Dietetics career roadmap based on assessment data including current experience, skills, and professional goals.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| assessmentData | object | Yes | Assessment data containing experience, skills, goals, sessionId, and timestamp |
| assessmentData.experience | object | No | Current professional experience details |
| assessmentData.skills | object | No | Current skill assessments |
| assessmentData.goals | object | No | Career and development goals |
| assessmentData.sessionId | string | Yes | Unique session identifier for tracking |
| assessmentData.timestamp | string | Yes | ISO 8601 timestamp of assessment |
| sessionId | string | Yes | Session identifier matching assessmentData.sessionId |
| userId | integer or null | No | Optional user identifier for personalization |
| timestamp | string | Yes | ISO 8601 timestamp of request |

**Response Shape:**
```json
{
  "roadmapId": "string",
  "userId": "integer or null",
  "specialization": "string",
  "timelineMonths": "integer",
  "phases": [
    {
      "phase": "integer",
      "title": "string",
      "duration": "string",
      "objectives": ["string"],
      "resources": [
        {
          "type": "string",
          "title": "string",
          "provider": "string",
          "duration": "string"
        }
      ]
    }
  ],
  "skillGaps": [
    {
      "skill": "string",
      "currentLevel": "string",
      "targetLevel": "string",
      "priority": "string"
    }
  ],
  "nextSteps": ["string"],
  "estimatedCompletionDate": "string",
  "generatedAt": "string"
}
```

---

### GET /api/nutrition/specializations

**Get Available Specializations**

Retrieves all available nutrition and dietetics specialization paths supported by the roadmap platform.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | N/A | N/A | No parameters required |

**Response Shape:**
```json
{
  "specializations": [
    {
      "id": "string",
      "name": "string",
      "description": "string",
      "requiredExperience": "string",
      "typicalDuration": "integer",
      "certifications": ["string"],
      "careerOutcomes": ["string"]
    }
  ]
}
```

---

### GET /api/nutrition/learning-paths

**Get All Learning Paths**

Retrieves comprehensive learning paths available for nutrition and dietetics professional development across all specializations and skill levels.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (none) | N/A | N/A | No parameters required |

**Response Shape:**
```json
{
  "learningPaths": [
    {
      "pathId": "string",
      "title": "string",
      "specialization": "string",
      "skillLevel": "string",
      "duration": "integer",
      "modules": [
        {
          "moduleId": "string",
          "title": "string",
          "description": "string",
          "duration": "integer",
          "resources": ["string"]
        }
      ],
      "prerequisites": ["string"],
      "outcomes": ["string"]
    }
  ]
}
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

- **Kong Route:** https://api.mkkpro.com/career/nutrition-dietetics
- **API Docs:** https://api.mkkpro.com:8181/docs
