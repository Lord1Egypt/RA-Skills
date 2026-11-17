## Description:

Inventories and classifies installed OpenClaw skills, generates Markdown, JSON, or HTML reports, and offers optional sharing and skill enablement controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuntao2011](https://clawhub.ai/user/kuntao2011)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and administrators use this skill to audit installed skills, identify duplicates and missing dependencies, and create inventory reports. They can optionally share a report or enable and disable selected skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sharing an inventory may expose skill names, descriptions, sources, and usage data to Feishu or Notion.

Mitigation: Avoid --push in sensitive environments; review the report and intended destination before opting in.

Risk: Enabling or disabling skills changes local OpenClaw configuration.

Mitigation: Review --enable and --disable targets before running them, and retain the automatic configuration backup.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kuntao2011/skills/skill-classifier)

## Skill Output:

**Output Type(s):** [Markdown, JSON, HTML, Shell commands, Guidance]

**Output Format:** [Chinese-language guidance and Markdown, JSON, or static HTML inventory reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes classification and status summaries; optional usage, dependency, and change reports.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
