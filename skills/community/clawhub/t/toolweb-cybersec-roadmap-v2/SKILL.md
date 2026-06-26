---
name: Cyber Security Roadmap
description: Generates personalized cybersecurity learning paths based on experience level, goals, and learning preferences.
---

# Overview

The Cyber Security Roadmap API is a comprehensive learning path generator designed to help security professionals and aspiring cybersecurity practitioners build structured, personalized career development plans. By assessing your current experience level, technical knowledge, security background, career goals, and learning preferences, the API generates tailored roadmaps that guide you through the skills and certifications needed to advance in cybersecurity.

This tool is ideal for career changers entering security, professionals seeking specialization in specific domains (threat analysis, compliance, incident response, etc.), and organizations building security training programs for their teams. The API combines industry-standard frameworks with adaptive learning pathways to create realistic, achievable progression plans.

Whether you're starting from zero experience or looking to deepen expertise in a specific cybersecurity domain, the Cyber Security Roadmap API provides the structured guidance needed to achieve your professional goals efficiently.

## Usage

### Sample Request

```json
{
  "assessmentData": {
    "experience_level": "intermediate",
    "knowledge": [
      "networking",
      "linux",
      "python"
    ],
    "security_experience": [
      "network monitoring",
      "vulnerability scanning"
    ],
    "goals": [
      "penetration testing",
      "incident response"
    ],
    "time_commitment": "10-15 hours/week",
    "learning_preferences": [
      "hands-on labs",
      "video courses",
      "certifications"
    ],
    "sessionId": "sess-12345-abcde",
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "sessionId": "sess-12345-abcde",
  "userId": 42,
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### Sample Response

```json
{
  "roadmap_id": "rm-789xyz",
  "user_id": 42,
  "experience_level": "intermediate",
  "specialization": "penetration testing",
  "milestones": [
    {
      "phase": 1,
      "title": "Foundation Strengthening",
      "duration_weeks": 4,
      "topics": [
        "advanced networking concepts",
        "web application architecture",
        "security testing fundamentals"
      ],
      "certifications": [
        "CompTIA Security+"
      ],
      "estimated_hours": 40
    },
    {
      "phase": 2,
      "title": "Penetration Testing Essentials",
      "duration_weeks": 8,
      "topics": [
        "reconnaissance techniques",
        "scanning and enumeration",
        "exploitation methods",
        "post-exploitation"
      ],
      "certifications": [
        "CEH (Certified Ethical Hacker)"
      ],
      "estimated_hours": 80,
      "labs": [
        "HackTheBox",
        "TryHackMe"
      ]
    },
    {
      "phase": 3,
      "title": "Advanced Specialization",
      "duration_weeks": 12,
      "topics": [
        "advanced exploitation",
        "web application pentesting",
        "reporting and remediation"
      ],
      "certifications": [
        "OSCP (Offensive Security Certified Professional)"
      ],
      "estimated_hours": 200,
      "labs": [
        "OSCP Lab Environment"
      ]
    }
  ],
  "recommended_resources": [
    {
      "title": "Penetration Testing with Kali Linux",
      "type": "course",
      "platform": "Udemy",
      "estimated_duration": "40 hours"
    },
    {
      "title": "Web Security Academy",
      "type": "labs",
      "platform": "PortSwigger",
      "estimated_duration": "60 hours"
    }
  ],
  "total_estimated_duration_weeks": 24,
  "created_at": "2025-01-15T10:30:00Z"
}
```

## Endpoints

### GET /
**Health Check**

Verifies that the API is operational and accessible.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| — | — | — | No parameters required |

**Response:** Returns HTTP 200 with service status.

---

### POST /api/cybersecurity/roadmap
**Generate Personalized Roadmap**

Generates a comprehensive, personalized cybersecurity learning roadmap based on the provided assessment data.

**Request Body:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `assessmentData` | `AssessmentData` object | Yes | Learner assessment details including experience level, knowledge, goals, and preferences |
| `sessionId` | string | Yes | Unique session identifier for tracking this request |
| `userId` | integer or null | No | Optional user identifier for authenticated requests |
| `timestamp` | string | Yes | ISO 8601 timestamp of the request |

**AssessmentData object:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experience_level` | string | Yes | Current skill level: "beginner", "intermediate", "advanced", or "expert" |
| `knowledge` | array of strings | No | List of technical areas already understood (e.g., "networking", "linux", "python") |
| `security_experience` | array of strings | No | List of security-related experience (e.g., "network monitoring", "incident response") |
| `goals` | array of strings | No | Career goals and specializations sought (e.g., "penetration testing", "compliance", "threat analysis") |
| `time_commitment` | string | Yes | Available weekly learning time (e.g., "5-10 hours/week", "15+ hours/week") |
| `learning_preferences` | array of strings | No | Preferred learning modalities (e.g., "hands-on labs", "video courses", "certifications", "books") |
| `sessionId` | string | Yes | Session identifier matching request-level sessionId |
| `timestamp` | string | Yes | ISO 8601 timestamp |

**Response (HTTP 200):**

Returns a personalized roadmap object containing:
- Phased milestones with duration and topic recommendations
- Relevant certifications for each phase
- Recommended learning resources (courses, labs, books)
- Estimated total completion time
- Specialization path based on goals

**Error Response (HTTP 422):**

Returns validation errors if required fields are missing or malformed.

---

### GET /api/cybersecurity/specializations
**Retrieve Available Specializations**

Lists all available cybersecurity specialization paths offered by the roadmap engine.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| — | — | — | No parameters required |

**Response (HTTP 200):**

Returns an array of specialization objects, each containing:
- Specialization name and description
- Required foundational knowledge
- Typical duration
- Associated certifications
- Career roles aligned with this path

Example specializations: Penetration Testing, Security Architecture, Incident Response, Cloud Security, Compliance & Governance, Threat Intelligence, Application Security.

---

### GET /api/cybersecurity/learning-paths
**Retrieve All Learning Paths**

Fetches the complete catalog of available learning paths, including difficulty levels and prerequisites.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| — | — | — | No parameters required |

**Response (HTTP 200):**

Returns an array of learning path objects, each containing:
- Path identifier and title
- Description and learning outcomes
- Difficulty level (beginner, intermediate, advanced)
- Prerequisites
- Recommended duration
- Associated learning modules and resources
- Certification mappings

---

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

---

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

---

## References

- **Kong Route:** https://api.mkkpro.com/career/cybersec-roadmap-v2
- **API Docs:** https://api.mkkpro.com:8109/docs
