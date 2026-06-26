---
name: resume-tailor
description: Generate, review, and export tailored application materials.
---

# Resume Tailor Skill

## Trigger

Activate when user asks:

- "Generate tailored resume for this job"
- "Help me create application materials"
- "Approve/reject this material draft"
- "Export approved material"

## Workflow

1. If user provides `job_id`, call material generation API:
   - `POST http://127.0.0.1:8010/api/material/generate`
   - Body: `{"job_id":"<job_id>","resume_version":"resume_v1"}`
2. Parse JSON response:
   - If `status=skipped_low_match`, explain low match and ask whether to continue with another job.
   - If `status=pending_review`, show:
     - `thread_id`
     - resume bullets
     - cover letter
     - greeting message
3. Ask user for review decision:
   - `approve` / `reject` / `regenerate` (optional feedback text)
4. Execute review call:
   - `POST http://127.0.0.1:8010/api/material/review`
   - Body example:
     - `{"thread_id":"<thread_id>","decision":"regenerate","feedback":"强调可量化结果"}`
5. If approved, export file:
   - `POST http://127.0.0.1:8010/api/material/export`
   - Body: `{"thread_id":"<thread_id>","format":"pdf"}`
   - Return file name/path/download URL to user.

## Command templates (exec tool + curl)

- Generate:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/generate" -H "Content-Type: application/json" -d '{"job_id":"<job_id>","resume_version":"resume_v1"}'`
- Review:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/review" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","decision":"approve"}'`
- Export:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/material/export" -H "Content-Type: application/json" -d '{"thread_id":"<thread_id>","format":"pdf"}'`

## Constraints

- Never auto-submit external applications.
- For every approve/reject action, require explicit user confirmation.
- If API errors or invalid JSON appear, surface the error clearly and ask user whether to retry.
