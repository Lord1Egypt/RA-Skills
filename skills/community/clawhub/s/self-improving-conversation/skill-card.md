## Description:

Captures redacted dialogue learnings, tone mismatches, escalation failures, context loss, hallucinations, and requested conversational capabilities in local `.learnings/` files, with optional project-scoped reminder hooks and reviewed promotion workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture recurring conversation failures as redacted local markdown learnings, review patterns, and promote proven fixes into agent guidance or extracted skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local conversation-quality logs can retain private data if entries are too detailed.

Mitigation: Keep `.learnings/` ignored by git, redact aggressively, and never store credentials, PII, or private data.

Risk: Optional hooks persist across sessions and can create reminders in projects where they are not appropriate.

Mitigation: Enable hooks only in intended projects, keep them project-scoped, and use narrow matchers.

Risk: Promoting learnings into prompt or agent files can spread incorrect or misleading guidance.

Mitigation: Promote only proven patterns and apply changes only after explicit human review of a diff.

Risk: Installing from a mutable branch can bypass the reviewed release artifact.

Mitigation: Prefer ClawdHub or a pinned reviewed commit over cloning a mutable branch manually.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jose-compu/skills/self-improving-conversation)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON hook configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append redacted local markdown entries and propose reviewed diffs for prompt or skill files; optional hooks emit reminder text only.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
