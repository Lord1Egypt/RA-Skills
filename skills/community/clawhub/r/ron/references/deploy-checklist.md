# Deploy Checklist

Ron runs this automatically on every deploy review. Customize for your stack.

## Pre-Deploy

- [ ] Root cause confirmed in logs/errors — not guessed
- [ ] Fix addresses root cause, not just symptom
- [ ] Same pattern checked in adjacent files/routes
- [ ] All environment variables present in deploy target (not just local)
- [ ] No secrets or credentials hardcoded

## For Next.js / Vercel / Amplify

- [ ] Server-side env vars added to `next.config.ts` (SSR Lambda can't see process.env otherwise)
- [ ] Build cache not stale — force rebuild if env vars changed
- [ ] API routes tested with actual deployed URL, not localhost
- [ ] CloudWatch / deploy logs checked after deploy (not just build success)

## For Any Cloud Deploy

- [ ] Rollback plan confirmed (can you revert in < 5 min?)
- [ ] Monitoring/alerting in place for the changed surface
- [ ] No direct pushes to main without review (unless explicitly allowed)

## Post-Deploy

- [ ] Smoke test on the actual failing case (not a similar case)
- [ ] Logs clean — no new errors in first 5 minutes
- [ ] End-to-end user flow tested (not just unit test passing)

---

*Add stack-specific checks below. This file lives in your skills/ron/references/ directory.*
