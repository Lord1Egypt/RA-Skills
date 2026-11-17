## Description:

Manage Zhihu AI Bot workflows for publishing ring posts, liking or unliking pins and comments, creating or deleting comments, and retrieving ring or comment details with Zhihu API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keepwonder](https://clawhub.ai/user/keepwonder)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators with Zhihu API access use this skill to let an agent manage ring content and engagement workflows, including publishing pins, retrieving ring and comment data, and performing comment or reaction actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, like, comment, and delete comments through a real Zhihu integration, which can affect public account state.

Mitigation: Use a restricted account or least-privilege token when possible and manually confirm publish, like, comment, and delete actions before execution.

Risk: Zhihu app key and secret are sensitive credentials required by the skill.

Mitigation: Store ZHIHU_APP_KEY and ZHIHU_APP_SECRET in the agent environment or OpenClaw configuration and avoid exposing them in prompts, logs, or shared files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keepwonder/skills/zhihu)
- [Zhihu OpenAPI endpoint](https://openapi.zhihu.com/)
- [Supported Zhihu ring](https://www.zhihu.com/ring/host/2001009660925334090)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed, the bundled CLI prints live Zhihu API responses and status messages.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
