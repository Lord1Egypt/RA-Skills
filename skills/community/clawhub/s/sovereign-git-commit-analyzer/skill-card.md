## Description:

Analyzes git commit history to report commit frequency, contributor activity, file-change hotspots, and commit-message quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers, team leads, and engineering managers use this skill to analyze repository activity, contributor patterns, and commit quality for development process insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe shell input handling in the analyzer.

Mitigation: Use the skill only on trusted repositories and CI inputs until numeric and branch arguments are validated and report output is escaped.

Risk: Generated reports may expose contributor emails, filenames, commit activity, and commit-message details.

Mitigation: Review reports before publishing or uploading them outside the repository's intended audience.

Risk: The output-file option can overwrite an existing path.

Mitigation: Choose report paths deliberately and avoid pointing output at important existing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-git-commit-analyzer)
- [Publisher profile](https://clawhub.ai/user/ryudi84)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown, JSON, or plain-text git analysis reports, with optional file output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May exit with a nonzero status in CI when the commit-message quality score is below the configured threshold.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill.json, script header, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
