## Description:

A Chinese-language pre-installation review protocol for evaluating AI agent skills for credential theft, obfuscation, data exfiltration, permission scope, and installation risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xocio](https://clawhub.ai/user/xocio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill before installing or running third-party skills to inspect source, permissions, network behavior, and risk indicators, then produce a structured review report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual checklist results can miss issues if the reviewer skips files or relies only on source reputation.

Mitigation: Read all files in the candidate skill, compare requested permissions to the stated purpose, and pair the manual review with automated scans where available.

Risk: Example shell commands may fetch remote content or print local files when copied without adapting the target path or repository.

Mitigation: Run review commands only against a temporary copy of the candidate skill or its public repository, and inspect domains and paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xocio/skills/skill-vetter-zh)
- [README project link](https://clawhub.ai/spclaudehome/skill-vetter)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown review checklist and structured security report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language review workflow with risk grading and install recommendations]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
