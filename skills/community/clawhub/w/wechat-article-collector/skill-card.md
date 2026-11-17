## Description:

Collects WeChat Official Account articles through Browser Harness from a logged-in browser session, deduplicates them, downloads full text, and saves local Markdown copies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adchina2025](https://clawhub.ai/user/adchina2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to archive authorized WeChat Official Account articles or configured article pages into a local knowledge base as Markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape authenticated or custom websites beyond the stated WeChat backup workflow.

Mitigation: Use it only with accounts and websites you are authorized to archive, and avoid custom or login-required targets unless permissions and retention rules are clear.

Risk: The security evidence reports command-injection exposure in URL handling and filename-sanitization concerns.

Mitigation: Fix those issues before running the skill on untrusted input, and review the generated file paths before scheduling unattended runs.

Risk: Unattended collection can retain local copies of sensitive article content.

Mitigation: Define storage location, access control, and retention expectations before enabling scheduled collection.

## Reference(s):

- [Browser Harness](https://github.com/browser-use/browser-harness)
- [WeChat Official Account Platform](https://mp.weixin.qq.com)
- [ClawHub Skill Page](https://clawhub.ai/adchina2025/skills/wechat-article-collector)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, JSON article lists, configuration JSON, and terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves one Markdown file per article in the configured local directory and may write an intermediate article list to /tmp/all_articles.json.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
