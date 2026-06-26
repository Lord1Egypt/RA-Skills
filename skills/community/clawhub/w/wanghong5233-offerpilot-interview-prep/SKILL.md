---
name: interview-prep
description: Generate interview question bank and answer strategy from JD and company intel.
---

# Interview Prep Skill

## Trigger

Activate when user asks:

- "帮我准备这家公司的面试题"
- "根据 JD 出一套面试问题"
- "给我这岗位的回答思路"
- "做一版可背诵的面试提纲"

## Workflow

1. Collect input:
   - Prefer `job_id` (from `/api/jobs/recent`) OR provide `company + role_title + jd_text`.
2. Call:
   - `POST http://127.0.0.1:8010/api/interview/prep`
   - Body example:
     - `{"job_id":"<job_id>","use_company_intel":true,"question_count":8}`
   - Or:
     - `{"company":"MiniAgent","role_title":"AI Agent Intern","jd_text":"...","use_company_intel":true,"question_count":8}`
3. Parse response and present:
   - `summary`
   - `likely_focus`
   - `key_storylines`
   - top interview questions (`question`, `intent`, `answer_tips`)
4. Ask user whether to export/continue with mock Q&A.

## Command templates (exec tool + curl)

- By job id:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/interview/prep" -H "Content-Type: application/json" -d '{"job_id":"<job_id>","use_company_intel":true,"question_count":8}'`
- By custom input:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/interview/prep" -H "Content-Type: application/json" -d '{"company":"MiniAgent","role_title":"AI Agent Intern","jd_text":"Need Python, LangGraph, RAG","use_company_intel":true,"question_count":8}'`

## Constraints

- Keep output concise and actionable (avoid long generic theory).
- If API returns non-2xx, surface the raw error and ask user whether to retry.
- Do not claim interview certainty; present as "likely focus" with confidence.
