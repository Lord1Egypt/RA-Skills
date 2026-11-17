## Description:

Capture user corrections, failed tool runs, recurring gotchas, and useful lessons as short structured notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture corrections, failed tool runs, recurring project gotchas, and missing capabilities as concise, redacted, project-scoped notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning notes could accidentally retain private data, credentials, customer information, or excessive command output.

Mitigation: Write short redacted summaries and avoid storing credentials, private messages, customer data, full transcripts, or full command output.

Risk: A captured lesson could be promoted into durable agent or project instructions before it has enough review.

Mitigation: Treat durable instruction changes as proposals and require explicit user approval before editing instructions, hooks, or configuration.

Risk: Project-local learning notes can become stale or misleading over time.

Mitigation: Review .learnings notes periodically, link recurring issues, and mark resolved or proposed notes with the approved destination.

## Reference(s):

- [Learning Capture README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/brasco05/skills/self-improving-agent1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown notes plus brief text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates project-local .learnings notes; captured context should remain redacted and human-reviewable.]

## Skill Version(s):

1.0.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
