## Description:

Skill Dependency Resolver scans skills for Python requirements.txt files, detects version conflicts, and generates a merged requirements file with an analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and system administrators use this skill to inspect Python dependency requirements across multiple installed skills, identify conflicts, and produce a consolidated requirements file for review before installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated merged requirements file may change package versions used by other skills.

Mitigation: Review generated package version changes before installing them, especially for production or security-sensitive skills.

Risk: Installation creates a CLI symlink in ~/.local/bin.

Mitigation: Install only in environments where adding this local command is acceptable, and remove the symlink when uninstalling.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/utopiabenben/skills/skill-dependency-resolver)
- [Publisher profile](https://clawhub.ai/user/utopiabenben)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Plain-text requirements file plus CLI summary and dependency analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated requirements-merged.txt should be reviewed before package installation.]

## Skill Version(s):

0.1.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
