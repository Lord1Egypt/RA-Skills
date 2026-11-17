## Description:

Venus Tracker helps agents synchronize Feishu Bitable project data and produce morning and evening progress tracking for the Venus kindergarten ERP project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project operators use this skill within the venus-project-pm workflow to initialize, migrate, synchronize, and report on Feishu Bitable project tracking tables for the Venus ERP release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates data-changing Feishu project-record operations to a local synchronization script that is not included in the artifact.

Mitigation: Review the referenced synchronization script before running commands, and confirm the intended Feishu Base and credentials.

Risk: Unreviewed installation paths could run code outside the validated ClawHub release.

Mitigation: Prefer the reviewed ClawHub install path over the unpinned git clone path unless the source has been reviewed separately.

## Reference(s):

- [Project homepage](https://github.com/spikesubingrui-design/venus-tracker)
- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/skills/venus-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and operational status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify blockers, affected modules, launch phase, next milestone, and schedule or submission risks when present.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
