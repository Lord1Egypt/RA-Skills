## Description:

Security scanner for OpenClaw agent skills that supports pre-install ClawHub checks, local read-only pattern scanning, and user-initiated integrity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review OpenClaw skills before installation, audit installed skills for dangerous patterns or secrets, and compare user-approved integrity baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the zero-exec and read-only framing conflicts with browser use, a local CLI fallback, and baseline-writing instructions.

Mitigation: Use browser and CLI checks only with clearly validated skill slugs, avoid shell interpolation, and treat saved baselines as review aids rather than strong tamper detection.

Risk: The skill may read installed skill files and save user-requested baseline records.

Mitigation: Run scans only on intended local skill directories and create baselines only after explicit user approval.

## Reference(s):

- [Skill Guard ClawHub page](https://clawhub.ai/tommot2/skills/tommo-skill-guard)
- [Security Pattern Reference](references/security-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style scan reports and concise risk guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports security status, file counts, pattern findings, and recommended user review steps.]

## Skill Version(s):

5.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
