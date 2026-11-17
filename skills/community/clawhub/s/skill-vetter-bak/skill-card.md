## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aysun168](https://clawhub.ai/user/aysun168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before installing or running third-party skills to review source, scope permissions, classify risk, and document an installation verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vetting GitHub-hosted skills may prompt network requests to GitHub or raw file URLs.

Mitigation: Review proposed commands and destination domains before execution, avoid sending credentials, and run checks from a least-privileged workspace.

Risk: A checklist-based review can miss unsafe behavior if the reviewer skips files or accepts incomplete evidence.

Mitigation: Review every artifact file, document unresolved questions, and require human approval for high-risk or credential-related findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aysun168/skills/skill-vetter-bak)
- [Publisher profile](https://clawhub.ai/user/aysun168)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown report with checklist-style fields and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single vetting report; may include proposed GitHub API curl commands for reviewer use.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
