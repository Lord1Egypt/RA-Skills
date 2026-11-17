## Description:

Orchestrates a gated bug-fix workflow: reproduce and diagnose, patch within an approved file scope, validate, run global checks, and report results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to investigate and fix repository bugs through a checkpointed workflow. It guides diagnosis, scoped code changes, validation, safeguard checks, and a structured repair report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow's repeated npx tsx commands may download and run an unpinned package when tsx is not already installed.

Mitigation: Before installation, confirm that tsx is pinned in a reviewed dependency lockfile and that the workflow uses that local installation.

## Reference(s):

- [Ultravibe Bugfix on ClawHub](https://clawhub.ai/zengfr/skills/ultravibe-bugfix)
- [Server-resolved GitHub source](https://github.com/zengfr/AutoCoding/tree/main/docs/generated-skills/ultravibe-bugfix)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON]

**Output Format:** [Markdown workflow instructions with shell commands and structured JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses phase gates and bounded iterations; completion depends on tests, scope checks, and static checks passing.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
