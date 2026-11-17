## Description:

抓取 Solidot 热门和最新文章，推送到飞书。

This skill is ready for commercial/non-commercial use.

## Publisher:

[n0nsense11](https://clawhub.ai/user/n0nsense11)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect current Solidot article links and publish a concise daily news digest to Feishu or a local Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Feishu document token can be exposed to local process listings when passed to the Feishu write command.

Mitigation: Use a narrowly scoped Feishu document token, run only in trusted environments, and rotate the token if exposure is suspected.

Risk: The skill can write generated content to a Feishu document or to the local workspace.

Mitigation: Confirm the intended document token and workspace path before execution, and review the generated digest before sharing it broadly.

Risk: The optional cron setup creates recurring daily writes.

Mitigation: Add the cron job only when recurring daily publication is desired and remove or disable it when the workflow is no longer needed.

## Reference(s):

- [Solidot](https://www.solidot.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown document with terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 15 Solidot article links and writes to Feishu when FEISHU_DOC_TOKEN is configured; otherwise writes solidot-push.md in the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
