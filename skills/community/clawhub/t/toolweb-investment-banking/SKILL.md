---
name: Investment Banking Specialist Roadmap
description: Professional Investment Banking Career Roadmap Platform that generates personalized career development paths and specialization guidance.
---

# Overview

The Investment Banking Specialist Roadmap is a professional career development platform designed to help financial professionals navigate their path to investment banking specialization. This API provides personalized roadmap generation, specialization path discovery, and structured learning resources tailored to individual experience levels, skill gaps, and career objectives.

Built for finance professionals, career coaches, and educational institutions, this platform combines assessment data with industry-standard competency frameworks to deliver actionable guidance. Whether you're transitioning into investment banking, advancing within the field, or targeting specific specializations like M&A, DCM, or ECM, the platform adapts to your unique profile and delivers step-by-step career progression strategies.

The roadmap engine analyzes your current experience, technical skills, and career goals to recommend learning paths, specialization tracks, and development milestones aligned with real-world investment banking career trajectories.

## Usage

### Request: Generate Personalized Roadmap

```json
{
  "sessionId": "sess_abc123xyz",
  "userId": 42,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "sess_abc123xyz",
    "timestamp": "2024-01-15T10:30:00Z",
    "experience": {
      "yearsInFinance": 3,
      "previousRole": "Financial Analyst",
      "currentEmployer": "Fortune 500 Bank"
    },
    "skills": {
      "technicalSkills": ["Excel", "Python", "SQL", "Financial Modeling"],
      "softSkills": ["Communication", "Analytical Thinking"],
      "certifications": ["CFA Level 1"]
    },
    "goals": {
      "targetRole": "Associate - M&A Advisory",
      "timelineMonths": 18,
      "geographicPreference": "NYC"
    }
  }
}
```

### Response: Personalized Roadmap

```json
{
  "roadmapId": "rm_xyz789",
  "userId": 42,
  "sessionId": "sess_abc123xyz",
  "generatedAt": "2024-01-15T10:30:15Z",
  "assessmentSummary": {
    "currentLevel": "intermediate",
    "experienceGap": 2,
    "skillGapAreas": ["Advanced Financial Modeling", "Valuation Techniques", "Deal Structuring"]
  },
  "recommendedRoadmap": {
    "specialization": "M&A Advisory",
    "phases": [
      {
        "phase": 1,
        "duration": "3 months",
        "focus": "Foundation Building",
        "milestones": [
          "Master DCF Analysis",
          "Complete Comparable Company Analysis",
          "Study Recent M&A Case Studies"
        ],
        "learningResources": ["Financial Modeling Masterclass", "M&A Primer Course"]
      },
      {
        "phase": 2,
        "duration": "6 months",
        "focus": "Specialization Development",
        "milestones": [
          "LBO Model Proficiency",
          "Deal Structuring Fundamentals",
          "Industry Deep Dive"
        ],
        "learningResources": ["Advanced LBO Modeling", "Investment Banking Transactions"]
      },
      {
        "phase": 3,
        "duration": "9 months",
        "focus": "Professional Readiness",
        "milestones": [
          "End-to-End Deal Analysis",
          "Interview Preparation",
          "Networking and Positioning"
        ],
        "learningResources": ["Mock Interview Program", "Networking Strategy Guide"]
      }
    ]
  },
  "specializations": [
    {
      "name": "M&A Advisory",
      "matchScore": 0.92,
      "description": "Mergers and Acquisitions specialization"
    },
    {
      "name": "ECM",
      "matchScore": 0.78,
      "description": "Equity Capital Markets specialization"
    }
  ],
  "nextSteps": [
    "Enroll in Financial Modeling Masterclass",
    "Begin DCF Analysis practice problems",
    "Schedule monthly progress reviews"
  ]
}
```

## Endpoints

### GET `/`
**Health Check Endpoint**

Verifies API availability and connectivity.

**Parameters:** None

**Response:**
- `200 OK` - API is operational
  - Returns health status object

---

### POST `/api/ib/roadmap`
**Generate Personalized Roadmap**

Creates a customized Investment Banking career roadmap based on assessment data, current experience, skills inventory, and career goals.

**Required Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessionId` | string | Yes | Unique session identifier for tracking |
| `timestamp` | string | Yes | ISO 8601 timestamp of request |
| `assessmentData` | object | Yes | Contains experience, skills, and goals objects |
| `assessmentData.sessionId` | string | Yes | Session identifier (must match parent sessionId) |
| `assessmentData.timestamp` | string | Yes | Assessment timestamp |
| `assessmentData.experience` | object | No | Career history and current position details |
| `assessmentData.skills` | object | No | Technical skills, soft skills, and certifications |
| `assessmentData.goals` | object | No | Target role, timeline, and preferences |

**Optional Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `userId` | integer | User identifier for profile association |

**Response (200 OK):**
- `roadmapId` - Unique roadmap identifier
- `userId` - Associated user ID
- `sessionId` - Tracking session ID
- `generatedAt` - Timestamp of generation
- `assessmentSummary` - Analysis of current level and gaps
- `recommendedRoadmap` - Multi-phase career progression plan
- `specializations` - Ranked specialization matches with scores
- `nextSteps` - Immediate action items

**Error Response (422):**
- Returns validation errors if required fields are missing or malformed

---

### GET `/api/ib/specializations`
**Get Available Specializations**

Retrieves all available investment banking specialization paths and their descriptions.

**Parameters:** None

**Response (200 OK):**
- Array of specialization objects including:
  - `name` - Specialization title (e.g., "M&A Advisory", "DCM", "ECM")
  - `description` - Career path overview
  - `requirements` - Prerequisites and competencies
  - `careerProgression` - Typical advancement track
  - `averageSalary` - Compensation ranges

---

### GET `/api/ib/learning-paths`
**Get All Available Learning Paths**

Retrieves comprehensive list of structured learning resources, courses, and development modules available within the platform.

**Parameters:** None

**Response (200 OK):**
- Array of learning path objects including:
  - `pathId` - Unique path identifier
  - `title` - Learning resource name
  - `specialization` - Applicable specialization
  - `difficulty` - Level (beginner, intermediate, advanced)
  - `duration` - Estimated completion time
  - `topics` - Learning objectives and modules
  - `prerequisites` - Required prior knowledge

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

- **Kong Route:** https://api.mkkpro.com/career/investment-banking
- **API Docs:** https://api.mkkpro.com:8186/docs
