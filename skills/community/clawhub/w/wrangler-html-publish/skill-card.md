## Description:

仅在用户明确要求 Wrangler 或 Cloudflare Pages 发布 HTML、单页或静态站点时使用，整理文件、部署并验证实际 HTTPS 地址。普通 HTML 生成或泛称生成网页链接不自动触发本技能，避免与默认发布流程重复上传。仅本地时只保存，公开上传须有授权，不处理 OSS 上传或动态后端。

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

开发者可在用户明确要求使用 Wrangler 或 Cloudflare Pages 发布 HTML 或静态站点时，用此技能归档文件、整理经审核的部署快照、执行发布并验证实际页面地址。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloudflare Pages content is normally public, so an unreviewed page or embedded resource could expose private information.

Mitigation: Review the page and its resources for public release, confirm the user's authorization, and check the complete deployment file list before publishing.

Risk: The security verdict is benign with medium confidence, but inspection coverage is incomplete and tool-misuse analysis was degraded.

Mitigation: Review the partially interpreted JavaScript files and required runtime permissions before relying on the skill when stronger assurance is needed.

## Reference(s):

- [Cloudflare Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/)
- [Wrangler HTML Publish on ClawHub](https://clawhub.ai/156554395/skills/wrangler-html-publish)
- [Local configuration and publishing manifest](references/state.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [HTML files, deployment URLs, and concise Markdown status reports with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the source HTML and reports the actual deployment and verification status.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
