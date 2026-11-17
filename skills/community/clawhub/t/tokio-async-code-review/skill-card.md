## Description:

Reviews Tokio async runtime usage in Rust code, including task management, synchronization primitives, channel patterns, runtime configuration, and Rust 2024 async changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Rust code that uses Tokio or async/await. It guides checks for runtime setup, task lifecycle, blocking operations, synchronization, channels, cancellation, and evidence-backed severity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review findings may be incorrect or overstate severity when dependency, runtime, or blocking evidence is incomplete.

Mitigation: Complete the documented gates and require file:line evidence before reporting Critical or Major issues.

Risk: Suggested async changes can alter runtime behavior, cancellation, locking, or concurrency limits.

Mitigation: Treat the output as review guidance and confirm changes against project tests and relevant Tokio or Rust behavior before applying them.

## Reference(s):

- [Task Management](references/task-management.md)
- [Sync Primitives](references/sync-primitives.md)
- [Channels](references/channels.md)
- [Pinning, Cancellation, and Async Internals](references/pinning-cancellation.md)
- [Review Verification Protocol](../review-verification-protocol/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with file:line findings, severity labels, and concise descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings require gate checks and file:line evidence before Critical or Major severity is asserted.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
