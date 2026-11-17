## Description:

Skill Vetter Optimized helps agents and reviewers evaluate AI agent skills before installation by checking source trust, permission scope, red flags, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[confidentkai](https://clawhub.ai/user/confidentkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to vet skills from ClawHub, GitHub, or other sources before installation. It provides a structured review protocol, checklist, and helper script for triaging obvious risk signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script may be mistaken for a complete security scanner.

Mitigation: Use it only for quick triage and complete the documented full review before trusting a skill.

Risk: The workflow is Chinese-oriented, which may reduce review accuracy for teams that cannot read the source language.

Mitigation: Use qualified reviewers or translation support so all checklist items, findings, and verdicts are understood before installation.

## Reference(s):

- [Skill Review Checklist](references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/confidentkai/skills/skill-vetter-optimized)
- [Publisher Profile](https://clawhub.ai/user/confidentkai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and checklist-style review output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a skill vetting report with source, author, version, red flags, permission needs, risk level, verdict, and notes.]

## Skill Version(s):

2.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
