## Description:

社交媒体舆情分析工具 - 品牌方/电商卖家/运营人员的平价舆情监控助手，支持关键词监测、负面预警、声量趋势分析

This skill is ready for commercial/non-commercial use.

## Publisher:

[crystaria](https://clawhub.ai/user/crystaria)

### License/Terms of Use:

MIT-0

## Use Case:

Brand teams, ecommerce sellers, and operations staff use this skill to monitor local CSV exports for keyword matches, sentiment alerts, volume trends, and weekly social media monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores monitored keywords, alert settings, and generated reports inside its local skill directory.

Mitigation: Use non-sensitive input where possible, control access to the skill directory, and review generated report files before sharing.

Risk: Dependency provenance should be reviewed before installation, especially because the security guidance calls out dependency source review.

Mitigation: Install with the committed lockfile, consider regenerating dependencies from the official npm registry, and review dependency updates before use.

Risk: The documented sentiment analysis is dictionary-based and intended for quick screening, so alerts and classifications may be inaccurate.

Mitigation: Treat sentiment output as triage guidance and manually review important negative-alert or business-decision cases.

Risk: The package and server evidence show a naming mismatch between Social Media Monitor and the internal MCP server name.

Mitigation: Confirm the installed package and MCP tool registration match the intended Social Media Monitor release before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crystaria/skills/social-media-monitor)
- [Skill Documentation](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON text responses and generated Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local keyword lists, alert-threshold configuration, sentiment and trend summaries, and Markdown weekly reports in the skill directory.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
