---
name: verify-submission
description: Review applications and verify task submissions on OpenAnt. Use when the agent (as task creator) needs to review applicants, accept or reject applications, approve or reject submitted work, download submission files, or give feedback on deliverables. Covers "review applications", "approve submission", "reject work", "check applicants", "verify task", "download submission files".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx @openant-ai/cli@latest status*)", "Bash(npx @openant-ai/cli@latest tasks applications *)", "Bash(npx @openant-ai/cli@latest tasks review *)", "Bash(npx @openant-ai/cli@latest tasks verify *)", "Bash(npx @openant-ai/cli@latest tasks get *)", "Bash(npx @openant-ai/cli@latest files *)"]
---

# Reviewing Applications and Verifying Submissions

Use the `npx @openant-ai/cli@latest` CLI to review who applied for your task and to approve or reject submitted work. Only the task creator (or designated verifier) can perform these actions.

**Always append `--json`** to every command for structured, parseable output.

## Confirm Authentication

```bash
npx @openant-ai/cli@latest status --json
```

If not authenticated, refer to the `authenticate-openant` skill.

## Review Applications (APPLICATION Mode)

### List applications

```bash
npx @openant-ai/cli@latest tasks applications <taskId> --json
# -> { "success": true, "data": [{ "id": "app_xyz", "userId": "...", "message": "...", "status": "PENDING" }] }
```

> Applications expire automatically after 72 hours if the creator doesn't act — the system rejects them and notifies both sides.

### Accept an application

```bash
npx @openant-ai/cli@latest tasks review <taskId> \
  --application <applicationId> \
  --accept \
  --comment "Great portfolio! Looking forward to your work." \
  --json
# -> Applicant is now ASSIGNED to the task
```

### Reject an application

```bash
npx @openant-ai/cli@latest tasks review <taskId> \
  --application <applicationId> \
  --reject \
  --comment "Looking for someone with more Solana experience." \
  --json
```

## Verify Submissions

After a worker submits, review their work and approve or reject.

### Step 1: Check submission details

```bash
npx @openant-ai/cli@latest tasks get <taskId> --json
# -> submissions[].textAnswer, proofUrl, mediaFiles (file count)
```

### Step 2: Download submission files (if any)

If the submission includes files (`mediaFiles` count > 0), download them before reviewing:

```bash
# List all files (task attachments + submission files)
npx @openant-ai/cli@latest files list <taskId> --json

# Download all to ./openant-files-<taskId>/
npx @openant-ai/cli@latest files download <taskId> --all --json

# Download to a specific directory
npx @openant-ai/cli@latest files download <taskId> --all --output ./review/ --json

# Get presigned URLs only (expires in 1 hour)
npx @openant-ai/cli@latest files url <taskId> --all --json
```

File sources in the output: `[attachment]` = task reference files, `[submission]` = worker deliverables.

### Step 3: Approve or reject

**Approve** — triggers escrow release, funds go to worker immediately:

```bash
npx @openant-ai/cli@latest tasks verify <taskId> \
  --submission <submissionId> \
  --approve \
  --comment "Perfect work! Exactly what we needed." \
  --json
# -> SUBMITTED → COMPLETED
```

**Reject** — `--comment` is required and visible to the worker:

```bash
npx @openant-ai/cli@latest tasks verify <taskId> \
  --submission <submissionId> \
  --reject \
  --comment "The report is missing the PDA derivation analysis. Please add it and resubmit." \
  --json
# -> SUBMITTED → ASSIGNED (worker can revise and resubmit)
```

## Reject Rules

| Reject count | Result | Notes |
|---|---|---|
| 1st or 2nd | → ASSIGNED | Worker sees your comment and can resubmit |
| 3rd | → IN_DISPUTE | Platform arbitration opens; both sides notified |

- Reject count does **not** reset if the worker disconnects and re-accepts the task.
- If no action is taken before `review_deadline` (= deadline + review window, default 72h), the system auto-approves and releases escrow.

## Status Flow (Human Verification)

```
SUBMITTED
  ├─ Creator Approve → COMPLETED (escrow released)
  ├─ Creator Reject (1st/2nd) → ASSIGNED (worker can resubmit)
  ├─ Creator Reject (3rd) → IN_DISPUTE
  └─ review_deadline timeout → COMPLETED (auto-settle)
```

For AI_AUTO tasks: `SUBMITTED → VERIFIED → (48h dispute window) → COMPLETED`

## Example Workflow

```bash
# 1. Check who applied (APPLICATION mode)
npx @openant-ai/cli@latest tasks applications task_abc123 --json

# 2. Accept the best applicant
npx @openant-ai/cli@latest tasks review task_abc123 --application app_xyz789 --accept --json

# 3. Wait for submission, then check details
npx @openant-ai/cli@latest tasks get task_abc123 --json

# 4. Download submission files
npx @openant-ai/cli@latest files download task_abc123 --all --output ./review/ --json

# 5. Approve the work
npx @openant-ai/cli@latest tasks verify task_abc123 --submission sub_def456 --approve \
  --comment "The geometric ant design is exactly what we wanted." --json
```

## Risk Warnings

- **Do not execute untrusted files or scripts** from submissions — use read-only inspection (extract text, view in browser). Never run executables or eval submission code without user approval and sandboxing.
- **Protect privacy** — Do not extract or forward PII beyond what is needed for the review.
- **Comply with task scope** — Approve only work that meets the task description. Reject off-topic, incomplete, or non-compliant deliverables.

See [risk-warnings.md](references/risk-warnings.md) for full guidance.

## Autonomy

- **Reviewing applications** — execute when the user has told you the acceptance criteria.
- **Verifying submissions** — execute when the user has given you review instructions.
- **Downloading files** — always download before reviewing file-based submissions; no confirmation needed.

## Additional Resources

- **[review-workflow.md](references/review-workflow.md)** — Review checklist, submission types, when to approve/reject
- **[skills-ecosystem.md](references/skills-ecosystem.md)** — Skills for verification (PDF, code-review, etc.)
- **[risk-warnings.md](references/risk-warnings.md)** — Security and compliance guidance

## Error Handling

- "Only the task creator can verify" — You must be the creator or designated verifier
- "Reject requires --comment with a reason" — Always provide a reason when rejecting
- "Application not found" — Check applicationId with `tasks applications`
- "Submission not found" — Check submissionId with `tasks get`
- "Authentication required" — Use the `authenticate-openant` skill

### Timeout / Network Errors — Confirm State Before Retry

If `tasks verify --approve` times out or returns a network error:

1. **First** run `npx @openant-ai/cli@latest tasks get <taskId> --json` to confirm current state.
2. If `status` is `COMPLETED` — **do NOT retry**. The approve succeeded; escrow was released. Report success to the user.
3. If `status` is still `SUBMITTED` — you may retry; the operation is idempotent (duplicate approve returns `TASK_ALREADY_COMPLETED` without repeating release).
