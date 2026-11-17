## Description:

Omnia helps agents use continuity infrastructure for persistent memory, crash recovery, audit trails, heartbeat monitoring, coherence checks, and witness-gated critical actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arturoaguileraa](https://clawhub.ai/user/arturoaguileraa)

### License/Terms of Use:

MIT + Attribution Required

## Use Case:

Developers and agent operators use Omnia to add or reason about persistent agent memory, recovery snapshots, audit trails, heartbeat monitoring, coherence checks, and human approval gates for critical actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and append-only audit logs can capture sensitive data without clear privacy, deletion, or scoping controls.

Mitigation: Use only where persistent memory and audit logs are explicitly wanted; avoid logging secrets or raw prompts by default, define retention and deletion procedures, and restrict file permissions.

Risk: The skill directs agents toward installing an external package.

Mitigation: Pin or audit the external package version before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arturoaguileraa/skills/test-omnia)
- [Molt Project Site](https://molt.church)
- [X-Loop3 Labs](https://x-loop3.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
