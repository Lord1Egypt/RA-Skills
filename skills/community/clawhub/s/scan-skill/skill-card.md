## Description:

Deep security analysis of an individual skill before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsnishi](https://clawhub.ai/user/itsnishi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before installing or accepting a skill to analyze its SKILL.md and supporting files for injection, shell, obfuscation, persistence, and supply-chain risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can read outside the selected skill directory through symlinks.

Mitigation: Run it in a sandbox or on a copy of the target skill with symlinks removed.

Risk: Reports may reproduce unsafe text from hostile skills.

Mitigation: Treat generated reports as untrusted data and review excerpts before reusing them.

Risk: Package-install findings may trigger outbound checks to PyPI or npm.

Mitigation: Run scans only where those network checks are acceptable, or restrict network access when registry verification is not needed.

## Reference(s):

- [Scan Skill on ClawHub](https://clawhub.ai/itsnishi/skills/scan-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with severity-ranked findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes frontmatter analysis and supporting file inventory.]

## Skill Version(s):

1.1.1 (source: server release metadata, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
