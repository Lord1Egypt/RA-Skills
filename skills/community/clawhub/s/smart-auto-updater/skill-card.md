## Description:

Smart auto-updater with AI-powered impact assessment that checks updates, analyzes changes, evaluates system impact, and decides whether to auto-update or report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruiwang20010702](https://clawhub.ai/user/ruiwang20010702)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check OpenClaw and ClawHub skill updates, assess architecture, performance, compatibility, and security impact, and choose whether to apply low-risk updates or produce reports for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduled updates can change OpenClaw or installed skills without sufficient approval or recovery planning.

Mitigation: Use report-only mode unless automatic updates are deliberately approved, add an approval and rollback process, and document how to remove any cron jobs the skill creates.

Risk: Medium-risk updates or source changes may be applied too broadly if thresholds are configured aggressively.

Mitigation: Avoid MEDIUM auto-update, keep conservative thresholds for production environments, verify update sources, and manually review changelogs before applying non-low-risk updates.

Risk: LLM-based impact assessment can misclassify architecture, performance, compatibility, or security impact.

Mitigation: Treat generated risk reports as decision support, test updates in staging, and require human review for breaking changes, migrations, security-sensitive updates, or unclear changelog entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ruiwang20010702/skills/smart-auto-updater)
- [Risk Assessment Methodology](references/risk-assessment.md)
- [Report Templates](references/report-templates.md)
- [Integration Guide](references/integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report detail can be brief, detailed, or full; update behavior is controlled by environment variables such as SMART_UPDATER_AUTO_UPDATE and SMART_UPDATER_RISK_TOLERANCE.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json, released 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
