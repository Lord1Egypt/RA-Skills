---
name: Resume Builder
description: Generate professional resumes and cover letters from structured data with optional resume parsing capabilities.
---

# Overview

Resume Builder is a professional document generation API that transforms structured candidate data into polished, ATS-friendly resumes and cover letters. Built for recruiters, HR professionals, and career service platforms, it streamlines the resume creation process while maintaining consistent formatting and professional presentation standards.

The tool supports comprehensive resume data including work experience, education, skills, certifications, and accomplishments. It can simultaneously generate matching cover letters tailored to specific job opportunities. Resume Builder also includes parsing capabilities to extract structured data from existing resume documents, making it ideal for resume optimization workflows and bulk document generation scenarios.

Ideal users include recruitment agencies, career coaching platforms, applicant tracking systems, HR departments, and job placement services seeking to programmatically create or enhance professional documents at scale.

## Usage

**Generate a Resume and Cover Letter:**

```json
{
  "resume_data": {
    "full_name": "Sarah Chen",
    "email": "sarah.chen@email.com",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    "linkedin": "linkedin.com/in/sarahchen",
    "portfolio": "sarahchen.dev",
    "tagline": "Full-Stack Engineer | Cloud Architecture",
    "summary": "6+ years building scalable cloud solutions with focus on infrastructure automation and team leadership.",
    "experiences": [
      {
        "title": "Senior Software Engineer",
        "company": "CloudCorp Inc",
        "location": "San Francisco, CA",
        "start_date": "Jan 2021",
        "end_date": "Present",
        "highlights": [
          "Led migration of monolithic application to microservices reducing latency by 40%",
          "Architected and deployed Kubernetes infrastructure supporting 500+ deployments monthly",
          "Mentored team of 5 junior engineers on cloud-native best practices"
        ]
      },
      {
        "title": "Software Engineer",
        "company": "TechStart LLC",
        "location": "Oakland, CA",
        "start_date": "Jun 2018",
        "end_date": "Dec 2020",
        "highlights": [
          "Developed backend APIs serving 2M+ daily requests",
          "Implemented CI/CD pipeline reducing deployment time from 45 min to 8 min"
        ]
      }
    ],
    "education": [
      {
        "degree": "BS Computer Science",
        "institution": "UC Berkeley",
        "location": "Berkeley, CA",
        "year": "2018",
        "gpa": "3.8"
      }
    ],
    "skills": ["Python", "Go", "Kubernetes", "AWS", "Docker", "Terraform", "PostgreSQL"],
    "certifications": ["AWS Solutions Architect Professional", "CKA - Certified Kubernetes Administrator"],
    "tools": ["Git", "Jenkins", "Prometheus", "Grafana"],
    "accomplishments": ["Published article on infrastructure optimization in IEEE Software"]
  },
  "cover_letter_data": {
    "full_name": "Sarah Chen",
    "email": "sarah.chen@email.com",
    "phone": "+1-555-0123",
    "location": "San Francisco, CA",
    "company_name": "InnovateTech Solutions",
    "company_location": "Mountain View, CA",
    "job_title": "Staff Engineer - Platform",
    "job_description": "Lead architecture and implementation of next-gen distributed systems platform",
    "key_highlights": [
      "Proven track record scaling systems to millions of requests per second",
      "Deep expertise in Kubernetes and cloud infrastructure",
      "Strong mentorship and technical leadership experience"
    ]
  },
  "generate_cover_letter": true
}
```

**Sample Response:**

```json
{
  "status": "success",
  "resume_filename": "resume_sarah_chen_20240115.pdf",
  "cover_letter_filename": "cover_letter_sarah_chen_20240115.pdf",
  "download_urls": {
    "resume": "/download/resume_sarah_chen_20240115.pdf",
    "cover_letter": "/download/cover_letter_sarah_chen_20240115.pdf"
  },
  "generation_time_ms": 2341
}
```

## Endpoints

### GET /
**Root Endpoint**

