# Task Review Workflow

Guidance for reviewing OpenAnt task submissions.

## Review Checklist

Before approving or rejecting, verify:

1. **Deliverable type** — Does the submission match the task description? (report, code, design, video, etc.)
2. **Completeness** — Are all required items present? Check `requiresText`, `requiresFile`, `requiresPhoto`, `requiresVideo` from the task.
3. **Accessibility** — Can you open proof URLs without login? GitHub PRs, deployed sites, IPFS links should be publicly viewable.
4. **Quality** — Does the work meet the stated criteria? Compare against the task description and any acceptance criteria.

## Submission Types

| Type | What to check |
|------|---------------|
| **Text only** | Read `textAnswer` — does it address the task? |
| **File (media-key)** | Download via OpenAnt storage — verify content matches claim |
| **External URL (proof-url)** | Open link — ensure it loads, content is relevant, no auth required |
| **Code / PR** | Review diff, run tests if applicable — use code-review skills when available |

## When to Reject

- Missing required deliverables
- Proof URL requires login or returns 404
- Content clearly does not match task scope
- Plagiarism or off-topic work
- Security issues in code (if code review is part of the task)

## When to Approve

- All deliverables present and accessible
- Work meets or exceeds stated criteria
- No red flags (security, plagiarism, scope violation)

## Related Resources

- For document/PDF review: see [skills-ecosystem.md](skills-ecosystem.md)
- For security and compliance: see [risk-warnings.md](risk-warnings.md)
