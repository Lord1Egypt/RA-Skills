## Description:

每日AI/科技热榜日报。从AIHOT单站读取近3天热榜，生成报告并同步飞书文档，只发链接不发全文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators use this skill to gather recent AI and technology headlines from AIHOT, organize them into a Chinese daily report, archive a local Markdown file, and publish a Feishu document link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create Feishu documents, grant full access to a fixed Feishu account, and send links to a fixed Feishu group.

Mitigation: Confirm the Feishu tenant IDs, account, group, and permission choices match the intended deployment before installation or execution.

Risk: The security evidence reports embedded Feishu application credentials.

Mitigation: Rotate exposed credentials, remove secrets from the skill content, and supply credentials through a managed secret store before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binhuatochina/skills/technews-daily-report)
- [AIHOT daily feed](https://aihot.virxact.com/daily)
- [AIHOT](https://aihot.virxact.com)
- [Feishu document operations reference](references/feishu-doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report, Feishu document link, local file paths, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a dated report file and synchronization record when executed as written.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
