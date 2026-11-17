## Description:

CLI tool for analyzing, optimizing, and formatting resumes to improve ATS scoring via keyword matching and structured templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, resume reviewers, and developers use this CLI to inspect resumes, compare them with job descriptions, and prepare ATS-oriented formatting and keyword guidance workflows. In this release, many advertised analysis and generation functions are scaffolded rather than fully implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works with resumes and job descriptions, which can contain sensitive personal data.

Mitigation: Review the configured DB_PATH before use, keep local storage private, and avoid placing secrets in .env beyond required API keys.

Risk: Several advertised analysis, scoring, keyword, and generation functions are placeholders in this release.

Mitigation: Validate behavior with representative files before relying on parsing, scoring, keyword extraction, or generated resume output.

Risk: Installation instructions include a pipx package command that may not correspond to the reviewed artifact source.

Mitigation: Prefer a local editable install from the reviewed source when evaluating or deploying this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/resume-ats)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI operations; resume and job description inputs may be sensitive personal data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
