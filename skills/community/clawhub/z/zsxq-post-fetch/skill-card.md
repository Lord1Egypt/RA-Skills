## Description:

知识星球帖子抓取助手 — 默认通过官方 zsxq-cli OAuth/Keychain 登录态抓取用户已授权账号可访问的帖子，支持全部/精华筛选、关键词搜索、单帖详情、日期范围导出、多星球配置、Markdown 和附件整理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wufulin](https://clawhub.ai/user/wufulin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to fetch, search, summarize, and export Knowledge Planet content that their authorized account can access. It supports group lists, topic lists, digest filtering, single-topic detail, date ranges, Markdown export, and optional attachment organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling risks exist when the legacy ZSXQ_TOKEN fallback is enabled or left in the environment.

Mitigation: Use the default zsxq-cli OAuth login flow for normal use, and unset ZSXQ_TOKEN unless the user deliberately chooses the legacy HTTP fallback.

Risk: Automatic attachment downloads may expose credential material if auth headers are sent to non-ZSXQ hosts or redirects.

Mitigation: Consider disabling automatic attachment downloads in config.json until the downloader strips auth headers from non-ZSXQ hosts and redirects.

Risk: The installer may install the current global zsxq-cli npm package without a pinned version.

Mitigation: Install only when the publisher and npm package are trusted, and avoid running the installer with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wufulin/skills/zsxq-post-fetch)
- [API Reference](references/api-reference.md)
- [Architecture](docs/architecture.md)
- [Official zsxq-cli dependency](https://github.com/unnoo/zsxq-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance]

**Output Format:** [Chinese natural-language summaries, JSON command output, Markdown exports, local attachment files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Markdown and attachments are saved under the configured attachment directory by group and date when export or download options are enabled.]

## Skill Version(s):

1.2.0 (source: evidence.json release.version and artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
