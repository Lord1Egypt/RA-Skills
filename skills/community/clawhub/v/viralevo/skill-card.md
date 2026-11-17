## Description:

Self-evolving viral content trend advisor. Monitors 11 platforms, predicts what to post and when, and improves its own accuracy every week automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xf69](https://clawhub.ai/user/0xf69)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and operators use this skill to monitor public trend signals, choose content topics and posting windows, and refine future recommendations from logged post performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tavily API key and makes outbound requests for public trend discovery.

Mitigation: Use a scoped Tavily key where possible and avoid placing personal or sensitive data in monitored search terms.

Risk: Scheduled OpenClaw jobs may run collection, verification, and weekly review actions automatically.

Mitigation: Review cron entries before enabling them and start with manual runs until the generated reports and stored data match expectations.

Risk: Local profile, report, log, and database files may be deleted by the optional uninstall cleanup command.

Mitigation: Back up the Viralevo workspace before running destructive cleanup commands.

Risk: The inspected artifact is documentation-only and references implementation scripts that were not present for inspection.

Mitigation: Verify the installed package contents before relying on collection, scoring, reporting, or self-evolution behavior.

Risk: Trend scores and posting windows are probabilistic and may not predict actual business outcomes.

Mitigation: Use recommendations as decision support and compare them against platform analytics and human editorial judgment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xf69/skills/viralevo)
- [Publisher Profile](https://clawhub.ai/user/0xf69)
- [OpenClaw Cron Jobs Documentation](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, shell commands, JSON configuration snippets, and natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local reports, profile data, SQLite trend data, logs, and OpenClaw cron configuration when the referenced scripts are available.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 0.6.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
