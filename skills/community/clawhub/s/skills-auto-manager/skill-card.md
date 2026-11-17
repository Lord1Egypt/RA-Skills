## Description:

Skills Auto Manager helps agents check installed OpenClaw skills, browse ClawHub recommendations, and manage low-risk skill installs with reports and configurable review rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cooperiano](https://clawhub.ai/user/cooperiano)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to review the health of installed OpenClaw skills, find relevant ClawHub skills, and generate reports or installation recommendations. It can also help configure recurring checks and approval-based skill installation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automatic installation can change the installed skill set with weak approval boundaries.

Mitigation: Disable auto_install_low_risk and recurring cron execution unless the workflow has been reviewed; require manual approval for every install or update.

Risk: Recommended skills may have sensitive permissions, API key requirements, privacy impact, or financial-operation behavior.

Mitigation: Review each candidate skill's publisher, permissions, version, contents, and risk category before allowing installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cooperiano/skills/skills-auto-manager)
- [ClawHub Documentation](https://clawhub.ai/docs)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May schedule recurring OpenClaw checks and modify the installed skill set when auto-install options are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
