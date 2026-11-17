## Description:

Scans an unfamiliar software project to identify its project type, technology stack, architecture, file structure, complexity, and learning value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongxiupiaoxiang](https://clawhub.ai/user/hongxiupiaoxiang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use Q-ray to quickly understand, explore, evaluate, or take over an unfamiliar codebase. It performs static repository analysis and produces a local visual project overview report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enumerates repository file paths and summarizes project structure, which may expose sensitive filenames or private project details if run on the wrong folder.

Mitigation: Run it only against the intended project directory and avoid folders containing sensitive material that should not be summarized.

Risk: The generated overview is based on static analysis and may be incomplete or misleading for complex projects.

Mitigation: Review the generated report against the source files before using it for onboarding, handoff, or technical decisions.

## Reference(s):

- [Q-ray analysis rules](references/analysis-rules.md)
- [ClawHub skill page](https://clawhub.ai/hongxiupiaoxiang/skills/q-ray)

## Skill Output:

**Output Type(s):** [text, html, json, shell commands, guidance]

**Output Format:** [HTML report with supporting JSON scan data and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local generated files such as qray-data.json and qray-report.html.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
