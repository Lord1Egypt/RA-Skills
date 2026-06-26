# Checkpoint Format — Full Template

Use this template when writing any checkpoint file.

---

## Minimal Checkpoint

```markdown
# Checkpoint: build-login-page

**Created:** 2026-05-12 15:45 GMT+8
**Task:** Build login page with OAuth fallback

## Progress
- Created `src/pages/LoginPage.tsx`
- Implemented email/password form with validation
- Added OAuth redirect handler (Google + GitHub)
- Login state stored in `src/store/auth.ts`

## Next Action
Run `npm test -- --grep "LoginPage"` to verify existing tests pass,
then implement the OAuth callback handler at `src/pages/OAuthCallback.tsx`

## Blockers
- None — all dependencies installed

## Key Decisions
- Chose email+OAuth combo (not password-only) per user preference for speed
- Using Zustand for auth state (lighter than Redux, user approved)

## Relevant Context
- Project root: `~/projects/web-app`
- User preference: verbose error messages, Chinese UI labels
- API base: `http://localhost:3001/api`
```

---

## Checkpoint with Deep Stack (Multi-day)

```markdown
# Checkpoint: analyze-q1-data

**Created:** 2026-05-10 22:15 GMT+8
**Task:** Full Q1 financial data analysis + report generation

## Progress

### Day 1 (2026-05-09)
- Fetched raw transaction data via `python scripts/fetch_transactions.py`
- Cleaned 47k rows, removed duplicates
- Saved to `data/q1_clean.csv`

### Day 2 (2026-05-10)
- Ran revenue segmentation: `python scripts/segment.py --input data/q1_clean.csv --output data/segments/`
- Generated 4 segments: Enterprise, SMB, Consumer, Trial
- Found anomaly in Enterprise segment (Q1 week 3 revenue spike +38%)
- Started investigating root cause

### Current Stack
- Anomaly investigation stopped mid-way
- `data/segments/enterprise_q1.csv` has 12k rows with spike
- `scripts/investigate_anomaly.py` exists but not yet run
- Root cause likely a single large transaction from "Acme Corp" (invoice #10423)

## Next Action
Run `python scripts/investigate_anomaly.py --invoice 10423` to confirm
Acme Corp invoice is the spike source, then decide whether to exclude from report.

## Blockers
- Invoice #10423 details not yet fetched (API returned partial data)
- User needs to confirm: include or exclude anomalous transaction in final report?

## Key Decisions
- Using median instead of mean for averages (resistant to outliers like this spike)
- Report should be in Chinese (user's primary language)
- Charts generated as PNG (not interactive HTML) for email compatibility

## Relevant Context
- Project: `~/projects/q1-analysis`
- User: wangjipeng, preference Chinese output
- Deadline: report needed by 2026-05-14
- Email for delivery: jipeng@example.com
```

---

## Checkpoint After Context Warning

```markdown
# Checkpoint: refactor-api-client

**Created:** 2026-05-12 16:55 GMT+8
**Task:** Refactor `src/utils/api-client.ts` to support retry + timeout

## Progress
- Identified 3 functions needing retry logic: `get`, `post`, `upload`
- Implemented exponential backoff in `src/utils/retry.ts`
- Updated `api-client.ts` to use retry wrapper (lines 1-80 done)
- Still need to update `upload` function (lines 150-200)

## Next Action
Update `upload` function in `src/utils/api-client.ts` lines 150-200:
- Add retry wrapper with 3 max attempts
- Add 30s timeout
- Test with `curl -X POST http://localhost:3001/api/upload -d "test"`

## Blockers
- Need test file >5MB — currently don't have one
- May need to create dummy file with `dd if=/dev/zero of=test.bin bs=1M count=6`

## Key Decisions
- Retry on: 408, 429, 500, 502, 503, 504
- Do NOT retry on: 400, 401, 403 (auth errors — would amplify the problem)
- Timeout: 30s for all requests
- Log retries at WARN level (not ERROR) — they are expected behavior
```

---

## Anti-Pattern: Bad Checkpoint

```markdown
# Checkpoint: task

**Created:** 2026-05-12

Worked on some things. Made progress. Next is to continue.

## Progress
Did some stuff

## Next Action
Continue

## Blockers
Not sure
```

**Why it's bad:** No specific file, no specific command, no way to resume without asking questions.