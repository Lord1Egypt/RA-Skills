## Description:

连接时间之河（timehe.com）时间胶囊平台，帮助用户创建时间胶囊、每日写作、查看胶囊、参与团队胶囊和使用扫码写信亭。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yigenyecao-afk](https://clawhub.ai/user/yigenyecao-afk)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage Timehe time capsules through an agent, including creating capsules, retrieving writing prompts, submitting entries, viewing capsule status, and contributing to team capsules. It is intended for personal, family, partner, future-self, and team memory workflows connected to the Timehe service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process intimate personal, family, partner, team, or future-self messages.

Mitigation: Confirm user intent before sending sensitive capsule text to Timehe and avoid exposing capsule contents to third parties.

Risk: Authenticated actions may use a Timehe bearer token.

Mitigation: Use only tokens the user is comfortable granting to Timehe-related actions, avoid displaying tokens, and do not ask users to paste tokens unnecessarily.

Risk: Broad trigger wording could activate the skill during emotionally sensitive writing tasks.

Mitigation: Keep responses scoped to the user's requested Timehe action and ask for confirmation before creating capsules or submitting entries.

## Reference(s):

- [Timehe website](https://www.timehe.com)
- [Timehe API base](https://www.timehe.com/api)
- [Timehe booth](https://www.timehe.com/booth)
- [ClawHub skill page](https://clawhub.ai/yigenyecao-afk/skills/timehe)
- [ClawHub publisher profile](https://clawhub.ai/user/yigenyecao-afk)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown responses with inline JSON examples and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the optional TIMEHE_TOKEN environment variable for authenticated Timehe API actions.]

## Skill Version(s):

1.1.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
