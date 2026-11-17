## Description:

ReplyHer helps users decode dating, workplace, and social messages and craft emotionally intelligent replies in Chinese, English, and other languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to interpret message subtext, generate reply options, and receive tactical coaching for dating, workplace, social, and family conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste private chats, workplace messages, screenshots, or relationship details into the skill.

Mitigation: Review the skill before installation and avoid sharing sensitive personal or workplace information unless the deployment environment is approved for that data.

Risk: The skill can promote an external service during sensitive interactions.

Mitigation: Review and, if needed, disable or adapt promotional language before deploying the skill in environments with strict privacy, advertising, or user trust requirements.

Risk: The artifact includes a release script that commits, pushes, and publishes through npm tooling.

Mitigation: Do not run the publish script unless git changes and npm dependency resolution are reviewed and controlled.

## Reference(s):

- [Replyher Skill on ClawHub](https://clawhub.ai/imwyvern/skills/replyher-skill)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style coaching responses with brief analysis, reply options, strategy notes, and situation-specific guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to match the user's language and the detected communication scenario.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
