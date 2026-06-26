---
name: Network & Security Skills Assessment Generator API
description: Generates comprehensive skill assessments and personalized learning roadmaps for network and security professionals.
---

# Overview

The Network & Security Skills Assessment Generator API is a comprehensive platform designed to evaluate technical competencies and create tailored career development pathways. Built for security professionals, students, and organizations, this API generates detailed skill assessments, personalized learning roadmaps, and certification guidance based on individual experience levels and career goals.

The API leverages a modular curriculum covering network security, cybersecurity, cloud security, and infrastructure domains. It supports multiple experience levels (beginner, intermediate, advanced), integrates with major certification frameworks, and provides both theoretical knowledge checks and hands-on lab scenarios. Organizations use this tool for talent assessment, employee development planning, and competitive skill gap analysis.

Ideal users include cybersecurity training providers, corporate HR departments, educational institutions, and individual professionals seeking structured career advancement in security roles.

## Usage

### Sample Request

```json
{
  "candidate_name": "Jane Smith",
  "organization": "Acme Corp",
  "current_role": "Junior Network Administrator",
  "experience_level": "intermediate",
  "target_career": "Network Security Engineer",
  "selected_modules": [
    "network_fundamentals",
    "firewall_management",
    "intrusion_detection",
    "vpn_configuration"
  ],
  "skill_ratings": {
    "network_fundamentals": 4,
    "firewall_management": 3,
    "intrusion_detection": 2,
    "vpn_configuration": 3
  },
  "target_certifications": [
    "CISSP",
    "CEH"
  ],
  "preferred_vendors": [
    "Cisco",
    "Palo Alto Networks"
  ],
  "include_labs": true,
  "include_questions": true,
  "weekly_study_hours": 15
}
```

### Sample Response

```json
{
  "success": true,
  "assessment_html": "<html><body><h1>Skill Assessment Report: Jane Smith</h1><p>Based on selected modules and self-ratings, your current competency profile shows strong fundamentals with growth opportunities in advanced threat detection...</p></body></html>",
  "roadmap_html": "<html><body><h1>Personalized Learning Roadmap</h1><p>Month 1-2: Deep dive into IDS/IPS architecture and deployment (20 hours). Month 3-4: Advanced firewall policy design and VPN protocols (18 hours)...</p></body></html>",
  "certification_html": "<html><body><h1>Certification Pathway</h1><p>CISSP: 18 months (prerequisite: 5 years security experience). CEH: 6-8 months (recommended after completing modules on network security fundamentals)...</p></body></html>",
  "labs_html": "<html><body><h1>Hands-On Lab Scenarios</h1><p>Lab 1: Configure Cisco ASA Firewall Rules. Lab 2: Deploy and Tune Snort IDS. Lab 3: Set up Site-to-Site VPN...</p></body></html>",
  "questions_html": "<html><body><h1>Knowledge Checks</h1><p>Question 1: What is the primary function of a firewall? A) Content filtering B) Network access control... (Correct: B)</p></body></html>",
  "generated_at": "2024-01-15T14:32:00Z"
}
```

## Endpoints

### GET /
**Summary:** Root endpoint

Returns basic API information and status.

**Parameters:** None

**Response:**
```
Content-Type: application/json
{}
```

---

### GET /api/modules
**Summary:** Get Modules

Retrieves a list of all available assessment modules (network security, firewall management, intrusion detection, VPN configuration, etc.).

**Parameters:** None

**Response:**
```
Content-Type: application/json
{}
```

---

### GET /api/careers
**Summary:** Get Careers

Lists all available career paths and roles in the security domain (Network Security Engineer, Security Architect, Incident Response Analyst, etc.).

**Parameters:** None

**Response:**
```
Content-Type: application/json
{}
```

---

### GET /api/certifications
**Summary:** Get Certifications

Returns a catalog of supported certifications (CISSP, CEH, CCNA Security, Security+, etc.) with prerequisite information.

**Parameters:** None

**Response:**
```
Content-Type: application/json
{}
```

---

### POST /api/generate-assessment
**Summary:** Generate Assessment

Creates a comprehensive skill assessment and personalized learning roadmap based on candidate profile and selected modules.

**Request Body (application/json):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `candidate_name` | string | Yes | Candidate/Student name |
| `organization` | string | No | Organization or Institution (default: empty string) |
| `current_role` | string | Yes | Current job role or student status |
| `experience_level` | string | Yes | Experience level: beginner, intermediate, or advanced |
| `target_career` | string | Yes | Target career path |
| `selected_modules` | array[string] | Yes | Array of module keys to assess |
| `skill_ratings` | object | No | Self-rated skills on 1-5 scale (default: {}) |
| `target_certifications` | array[string] | No | Array of target certification names (default: []) |
| `preferred_vendors` | array[string] | No | Array of preferred technology vendors (default: []) |
| `include_labs` | boolean | No | Include hands-on lab scenarios (default: true) |
| `include_questions` | boolean | No | Include knowledge checks and questions (default: true) |
| `weekly_study_hours` | integer | No | Weekly study hours available (default: 10) |

**Response (200):**

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Request succeeded |
| `assessment_html` | string | HTML-formatted skill assessment report |
| `roadmap_html` | string | HTML-formatted personalized learning roadmap |
| `certification_html` | string | HTML-formatted certification guidance |
| `labs_html` | string or null | HTML-formatted lab scenarios (if requested) |
| `questions_html` | string or null | HTML-formatted knowledge checks (if requested) |
| `generated_at` | string | ISO 8601 timestamp of generation |

**Error Response (422):** Returns validation errors if required fields are missing or invalid.

---

### GET /api/module/{module_key}
**Summary:** Get Module Details

Retrieves detailed information about a specific assessment module including topics, learning outcomes, and prerequisite skills.

**Parameters:**

| Parameter | Type | Location | Required | Description |
|-----------|------|----------|----------|-------------|
| `module_key` | string | path | Yes | Unique identifier for the module (e.g., "network_fundamentals") |

**Response:**
```
Content-Type: application/json
{}
```

**Error Response (422):** Returns validation error if module_key is invalid or not provided.

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

- **Kong Route:** https://api.mkkpro.com/security/network-security-skills
- **API Docs:** https://api.mkkpro.com:8158/docs
