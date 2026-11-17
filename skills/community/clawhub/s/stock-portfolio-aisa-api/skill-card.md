## Description:

Create and manage stock and crypto portfolios with live AISA pricing and profit-and-loss tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, update, list, rename, delete, and review stock or crypto portfolios with live pricing and profit-and-loss summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local portfolio records can be modified or deleted through update, remove, delete, and rename commands.

Mitigation: Review commands before execution and keep backups of the repo-local portfolio JSON state before destructive operations.

Risk: The AISA API key can be sent to an endpoint configured through AISA_BASE_URL.

Mitigation: Use a low-privilege AISA_API_KEY and set AISA_BASE_URL only to trusted endpoints.

Risk: Live price responses may be incomplete or unsuitable as authoritative financial advice.

Mitigation: Treat returned prices and profit-and-loss calculations as informational and verify important financial data with authoritative sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/stock-portfolio-aisa-api)
- [Publisher Profile](https://clawhub.ai/user/aisadocs)
- [AISA API Endpoint](https://api.aisa.one/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, or delete local JSON portfolio state when invoked through the bundled Python client.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
