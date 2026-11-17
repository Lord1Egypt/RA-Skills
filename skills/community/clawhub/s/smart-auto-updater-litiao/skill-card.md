## Description:

Smart auto-updater that checks OpenClaw and skill updates, analyzes changelogs and diffs with an LLM, assesses impact, and either auto-updates low-risk changes or reports higher-risk updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw and ClawHub skill updates, assess update risk, apply low-risk updates, and receive reports or recommendations for changes that need review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify OpenClaw and installed skills.

Mitigation: Start in report-only mode and manually review changelogs before enabling automatic updates.

Risk: Automatic MEDIUM-risk updates may apply changes before a human reviews compatibility or operational impact.

Mitigation: Keep automatic updates limited to LOW risk unless the environment explicitly accepts MEDIUM-risk unattended changes.

Risk: Scheduled checks can create recurring unattended update behavior.

Mitigation: Add cron jobs only after validating the configuration, timezone, delivery channel, and rollback process.

Risk: Webhook notifications can expose operational update details to external endpoints.

Mitigation: Use only approved webhook endpoints and avoid sending reports to untrusted channels.

## Reference(s):

- [Risk Assessment Methodology](artifact/references/risk-assessment.md)
- [Report Templates](artifact/references/report-templates.md)
- [Integration Guide](artifact/references/integration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include risk classifications, update decisions, operational summaries, and recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
