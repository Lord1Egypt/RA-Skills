## Description:

Fix robotic QQ Bot replies by replacing default prompts with your own personality, using SOUL.md files for character-driven AI responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QQ bot operators use this skill to replace default, formal QQ bot system prompts with custom personality prompts. It is intended for bots that should sound less robotic in group chats or character-driven deployments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally changes a QQ bot's persistent system prompt, which can alter user-facing behavior broadly.

Mitigation: Review the SOUL.md content before applying it, preview the resulting prompt, and keep a rollback path for restoring the prior prompt.

Risk: The suggested persona pattern may deny chatbot or AI-assistant identity, which can create disclosure and trust concerns.

Mitigation: Avoid profiles that deny required AI disclosure, and adapt the persona rules to preserve any disclosure required by the deployment context.

Risk: Prompt profiles can introduce unrelated tool or data instructions that exceed the intended bot-personality scope.

Mitigation: Limit SOUL.md content to persona and communication rules, and remove unrelated tool, data-access, or operational instructions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/qqbot-prompt-optimizer)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with a SOUL.md template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompt-configuration guidance; no executable code is included in the artifact.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
