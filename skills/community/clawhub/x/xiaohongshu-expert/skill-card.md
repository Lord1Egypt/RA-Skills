## Description:

Collects and analyzes Xiaohongshu keyword, post, creator profile, engagement, and trend-tracking data, with optional Feishu Bitable export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suzanneyp](https://clawhub.ai/user/suzanneyp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content operations teams use this skill to collect Xiaohongshu topic and creator data, analyze high-performing posts and engagement metrics, and organize results into reports or Feishu Bitable tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scrape and preserve substantial Xiaohongshu post, comment, and creator profile data.

Mitigation: Require explicit confirmation for each collection scope, minimize full-comment and personal/profile field storage, and define retention limits before use.

Risk: The skill can export collected data to Feishu Bitable and recurring notifications.

Mitigation: Confirm each Feishu export and scheduled job, restrict access to exported tables or notification channels, and periodically review active tracking tasks.

Risk: Collection activity may conflict with Xiaohongshu rules or applicable privacy and copyright obligations.

Mitigation: Use only collection scopes that comply with platform rules and applicable obligations, and reduce collection volume when compliance or consent is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suzanneyp/skills/xiaohongshu-expert)
- [Publisher profile](https://clawhub.ai/user/suzanneyp)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, tables, Feishu Bitable field plans, cron expressions, and setup snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preserve substantial collected source text, comments, creator profile fields, and monitoring outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
