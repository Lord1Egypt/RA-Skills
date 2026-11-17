# Review Loop

Use this review only when the user invokes it, at an agreed task breakpoint, or
as part of explicitly configured maintenance.

## Review sequence

1. Gather pending chronological, incident, and request entries.
2. Remove candidates that are obsolete, unsupported, sensitive, or too
   task-specific to reuse.
3. Search existing durable guidance and retrieve full matching documents.
4. Apply the promotion threshold in `SKILL.md`.
5. Identify contradictions, owners, and documents that would be superseded.
6. Present proposed promotions for approval.
7. Write only approved changes, then update each source entry's status.
8. Re-index QMD when appropriate and report exact changes.

## Conflict handling

When a candidate conflicts with existing guidance:

- do not choose a winner based only on recency;
- identify each source's authority and owner;
- preserve the candidate as `blocked` or `needs-review`;
- ask the responsible user to resolve the conflict; and
- link the resolution or superseding decision from both records.

## Prevention-oriented writing

Prefer a short rule with a clear condition and action:

> When operating outside a repository checkout, always pass the repository
> explicitly.

Do not copy incident narratives, chat transcripts, or raw command output into
durable guidance. Link to the evidence entry instead.
