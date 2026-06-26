---
name: Dry Lab Career Roadmap Generator
description: Generates personalized bioinformatics and computational biology career roadmaps based on individual skills, education, and professional goals.
---

# Overview

The Dry Lab Career Roadmap Generator is a professional platform designed to guide individuals through evidence-based career pathways in bioinformatics and computational biology. This tool leverages assessment data including education background, programming proficiency, biology knowledge, tool expertise, and career aspirations to create customized development plans.

Built for researchers, students, and professionals transitioning into computational life sciences, the platform provides actionable guidance on skill development, industry insights, and job market information. It bridges the gap between academic preparation and industry requirements, helping users identify gaps and prioritize learning objectives aligned with their specific career objectives.

The generator integrates real-world job market data and company hiring practices to ensure recommendations reflect current industry demand and hiring trends for dry lab positions.

## Usage

### Sample Request

```json
{
  "assessmentData": {
    "education": "Master's in Bioinformatics",
    "programming": ["Python", "R", "Bash"],
    "biology": ["Molecular Biology", "Genomics", "Systems Biology"],
    "tools": ["BLAST", "SAMtools", "Bedtools", "GATK"],
    "goals": ["Genome Assembly", "Variant Calling", "Biostatistics"],
    "experience": "2 years in research",
    "sessionId": "sess_a1b2c3d4e5f6",
    "timestamp": "2025-01-15T14:30:00Z"
  },
  "sessionId": "sess_a1b2c3d4e5f6",
  "userId": 12345,
  "timestamp": "2025-01-15T14:30:00Z"
}
```

### Sample Response

```json
{
  "roadmap": {
    "currentLevel": "Intermediate",
    "recommendedPath": "Senior Bioinformatician",
    "skillGaps": [
      "Machine Learning for Genomics",
      "Cloud Computing (AWS/GCP)",
      "Advanced Statistics",
      "Pipeline Development"
    ],
    "recommendedCourses": [
      {
        "title": "Deep Learning in Genomics",
        "provider": "Coursera",
        "duration": "8 weeks",
        "priority": "High"
      },
      {
        "title": "AWS for Bioinformatics",
        "provider": "Udemy",
        "duration": "12 weeks",
        "priority": "High"
      }
    ],
    "targetCompanies": [
      "Illumina",
      "10x Genomics",
      "Genentech",
      "Flatiron Health"
    ],
    "timelineMonths": 12,
    "estimatedSalaryRange": {
      "min": 95000,
      "max": 145000
    }
  }
}
```

## Endpoints

### GET /

**Summary:** Root  
**Description:** Health check endpoint  
**Method:** GET  
**Path:** `/`  

**Response:**
- **200 OK:** Success response with empty schema

---

### GET /health

**Summary:** Health Check  
**Description:** Health check for monitoring  
**Method:** GET  
**Path:** `/health`  

**Response:**
- **200 OK:** Success response with empty schema

---

### POST /api/drylab/roadmap

**Summary:** Generate Roadmap  
**Description:** Generate personalized dry lab career roadmap based on assessment data  
**Method:** POST  
**Path:** `/api/drylab/roadmap`  

**Request Body (Required):**
- **Type:** application/json
- **Schema:** RoadmapRequest object

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| assessmentData | AssessmentData object | Yes | User's skill assessment including education, programming languages, biology expertise, tools knowledge, career goals, and experience level |
| sessionId | string | Yes | Unique session identifier for tracking |
| userId | integer or null | No | Optional user identifier for personalization |
| timestamp | string | Yes | ISO 8601 timestamp of request |

**AssessmentData Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| education | string | Yes | Highest level of education or field of study (e.g., "Master's in Bioinformatics") |
| programming | array of strings | Yes | List of programming languages (e.g., ["Python", "R", "Bash"]) |
| biology | array of strings | Yes | List of biology domains (e.g., ["Genomics", "Molecular Biology"]) |
| tools | array of strings | Yes | List of bioinformatics tools (e.g., ["BLAST", "SAMtools"]) |
| goals | array of strings | Yes | Career objectives and specialization goals |
| experience | string | Yes | Years and type of experience (e.g., "2 years in research") |
| sessionId | string | Yes | Session identifier matching request |
| timestamp | string | Yes | ISO 8601 timestamp |

**Response:**
- **200 OK:** Roadmap data including current level, recommended path, skill gaps, courses, target companies, timeline, and salary estimates
- **422 Unprocessable Entity:** Validation error with detailed error messages

---

### GET /api/drylab/companies

**Summary:** Get Companies  
**Description:** Retrieve list of target companies actively hiring for dry lab roles  
**Method:** GET  
**Path:** `/api/drylab/companies`  

**Response:**
- **200 OK:** Array of company objects with hiring information for dry lab positions

---

### GET /api/drylab/job-market

**Summary:** Get Job Market Info  
**Description:** Retrieve current job market information, trends, and salary data for dry lab roles  
**Method:** GET  
**Path:** `/api/drylab/job-market`  

**Response:**
- **200 OK:** Job market data including salary ranges, demand trends, location insights, and skill requirements

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

- **Kong Route:** https://api.mkkpro.com/career/dry-lab
- **API Docs:** https://api.mkkpro.com:8151/docs
