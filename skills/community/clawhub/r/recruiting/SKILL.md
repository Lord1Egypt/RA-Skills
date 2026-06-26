---
name: recruiting-pro
description: Hiring workflow management with structured processes and candidate tracking. Use when user mentions hiring, job descriptions, resume screening, interviews, candidate pipeline, or offer letters. Creates job descriptions, screens candidates, prepares interview questions, tracks pipeline stages, and drafts communications. All candidate data stored locally. NEVER makes hiring decisions or replaces human judgment.
---

# Recruiting

Structured hiring system. Better process, better hires.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All hiring data stored locally only**: `memory/recruiting/`
- **Candidate information never shared** externally
- **No integration** with external ATS or HR systems
- **No resume parsing services** - manual review only
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Write job descriptions and screening criteria
- ✅ Generate structured interview questions
- ✅ Track candidate pipeline stages
- ✅ Draft communications (for human review)
- ❌ **NEVER make hiring decisions**
- ❌ **NEVER store sensitive personal data** (SSN, DOB, etc.)
- ❌ **NEVER guarantee candidate quality** or predict success
- ❌ **NEVER replace** human judgment in hiring

### Fair Hiring Note
Structured processes improve fairness but do not eliminate bias. Human oversight required at all decision points.

## Quick Start

### Data Storage Setup
Hiring data stored in your local workspace:
- `memory/recruiting/jobs.json` - Open positions and requirements
- `memory/recruiting/candidates.json` - Candidate profiles and status
- `memory/recruiting/pipeline.json` - Hiring pipeline stages
- `memory/recruiting/interviews.json` - Interview guides and notes
- `memory/recruiting/communications.json` - Email templates and drafts

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Create Job Description
```
User: "Write a job description for a senior engineer"
→ Use scripts/create_job.py --title "Senior Engineer" --level senior
→ Generate JD with requirements, responsibilities, and screening criteria
```

### Screen Candidate
```
User: "Screen this resume for the PM role"
→ Use scripts/screen_candidate.py --job-id "JOB-123" --resume "resume.pdf"
→ Evaluate against job criteria, output match assessment
```

### Prepare Interview
```
User: "Prepare interview questions for the design role"
→ Use scripts/prep_interview.py --job-id "JOB-123" --type behavioral
→ Generate structured question set
```

### Track Pipeline
```
User: "Update candidate status to phone screen complete"
→ Use scripts/update_pipeline.py --candidate-id "CAND-456" --stage "phone-screen" --status completed
→ Move candidate in pipeline, set next actions
```

### Draft Communication
```
User: "Draft rejection email for candidate"
→ Use scripts/draft_email.py --type rejection --candidate-id "CAND-456"
→ Generate professional, personalized message for human review
```

## Module Reference

For detailed implementation:
- **Job Descriptions**: See [references/job-descriptions.md](references/job-descriptions.md)
- **Resume Screening**: See [references/resume-screening.md](references/resume-screening.md)
- **Interview Preparation**: See [references/interview-prep.md](references/interview-prep.md)
- **Pipeline Tracking**: See [references/pipeline-tracking.md](references/pipeline-tracking.md)
- **Communications**: See [references/communications.md](references/communications.md)
- **Fair Hiring**: See [references/fair-hiring.md](references/fair-hiring.md)

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `create_job.py` | Create job posting with requirements |
| `screen_candidate.py` | Evaluate resume against criteria |
| `prep_interview.py` | Generate interview question sets |
| `add_candidate.py` | Add candidate to pipeline |
| `update_pipeline.py` | Move candidate through stages |
| `view_pipeline.py` | Show current pipeline status |
| `draft_email.py` | Generate communications |
| `set_reminder.py` | Set follow-up reminders |
| `generate_report.py` | Create hiring metrics report |

## Disclaimer

This skill provides hiring process support only. All hiring decisions remain the responsibility of the hiring manager and organization. The skill does not guarantee candidate quality or success. Always comply with applicable employment laws and regulations.
