## Description:

Security-first skill vetting for AI agents that checks skill sources, permissions, suspicious patterns, and high-risk installation behavior before use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaszj](https://clawhub.ai/user/atlaszj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review third-party or unknown skills before installation, classify risk, and produce a concise vetting report with permissions, red flags, and install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims scanner and install-hook behavior, but the core scanner file is missing from the artifact.

Mitigation: Review the package carefully before relying on it as an installation gate, and verify the scanner file and hook behavior from trusted source materials.

Risk: The documented install hook can block installs and delete downloaded files.

Mitigation: Do not enable hook behavior until deletion, logging, execution, and failure paths are confirmed in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atlaszj/skills/skill-vetter-hermes)
- [Publisher Profile](https://clawhub.ai/user/atlaszj)
- [Skill Definition](artifact/SKILL.md)
- [Integration Report](artifact/INTEGRATION_REPORT.md)
- [Publish Guide](artifact/PUBLISH_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with checklists, tables, and inline shell or PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces risk classifications, red-flag summaries, permission notes, and install/block recommendations.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
