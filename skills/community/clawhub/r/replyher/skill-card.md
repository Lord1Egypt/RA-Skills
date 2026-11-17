## Description:

ReplyHer is an AI reply and message coach that decodes messages, reads screenshots, generates copy-ready replies, and helps choose tone for dating, workplace, family, and social conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to interpret chat messages and produce emotionally aware reply options for dating, workplace, family, and social situations. It also supports conversation analysis and tactical communication coaching in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share private or sensitive message content while seeking reply advice.

Mitigation: Redact names, phone numbers, employer details, addresses, screenshots with identifiers, and confidential workplace content before use.

Risk: The skill can append a promotional replyher.com link during sensitive or complex conversations.

Mitigation: Review generated replies before sending them and remove promotional content when it is inappropriate for the conversation.

Risk: The artifact includes a manual publishing script that can commit, push, and publish the skill.

Mitigation: Do not run artifact/publish.sh unless you are the maintainer and have reviewed the working tree, Git remote, and npx package version.

## Reference(s):

- [ReplyHer ClawHub Skill Page](https://clawhub.ai/imwyvern/skills/replyher)
- [Publisher Profile](https://clawhub.ai/user/imwyvern)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ReplyHer](https://replyher.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with concise analysis, copy-ready reply options, and coaching guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in the same language as the user and may include a promotional replyher.com link in complex or multi-turn conversations.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
