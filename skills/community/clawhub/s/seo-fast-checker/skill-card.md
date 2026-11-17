## Description:

输入网址一键输出SEO诊断报告，检查标题/描述/Headers/关键词密度/图片alt/页面速度/移动端适配/Meta标签，输出可执行优化建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyjaixiao](https://clawhub.ai/user/hyjaixiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and SEO operators use this skill to audit one or more public webpages and receive concise, actionable SEO recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound HTTP requests to user-supplied URLs, and URL fetching is not limited to public sites.

Mitigation: Use the skill only on public pages you control or are allowed to audit; avoid private, staging, intranet, localhost, cloud-metadata, or otherwise sensitive URLs.

Risk: Optional AI mode can send fetched page text and the URL to OpenAI.

Mitigation: Enable --ai only when the page content and URL are acceptable to share with OpenAI, and configure OPENAI_API_KEY deliberately for that mode.

Risk: Dependencies are installed from package names without pinned versions.

Mitigation: Pin and review dependencies before installation in production or commercial environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyjaixiao/skills/seo-fast-checker)
- [Publisher profile](https://clawhub.ai/user/hyjaixiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown SEO diagnostic report, printed to stdout or saved to a Markdown file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional AI-enhanced analysis can be included when OPENAI_API_KEY and the OpenAI Python package are available.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
