## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can maintain project learning logs and promote recurring guidance into agent memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[991200448](https://clawhub.ai/user/991200448)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and recurring patterns as Markdown learning entries. They can then review and promote high-value learnings into agent instruction or memory files for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs or promoted memory files may store user-derived sensitive content or agent-control instructions.

Mitigation: Review entries before promotion and redact secrets, customer data, transcripts, tokens, proprietary prompts, and raw command outputs before writing to learning or instruction files.

Risk: Global or user-level hooks can make learning reminders active across projects.

Mitigation: Prefer project-scoped hooks where possible and enable only the hooks intentionally needed for the workspace.

Risk: Promoted learnings can introduce incorrect or misleading guidance into future agent sessions.

Mitigation: Review and scan learning entries before promotion, resolve stale entries, and keep promoted guidance concise and specific.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs and agent instruction files when the agent follows the guidance; optional hooks emit reminders.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
