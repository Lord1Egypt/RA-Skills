## Description:

闲鱼数据抓取 uses Playwright and OCR to collect Xianyu product data, generate JSON and Markdown reports, and optionally upload screenshots and data to a Gitee repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beipian261](https://clawhub.ai/user/beipian261)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill for Xianyu market research, competitor analysis, keyword-based product collection, OCR extraction from screenshots, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe installation paths may run remote or privileged setup steps before review.

Mitigation: Avoid curl-piped installation and sudo flows; inspect the installer locally and install dependencies through trusted package managers.

Risk: Cron scheduling and self-update behavior can create persistence or change code after initial review.

Mitigation: Disable or remove cron and self-update unless the code source and update channel are verified.

Risk: Gitee tokens and Xianyu cookies are sensitive credentials used by the skill.

Mitigation: Use narrowly scoped credentials, store them privately, rotate them regularly, and remove them before sharing logs or configuration.

Risk: Screenshots and scraped data may be uploaded to a remote repository.

Mitigation: Use a private upload destination and inspect generated screenshots, JSON files, and reports before pushing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beipian261/skills/xianyu-data-grabber)
- [ClawHub publisher profile](https://clawhub.ai/user/beipian261)
- [Gitee](https://gitee.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, JSON data files, Markdown reports, and screenshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local screenshots, data files, analysis reports, logs, cron entries, and optional Gitee uploads.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
