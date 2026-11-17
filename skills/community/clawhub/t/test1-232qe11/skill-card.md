## Description:

Captures learnings, errors, feature requests, and corrections in markdown logs so agents can carry forward useful project knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a6191187](https://clawhub.ai/user/a6191187)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, knowledge gaps, and requested capabilities into project-local markdown files, then promote durable learnings into agent memory or reusable skills after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted memory files can preserve sensitive data, outdated conclusions, or incorrect guidance across future sessions.

Mitigation: Keep logs project-local where possible, avoid secrets, credentials, raw transcripts, and full command output, and require manual review before promoting content into agent memory files.

Risk: Optional hooks can inject reminders into future prompts and, when error detection is enabled, inspect command output that may contain sensitive details.

Mitigation: Enable hooks only after review, prefer the minimal activator-only setup, avoid global hooks unless intentionally desired, and treat command output as sensitive.

Risk: Unreviewed updates could change how future agents record or apply project learnings.

Mitigation: Install a pinned version or reviewed local copy and review diffs before updating or sharing promoted learnings.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets, configuration examples, and log-entry templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include project-local learning files, hook setup instructions, and skill scaffolding guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
