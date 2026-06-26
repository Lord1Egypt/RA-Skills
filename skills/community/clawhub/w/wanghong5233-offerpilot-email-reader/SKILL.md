---
name: email-reader
description: Classify hiring emails and sync job status.
---

# Email Reader Skill

## Trigger

Activate when user asks:

- "帮我分类这封邮件"
- "这封邮件是面试邀请还是拒信？"
- "同步一下这封邮件对应的投递状态"
- "查看最近邮件分类记录"
- "从邮箱里拉取未读邮件并分类"
- "触发一次邮件巡检"
- "配置每天自动巡检这条链路"

## Workflow

1. If user provides sender/subject/body:
   - Call `POST http://127.0.0.1:8010/api/email/ingest`
   - Body:
     - `{"sender":"<sender>","subject":"<subject>","body":"<body>"}`
2. Parse response:
   - show `classification.email_type`
   - show `company` / `interview_time` if exists
   - show `related_job_id` + `updated_job_status` if job status was updated
3. If user asks for history:
   - Call `GET http://127.0.0.1:8010/api/email/recent?limit=20`
   - summarize top items
4. If user asks to pull unread inbox:
   - Call `POST http://127.0.0.1:8010/api/email/fetch`
   - Body: `{"max_items":10,"mark_seen":false}`
   - Return fetched_count / processed_count.
5. If user asks heartbeat trigger/status:
   - Status: `GET http://127.0.0.1:8010/api/email/heartbeat/status`
   - Trigger once: `POST http://127.0.0.1:8010/api/email/heartbeat/trigger`
   - Start scheduler: `POST http://127.0.0.1:8010/api/email/heartbeat/start`
   - Stop scheduler: `POST http://127.0.0.1:8010/api/email/heartbeat/stop`
   - Notify test: `POST http://127.0.0.1:8010/api/email/heartbeat/notify-test`
6. For OpenClaw cron integration:
   - Recommend this exact cron payload message:
     - `Use email-reader skill to trigger one email heartbeat run, then summarize fetched_count, processed_count, interview invites, and notification status.`
   - This keeps OpenClaw heartbeat and backend `/api/email/heartbeat/trigger` on the same execution path.

## Command templates (exec tool + curl)

- Ingest:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/ingest" -H "Content-Type: application/json" -d '{"sender":"hr@example.com","subject":"面试邀请","body":"请于明天下午参加面试"}'`
- Recent:
  - `curl -sS "http://127.0.0.1:8010/api/email/recent?limit=20"`
- Fetch unread:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/fetch" -H "Content-Type: application/json" -d '{"max_items":10,"mark_seen":false}'`
- Heartbeat status:
  - `curl -sS "http://127.0.0.1:8010/api/email/heartbeat/status"`
- Heartbeat trigger:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/heartbeat/trigger"`
- Heartbeat start:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/heartbeat/start"`
- Heartbeat stop:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/heartbeat/stop"`
- Notify test:
  - `curl -sS -X POST "http://127.0.0.1:8010/api/email/heartbeat/notify-test" -H "Content-Type: application/json" -d '{"message":"OfferPilot test"}'`
- Suggested OpenClaw cron message:
  - `Use email-reader skill to trigger one email heartbeat run, then summarize fetched_count, processed_count, interview invites, and notification status.`

## Constraints

- Never send emails automatically.
- If classification confidence is low or type is `irrelevant`, clearly tell user uncertainty.
- For malformed input or API failure, surface exact error and ask whether to retry.
