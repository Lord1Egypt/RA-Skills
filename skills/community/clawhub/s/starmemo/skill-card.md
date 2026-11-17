## Description:

starmemo is an OpenClaw memory skill that stores structured memories, builds a local knowledge base, recalls relevant history, and can use configured LLM providers for extraction and answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nandujia](https://clawhub.ai/user/nandujia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to save conversation context, search prior memories, manage knowledge entries, and configure optional AI-assisted processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save ordinary conversation text into local memory files.

Mitigation: Use it only in an isolated environment when local conversation retention is acceptable, and avoid entering secrets or regulated data.

Risk: When AI processing is configured, prompts or recalled memories may be sent to external LLM providers.

Mitigation: Leave AI and web features disabled unless needed, and configure only approved providers for the deployment environment.

Risk: API keys provided through command-line configuration can remain in shell history or local configuration.

Mitigation: Prefer nonpersistent credentials, keep key persistence disabled unless required, and rotate any key that may have been exposed through command-line history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nandujia/skills/starmemo)
- [ClawHub publisher profile](https://clawhub.ai/user/nandujia)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Text and Markdown files with command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores daily memories and knowledge entries locally; optional AI processing depends on configured provider credentials.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
