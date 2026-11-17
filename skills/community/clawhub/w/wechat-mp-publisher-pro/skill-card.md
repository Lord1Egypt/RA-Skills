## Description:

Automates WeChat Official Account operations across data collection, topic planning, article drafting, image and layout preparation, account metadata, publishing support, and post-publication review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luemery](https://clawhub.ai/user/luemery)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and creators use this skill to plan, draft, format, and prepare WeChat Official Account posts with data-backed topic selection, visual guidance, publishing checklists, and performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML previews may preserve unsafe Markdown HTML or image attributes when drafts come from untrusted sources.

Mitigation: Review and sanitize generated previews before opening them, and avoid using downloaded or untrusted Markdown until preview escaping is fixed.

Risk: Topic keywords, competitor names, and search queries may be sent to Sogou WeChat and saved in local collection outputs.

Mitigation: Avoid sensitive terms in collection runs and review workspace/wechat_data outputs before sharing or retaining them.

Risk: Account configuration files can accumulate sensitive account details if users store secrets in them.

Mitigation: Keep secrets out of the WeChat configuration template and review saved config files before committing or sharing them.

## Reference(s):

- [Content Style Reference](references/content-style.md)
- [Design Guide](references/design-guide.md)
- [Article Template](assets/article_template.md)
- [Publish Checklist](assets/publish_checklist.md)
- [Sogou WeChat Search](https://weixin.sogou.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, HTML previews, JSON/CSV data files, configuration templates, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local files under workspace/wechat_data and workspace/wechat_output when scripts are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
