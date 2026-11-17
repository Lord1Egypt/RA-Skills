## Description:

公众号内容发布自动化技能。整合用户自有工具，实现内容生成、配图、三步预检、草稿箱发布的全流程自动化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[taoj2025](https://clawhub.ai/user/taoj2025)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators use this skill to generate WeChat public-account article drafts, add images, run publication checks, and prepare draft-box publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publication workflows may proceed before safety checks and human confirmation are reliable.

Mitigation: Require successful prechecks plus an explicit dry-run or confirmation step before connecting real WeChat credentials or publishing drafts.

Risk: Article rewriting and fixed attribution can alter existing content or apply unwanted branding.

Mitigation: Preview diffs, back up articles before modification, and make attribution and publishing labels configurable.

Risk: Scheduled runs can repeatedly execute the workflow with live API or WeChat credentials.

Mitigation: Do not install cron jobs until the workflow has been reviewed with test credentials, scoped permissions, and failure alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taoj2025/skills/wechat-content-pipeline)
- [Publisher profile](https://clawhub.ai/user/taoj2025)
- [Configuration reference](artifact/references/config.md)
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation)
- [Picsum image source](https://picsum.photos/800/600)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, generated image files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat draft preparation workflows with article text, image references, precheck results, and publishing guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
