---
name: CISSPly API
description: A CISSP exam preparation quiz API that delivers randomized questions, tracks session progress, and evaluates answers in real-time.
---

# Overview

CISSPly API is a specialized quiz platform designed to help security professionals prepare for the Certified Information Systems Security Professional (CISSP) certification exam. The API manages quiz sessions, delivers curated questions from a secure question bank, and provides instant evaluation of answers with detailed performance metrics.

Built by security experts with CISSP and CISM credentials, CISSPly combines robust session management with intelligent question distribution to create an effective study tool. The platform supports custom quiz lengths, tracks time-on-task metrics, and delivers comprehensive scoring analysis to help users identify knowledge gaps across CISSP domains.

Ideal users include cybersecurity professionals pursuing CISSP certification, training organizations delivering exam prep programs, and individuals seeking structured, API-driven learning platforms with granular performance tracking.

## Usage

### Example: Start a Quiz Session

**Request:**

```json
{
  "sessionId": "user-12345-session-001",
  "numQuestions": 50
}
```

**cURL:**

```bash
curl -X POST https://api.toolweb.in/tools/cissply/api/quiz/start \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "user-12345-session-001",
    "numQuestions": 50
  }'
```

**Response:**

```json
{
  "sessionId": "user-12345-session-001",
  "totalQuestions": 50,
  "questions": [
    {
      "questionId": 1,
      "text": "Which of the following is a primary function of the CISSP certification?",
      "options": [
        "Validates cybersecurity knowledge",
        "Provides coding expertise",
        "Certifies network administration",
        "Ensures software development skills"
      ],
      "category": "Security and Risk Management"
    },
    {
      "questionId": 2,
      "text": "What does CIA stand for in information security?",
      "options": [
        "Confidentiality, Integrity, Availability",
        "Central Intelligence Agency",
        "Compliance, Integration, Audit",
        "Cryptography, Identity, Authorization"
      ],
      "category": "Security and Risk Management"
    }
  ],
  "status": "started",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Example: Submit Quiz Answers

**Request:**

```json
{
  "sessionId": "user-12345-session-001",
  "answers": [0, 2, 1, 3, null],
  "timeTaken": 1800
}
```

**cURL:**

```bash
curl -X POST https://api.toolweb.in/tools/cissply/api/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "user-12345-session-001",
    "answers": [0, 2, 1, 3, null],
    "timeTaken": 1800
  }'
```

**Response:**

```json
{
  "sessionId": "user-12345-session-001",
  "totalQuestions": 5,
  "correctAnswers": 3,
  "score": 60,
  "timeTaken": 1800,
  "results": [
    {
      "questionId": 1,
      "userAnswer": 0,
      "correctAnswer": 0,
      "isCorrect": true,
      "category": "Security and Risk Management"
    },
    {
      "questionId": 2,
      "userAnswer": 2,
      "correctAnswer": 0,
      "isCorrect": false,
      "category": "Security and Risk Management"
    }
  ],
  "categoryPerformance": {
    "Security and Risk Management": 60,
    "Access Control": 100,
    "Cryptography": 50
  },
  "timestamp": "2024-01-15T10:40:00Z"
}
```

## Endpoints

### GET /
**Summary:** Root

Returns basic service information.

**Parameters:** None

**Response:** Service metadata and available endpoints.

---

### GET /health
**Summary:** Health Check

Health check endpoint to verify service availability and status.

**Parameters:** None

**Response:** Health status indicator.

---

### POST /api/quiz/start
**Summary:** Start Quiz

Initiates a new quiz session with randomized questions.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| sessionId | string | Yes | Unique identifier for the quiz session |
| numQuestions | integer | Yes | Number of questions to include in the quiz (1-100) |

**Request Body Schema:**

```json
{
  "sessionId": "string",
  "numQuestions": 0
}
```

**Response:** Quiz session object with randomized questions, metadata, and session status.

**Status Codes:**
- `200`: Quiz session started successfully
- `422`: Validation error (invalid parameters)

---

### POST /api/quiz/submit
**Summary:** Submit Quiz

Submits completed quiz answers and receives immediate evaluation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| sessionId | string | Yes | Session identifier from the started quiz |
| answers | array[integer \| null] | Yes | Array of answer indices; use null for unanswered questions |
| timeTaken | integer | Yes | Time spent on quiz in seconds |

**Request Body Schema:**

```json
{
  "sessionId": "string",
  "answers": [0, 1, null, 2],
  "timeTaken": 1800
}
```

**Response:** Detailed results including score, correct/incorrect answers, category breakdown, and performance metrics.

**Status Codes:**
- `200`: Quiz evaluated successfully
- `422`: Validation error (mismatched answer count or invalid session)

---

### POST /api/quiz/evaluate
**Summary:** Evaluate Quiz

Evaluates quiz answers and returns detailed results and analysis.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| data | object | Yes | Quiz evaluation data (flexible schema) |

**Request Body Schema:**

```json
{
  "sessionId": "string",
  "answers": [0, 1, 2],
  "timeTaken": 1800
}
```

**Response:** Comprehensive evaluation results with scoring breakdown by domain and recommendation data.

**Status Codes:**
- `200`: Evaluation completed successfully
- `422`: Validation error

---

### POST /api/admin/reload
**Summary:** Reload Questions

Reloads question database from Excel source files (admin-only endpoint).

**Parameters:** None

**Authentication:** Admin credentials required

**Response:** Confirmation of question reload with updated question count and categories.

**Status Codes:**
- `200`: Questions reloaded successfully
- `403`: Unauthorized (admin credentials required)

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

- **Kong Route:** https://api.toolweb.in/tools/cissply
- **API Docs:** https://api.toolweb.in:8175/docs
