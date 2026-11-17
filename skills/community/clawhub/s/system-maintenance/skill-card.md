## Description:

Complete maintenance system for OpenClaw with unified architecture, filesystem governance, and cross-platform design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to monitor system health, schedule maintenance, clean logs and temporary files, and generate maintenance reports. Review the release before enabling scheduled execution or cleanup behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can introduce persistent scheduled execution through cron-based maintenance tasks.

Mitigation: Do not run one-click setup or install-cron commands until scheduled targets are audited, persistence is explicitly approved, and an uninstall path is documented.

Risk: Cleanup behavior may affect broad filesystem locations without enough release-level scoping or safety controls.

Mitigation: Prefer dry-run cleanup, explicit confirmation, and reviewed path allowlists before deleting logs or temporary files.

Risk: The artifact references maintenance scripts that are not included in the packaged files.

Mitigation: Install only after the missing scripts are supplied, scanned, and matched to the documented commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jazzqi/skills/system-maintenance)
- [OpenClaw System Maintenance Homepage](https://github.com/jazzqi/openclaw-system-maintenance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe scheduled maintenance, cleanup, monitoring, and reporting actions for OpenClaw systems.]

## Skill Version(s):

1.3.2 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
