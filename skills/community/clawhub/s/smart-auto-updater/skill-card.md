## Description: <br>
Smart auto-updater with AI-powered impact assessment. Checks updates, analyzes changes, evaluates system impact, and decides whether to auto-update or just report. Perfect for hands-off maintenance with safety guarantees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiwang20010702](https://clawhub.ai/user/ruiwang20010702) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to check OpenClaw and skill updates, assess update risk, and decide whether to apply low-risk updates automatically or produce a report for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can schedule unattended OpenClaw and skill updates based on weakly bounded AI risk decisions. <br>
Mitigation: Use report-only or dry-run mode first, avoid scheduled auto-apply in production, and require a rollback plan before enabling automatic updates. <br>
Risk: Update metadata may be sent to third-party webhooks. <br>
Mitigation: Review webhook destinations and report contents before enabling delivery channels. <br>


## Reference(s): <br>
- [Risk Assessment Methodology](references/risk-assessment.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Integration Guide](references/integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk classifications, update decisions, summaries, and upgrade recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
