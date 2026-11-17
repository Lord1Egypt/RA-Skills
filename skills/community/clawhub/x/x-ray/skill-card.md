## Description:

Scans an unfamiliar software project to quickly identify its project type, technology stack, architecture, file structure, complexity, and learning value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppshux](https://clawhub.ai/user/ppshux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use X-ray to inspect unfamiliar codebases through static analysis, understand the project structure and stack, and generate a concise HTML project overview.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped repository-derived content.

Mitigation: Review the generated report before sharing it, avoid scanning sensitive workspaces unless the file inventory is acceptable, and open reports cautiously until escaping or a restrictive Content Security Policy is added.

Risk: Scanning untrusted repositories can expose file inventory and project metadata.

Mitigation: Run the skill only on an intended project path and avoid repositories containing secrets or sensitive source material.

## Reference(s):

- [Analysis Rules](references/analysis-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON scan data, Markdown guidance, shell commands, and an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates xray-data.json and xray-report.html from static repository inspection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