Returns service information and status.

**Response:** Service metadata object.

---

### GET /status
**Status Check**

Verifies API availability and health.

**Response:** JSON object containing service status and uptime information.

---

### POST /generate
**Generate Resume and/or Cover Letter**

Generates professional resume and optionally cover letter documents from structured data.

**Request Body:**
- `resume_data` (ResumeData, **required**) - Core resume information including name, contact details, experience, education, and skills
- `cover_letter_data` (CoverLetterData, optional) - Cover letter details including company and job information
- `generate_cover_letter` (boolean, optional, default: `true`) - Whether to generate accompanying cover letter

**ResumeData Schema (required fields: `full_name`, `email`, `phone`):**
- `full_name` (string, **required**) - Candidate full name
- `email` (string, **required**) - Email address
- `phone` (string, **required**) - Phone number
- `location` (string, optional) - City/region
- `linkedin` (string, optional) - LinkedIn profile URL
- `portfolio` (string, optional) - Portfolio or personal website URL
- `tagline` (string, optional) - Professional headline/tagline
- `availability` (string, optional) - Availability status (e.g., "Immediately", "2 weeks")
- `summary` (string, optional) - Professional summary/objective
- `experiences` (array of Experience objects, optional) - Work history
  - `title` (string) - Job title
  - `company` (string) - Company name
  - `location` (string) - Job location
  - `start_date` (string) - Start date
  - `end_date` (string, default: "Present") - End date
  - `highlights` (array of strings) - Key accomplishments
- `education` (array of Education objects, optional) - Educational background
  - `degree` (string) - Degree name (e.g., "BS Computer Science")
  - `institution` (string) - School/university name
  - `location` (string) - School location
  - `year` (string) - Graduation year
  - `gpa` (string) - GPA (optional)
- `skills` (array of strings, optional) - Technical and soft skills
- `certifications` (array of strings, optional) - Professional certifications
- `tools` (array of strings, optional) - Software/tools proficiency
- `accomplishments` (array of strings, optional) - Awards and achievements
- `other_employers` (array of strings, optional) - Additional employer references
- `job_description` (string, optional) - Target job description for resume optimization
- `original_resume` (string, optional) - Existing resume text for enhancement

**CoverLetterData Schema (required fields: `full_name`, `email`, `phone`, `company_name`, `job_title`):**
- `full_name` (string, **required**)
- `email` (string, **required**)
- `phone` (string, **required**)
- `location` (string, optional)
- `date` (string, optional)
- `hiring_manager` (string, optional, default: "Hiring Manager")
- `company_name` (string, **required**)
- `company_location` (string, optional)
- `company_address` (string, optional)
- `job_title` (string, **required**)
- `job_description` (string, optional)
- `opening_paragraph` (string, optional)
- `body_paragraph` (string, optional)
- `closing_paragraph` (string, optional)
- `key_highlights` (array of strings, optional)

**Response:** JSON object with `status`, document filenames, download URLs, and generation timestamp.

**Error Responses:**
- `422 Validation Error` - Invalid request schema or missing required fields

---

### POST /parse-resume
**Parse Resume Endpoint**

Extracts structured data from unstructured resume documents for re-generation or updating.

**Request Body:**
- `data` (object, **required**) - Resume content as flexible object (supports various input formats including text, PDF metadata, or document content)

**Response:** Structured JSON object matching ResumeData schema with extracted fields.

**Error Responses:**
- `422 Validation Error` - Invalid input format or unparseable resume content

---

### GET /download/{filename}
**Download Generated Document**

Retrieves generated resume or cover letter file.

**Path Parameters:**
- `filename` (string, **required**) - Document filename returned from `/generate` endpoint

**Response:** File download (PDF or specified format).

**Error Responses:**
- `422 Validation Error` - Invalid or non-existent filename

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

- Kong Route: https://api.toolweb.in/tools/resumy
- API Docs: https://api.toolweb.in:8166/docs
