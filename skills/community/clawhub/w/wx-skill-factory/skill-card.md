## Description:

Skill Factory guides an agent through iterative creation, testing, refinement, and modularization of new skills across manual, semi-automatic, and fully automatic modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mwangxiang](https://clawhub.ai/user/mwangxiang)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to design, generate, test, compare, iterate, and deliver new agent skills from user requirements. It also supports improving existing skills and splitting stable workflow steps into reusable sub-skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may call third-party AI services using user-configured endpoints.

Mitigation: Review and approve the exact endpoint, retention policy, and data-handling terms before sending confidential code, private documents, personal data, or embedded secrets.

Risk: The technical library template discusses API key placement in package Markdown.

Mitigation: Use environment variables or a secret manager for live API keys, and do not store live secrets in tech-library.md inside the skill package.

Risk: Generated or iterated skills may include incorrect, misleading, or unsafe instructions.

Mitigation: Review, test, and scan generated skills before deployment.

## Reference(s):

- [Skill Factory on ClawHub](https://clawhub.ai/mwangxiang/skills/wx-skill-factory)
- [Call Guide Template](artifact/call-guide.md)
- [Technical Library Template](artifact/tech-library.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured reports, tables, templates, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce skill drafts, design documents, test reports, comparison reports, iteration records, delivery reports, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
