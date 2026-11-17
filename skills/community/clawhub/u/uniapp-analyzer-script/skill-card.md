## Description:

Analyzes uni-app and Vue projects to quantify technical debt, detect code issues, and generate project analysis documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[include5943](https://clawhub.ai/user/include5943)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze uni-app and Vue codebases, preview selected files, run local code-quality checks, and produce project documentation for review or refactoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local repository files may be copied and analyzed with under-scoped exclusion handling.

Mitigation: Run the analyzer in a sandbox or clean workspace, use preview mode to inspect selected files, and avoid repositories containing secrets until exclusion handling is fixed.

Risk: The skill may prompt users to install the skill-seekers dependency from pip.

Mitigation: Inspect the dependency before use and install it in a dedicated virtual environment rather than a shared system Python environment.

## Reference(s):

- [API Reference](references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/include5943/skills/uniapp-analyzer-script)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON analysis files, shell command guidance, and generated reference files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes analysis outputs under analysis-output/{project-name}; preview and deep-analysis modes affect file selection and metadata extraction.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
