## Description:

Guides users through creating an OpenClaw Agent, running a creation script, and optionally pairing a Feishu bot with supplied credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snlcc](https://clawhub.ai/user/snlcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to collect agent details, create a standardized OpenClaw agent workspace, register it in openclaw.json, and optionally pair a Feishu bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write persistent workspace instructions and update openclaw.json.

Mitigation: Review generated workspace templates and configuration changes before installation or execution.

Risk: Feishu AppSecrets may be passed on the command line and saved as plaintext configuration.

Mitigation: Avoid passing real secrets on the command line when possible, treat saved credentials as sensitive plaintext, and rotate or remove them if exposed.

Risk: Generated proactive monitoring and commit or push instructions may create behavior broader than intended.

Mitigation: Remove or narrow those instructions unless that behavior is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snlcc/skills/x-creat-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/snlcc)
- [Feishu agent creation](https://open.feishu.cn/page/launcher?from=backend_oneclick)
- [Feishu bot creation](https://open.feishu.cn/page/openclaw?form=multiAgent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide execution of a Python script that creates workspace files and updates OpenClaw configuration.]

## Skill Version(s):

1.2.14 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
