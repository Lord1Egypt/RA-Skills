---
name: Interviewly API
description: AI-powered voice mock interview platform that analyzes job descriptions and conducts adaptive interviews with real-time feedback.
---

# Overview

Interviewly is an AI-powered mock interview platform designed to help job candidates prepare for technical and behavioral interviews. The platform uses advanced natural language processing to analyze job descriptions, generate role-specific interview questions, and provide comprehensive feedback on candidate responses.

The API enables a four-step interview workflow: job description analysis, interview initialization, response submission with real-time evaluation, and final report generation. Each interview is personalized based on the analyzed job requirements, creating a realistic and tailored preparation experience.

Ideal users include job seekers preparing for interviews, recruitment platforms offering candidate assessment features, corporate training teams, and educational institutions building interview preparation modules.

## Usage

### Example: Complete Interview Workflow

**Step 1: Analyze Job Description**

```json
POST /api/v1/analyze-jd
Content-Type: application/json

{
  "job_description": "Senior Full Stack Engineer - 5+ years experience with React, Node.js, and AWS. Must have experience with microservices architecture and CI/CD pipelines."
}
```

Response:
```json
{
  "success": true,
  "session_id": "sess_a1b2c3d4e5f6",
  "analysis": {
    "required_skills": ["React", "Node.js", "AWS", "Microservices", "CI/CD"],
    "experience_level": "Senior",
    "role_type": "Full Stack Engineer"
  },
  "estimated_questions": 6,
  "message": "Job description analyzed successfully"
}
```

**Step 2: Start Interview**

```json
POST /api/v1/start-interview
Content-Type: application/json

{
  "session_id": "sess_a1b2c3d4e5f6",
  "user_id": 12345
}
```

Response:
```json
{
  "success": true,
  "first_question": "Tell me about your experience with microservices architecture. Can you describe a specific project where you designed or worked with microservices?",
  "question_number": 1,
  "total_questions": 6,
  "time_limit_minutes": 3
}
```

**Step 3: Submit Response**

```json
POST /api/v1/submit-response
Content-Type: application/json

{
  "session_id": "sess_a1b2c3d4e5f6",
  "question_number": 1,
  "user_response": "I led the migration of our monolithic application to microservices using Node.js. We split into 8 independent services with their own databases, managed through Kubernetes on AWS ECS.",
  "response_time_seconds": 45,
  "transcription_confidence": 0.98
}
```

Response:
```json
{
  "success": true,
  "next_question": "What challenges did you face during this migration and how did you overcome them?",
  "question_number": 2,
  "feedback": "Strong answer demonstrating practical microservices experience. Consider adding more details about deployment strategies.",
  "interview_complete": false
}
```

**Step 4: End Interview & Download Report**

```json
POST /api/v1/end-interview
Content-Type: application/json

{
  "session_id": "sess_a1b2c3d4e5f6"
}
```

Response:
```json
{
  "success": true,
  "overall_score": 78,
  "report_url": "https://api.toolweb.in/api/v1/download/sess_a1b2c3d4e5f6",
  "message": "Interview completed. Report generated successfully."
}
```

## Endpoints

### GET /
**Purpose:** API health check  
**Parameters:** None  
**Response:** 200 OK with service status

---

### GET /status
**Purpose:** Detailed health check with service diagnostics  
**Parameters:** None  
**Response:** 200 OK with detailed health information

---

### POST /api/v1/analyze-jd
**Purpose:** Analyze job description and initialize interview session

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| job_description | string | Yes | Full job description text to analyze |

**Response Shape:**
```json
{
  "success": boolean,
  "session_id": string,
  "analysis": {
    "required_skills": string[],
    "experience_level": string,
    "role_type": string
  },
  "estimated_questions": integer,
  "message": string
}
```

---

### POST /api/v1/start-interview
**Purpose:** Initialize interview session and generate first question

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| session_id | string | Yes | Session ID from analyze-jd response |
| user_id | integer | Yes | Unique identifier for the candidate |

**Response Shape:**
```json
{
  "success": boolean,
  "first_question": string,
  "question_number": integer,
  "total_questions": integer,
  "time_limit_minutes": integer
}
```

---

### POST /api/v1/submit-response
**Purpose:** Submit candidate response, evaluate with Claude AI, and generate next question

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| session_id | string | Yes | Active session ID |
| question_number | integer | Yes | Current question number |
| user_response | string | Yes | Candidate's answer text |
| response_time_seconds | integer | No | Time taken to respond in seconds |
| transcription_confidence | number | No | Confidence score (0-1) if voice-transcribed |

**Response Shape:**
```json
{
  "success": boolean,
  "next_question": string | null,
  "question_number": integer | null,
  "feedback": string | null,
  "interview_complete": boolean
}
```

---

### POST /api/v1/end-interview
**Purpose:** Terminate interview, generate comprehensive evaluation report, and create PDF with download URL

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| session_id | string | Yes | Session ID to end |

**Response Shape:**
```json
{
  "success": boolean,
  "overall_score": integer,
  "report_url": string,
  "message": string
}
```

---

### GET /api/v1/download/{session_id}
**Purpose:** Download the interview report PDF

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| session_id | string (path) | Yes | Session ID of completed interview |

**Response:** PDF file download

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

- Kong Route: https://api.toolweb.in/tools/interviewly
- API Docs: https://api.toolweb.in:8173/docs
