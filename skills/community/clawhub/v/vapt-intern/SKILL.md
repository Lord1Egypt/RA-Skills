---
name: VAPT Intern Roadmap
description: Professional Vulnerability Assessment & Penetration Testing Career Roadmap Platform that generates personalized learning paths for aspiring VAPT professionals.
---

# Overview

The VAPT Intern Roadmap is a professional career development platform designed to guide aspiring cybersecurity professionals through a structured Vulnerability Assessment and Penetration Testing (VAPT) learning journey. This platform leverages assessment data including current experience levels, technical skills, and career goals to generate personalized roadmaps tailored to individual development needs.

Built for security practitioners, hiring managers, and training organizations, the VAPT Intern Roadmap provides evidence-based progression paths aligned with industry standards and real-world VAPT competencies. The platform integrates session management and timestamp tracking to ensure personalized, repeatable assessments and progress monitoring over time.

Ideal users include aspiring penetration testers seeking structured learning paths, security training providers developing curriculum, and organizations evaluating VAPT skill readiness within their teams.

## Usage

### Sample Request

```json
{
  "assessmentData": {
    "experience": {
      "yearsInIT": 2,
      "penetrationTestingExperience": "6 months",
      "networkingBackground": true
    },
    "skills": {
      "networking": "intermediate",
      "linuxAdministration": "intermediate",
      "webApplicationSecurity": "beginner",
      "scriptingLanguages": ["Python", "Bash"]
    },
    "goals": {
      "certificationTarget": "OSCP",
      "careerGoal": "Junior Penetration Tester",
      "timelineMonths": 12
    },
    "sessionId": "sess_8f7a3c2e9d1b",
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "sessionId": "sess_8f7a3c2e9d1b",
  "userId": 12345,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Sample Response

```json
{
  "roadmapId": "roadmap_5e2d8f9c",
  "userId": 12345,
  "sessionId": "sess_8f7a3c2e9d1b",
  "generatedAt": "2025-01-15T10:30:15Z",
  "phases": [
    {
      "phase": 1,
      "title": "Foundation & Prerequisites",
      "duration": "8 weeks",
      "focus": [
        "Advanced Networking (TCP/IP, DNS, HTTP/HTTPS)",
        "Linux System Administration",
        "Python for Security Automation"
      ],
      "resources": ["TryHackMe", "HackTheBox", "Udemy courses"],
      "estimatedHours": 120
    },
    {
      "phase": 2,
      "title": "Core VAPT Techniques",
      "duration": "12 weeks",
      "focus": [
        "Reconnaissance & Information Gathering",
        "Vulnerability Scanning & Assessment",
        "Web Application Testing (OWASP Top 10)",
        "Exploitation Fundamentals"
      ],
      "resources": ["PortSwigger Web Academy", "OWASP Documentation"],
      "estimatedHours": 180
    },
    {
      "phase": 3,
      "title": "Certification Preparation",
      "duration": "12 weeks",
      "focus": [
        "OSCP Lab Environment Practice",
        "Report Writing & Communication",
        "Hands-on Penetration Testing"
      ],
      "resources": ["Offensive Security Course", "PWK Labs"],
      "estimatedHours": 200
    }
  ],
  "certificationPath": "OSCP",
  "estimatedCompletionDate": "2025-12-15",
  "keyMilestones": [
    "Complete 50 HackTheBox machines",
    "Pass Security+ or equivalent",
    "Complete 20 practice penetration tests",
    "Achieve OSCP certification"
  ]
}
```

## Endpoints

### GET /

**Description:** Root endpoint

**Method:** GET

**Path:** `/`

**Parameters:** None

**Response:** Returns welcome information and API status (schema: empty object)

**Status Codes:**
- `200`: Successful Response

---

### GET /health

**Description:** Health check endpoint for service status verification

**Method:** GET

**Path:** `/health`

**Parameters:** None

**Response:** Returns service health status (schema: empty object)

**Status Codes:**
- `200`: Successful Response

---

### POST /api/vapt/roadmap

**Description:** Generate a personalized VAPT intern roadmap based on assessment data, experience level, skills, and career goals.

**Method:** POST

**Path:** `/api/vapt/roadmap`

**Request Body (Required):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `assessmentData` | AssessmentData | ✓ | Comprehensive assessment object containing experience, skills, and goals |
| `assessmentData.experience` | object | optional | Experience background details (yearsInIT, penetrationTestingExperience, etc.) |
| `assessmentData.skills` | object | optional | Current technical skills assessment (networking, linux, web security levels, programming languages) |
| `assessmentData.goals` | object | optional | Career objectives (certificationTarget, careerGoal, timelineMonths) |
| `assessmentData.sessionId` | string | ✓ | Unique session identifier for tracking assessment |
| `assessmentData.timestamp` | string | ✓ | ISO 8601 timestamp of assessment creation |
| `sessionId` | string | ✓ | Session identifier for the request |
| `userId` | integer \| null | optional | Optional user identifier for authenticated requests |
| `timestamp` | string | ✓ | ISO 8601 timestamp of request submission |

**Response Schema:**

Returns a personalized roadmap object containing:
- `roadmapId`: Unique roadmap identifier
- `userId`: Associated user ID
- `sessionId`: Request session ID
- `generatedAt`: Timestamp of roadmap generation
- `phases`: Array of learning phases with duration, focus areas, resources, and estimated hours
- `certificationPath`: Recommended certification target
- `estimatedCompletionDate`: Projected completion date
- `keyMilestones`: Array of major achievement milestones

**Status Codes:**
- `200`: Successful Response - Roadmap generated successfully
- `422`: Validation Error - Request parameters did not pass validation

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

- **Kong Route:** https://api.mkkpro.com/career/vapt-intern
- **API Docs:** https://api.mkkpro.com:8058/docs
