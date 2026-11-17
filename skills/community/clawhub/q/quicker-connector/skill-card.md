## Description:

Integrates with Quicker to read, search, match, execute, and maintain actions and settings, and to generate importable launch-action JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awamwang](https://clawhub.ai/user/awamwang)

### License/Terms of Use:

MIT

## Use Case:

Windows users and developers use this skill to find and run Quicker actions, inspect or update Quicker configuration, and prepare importable launch actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actions may run without meaningful confirmation or execute code unexpectedly.

Mitigation: Use a corrected release that requires an explicit action choice; increasing the matching threshold alone does not address the confirmation bypass.

Risk: Remote-access credentials may be stored insecurely.

Mitigation: Leave optional cloud credentials unset unless needed, and protect configuration files and Quicker backups.

Risk: Broad permissions may increase the impact of unintended actions.

Mitigation: Avoid the blanket permissions command and grant only the access needed for the requested task.

## Reference(s):

- [Quicker user manual: maintenance tools](https://getquicker.net/KC/Manual/Doc/settings-BasicToolsSettingPage)
- [Quicker website](https://getquicker.net/)
- [Quicker Connector on ClawHub](https://clawhub.ai/awamwang/skills/quicker-connector)

## Skill Output:

**Output Type(s):** [Guidance, Code, JSON, Configuration files, Shell commands]

**Output Format:** [Markdown, JSON, Python or PowerShell code, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-specific; may create local exports and importable Quicker action files.]

## Skill Version(s):

1.6.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
