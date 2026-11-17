## Description:

一款通过自然语言交互追踪每日卡路里摄入量的MCP服务器，提供餐食记录、每日总结、周报生成和食物搜索功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the XiaoBenYang calorie-tracking API for meal logging, daily calorie summaries, weekly reports, and food calorie lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the API key in a local plaintext .env file.

Mitigation: Use only an API key suitable for local plaintext storage, avoid shared or committed workspaces, and rotate the key if it is exposed.

Risk: The server security summary reports copy-paste inconsistencies from an unrelated gaokao project, which can make the service identity less clear.

Mitigation: Review the tool names, MCP identifiers, and service documentation before deployment, and ask the publisher to correct the inconsistent references.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-ccxt)
- [XiaoBenYang service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value before API-backed tools can be used.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
