## Description:

自动抓取 r/wallstreetbets 热股数据，生成每日报告推送到 Discord。使用 ApeWisdom API，支持分片发送避免 Discord 2000 字符限制。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingkko](https://clawhub.ai/user/mingkko)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and operators use this skill to publish scheduled WallStreetBets stock-mention digests to a configured Discord channel. It helps monitor ApeWisdom trend data, including top tickers, rank changes, newcomers, and message chunks sized for Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cron job can automatically post stock-market digests to Discord without an operator reviewing each message.

Mitigation: Confirm the target Discord channel and posting schedule before enabling cron, and test a manual run first.

Risk: The documented install paths and HOME setting assume root-level execution.

Mitigation: Run the skill as an unprivileged user and update OPENCLAW_BIN, SKILL_DIR, HOME, and cron paths for that account.

Risk: Fixed files and directories under /tmp can expose or collide with digest data on shared systems.

Mitigation: Use a private temporary directory with restrictive permissions for logs, raw output, JSON, and chunks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingkko/skills/wsb-digest)
- [Publisher profile](https://clawhub.ai/user/mingkko)
- [Project homepage](https://github.com/mingkko/wsb-digest)
- [Install guide](references/install-guide.md)
- [ApeWisdom WallStreetBets API](https://apewisdom.io/api/v1.0/filter/wallstreetbets)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON payload containing a Markdown digest, with shell-based Discord delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discord delivery is chunked below the 2000 character message limit.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
