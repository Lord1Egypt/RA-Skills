## Description:

One-time founder onboarding that generates a personalized manifest, STREAM calibration, development principles, and stack selection for Solo Factory projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fortunto2](https://clawhub.ai/user/fortunto2)

### License/Terms of Use:

MIT

## Use Case:

External developers and solo founders use this skill to initialize reusable Solo Factory defaults and project-level profile files before using related scaffold, validation, setup, and decision-support skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Solograph check can execute or install an unpinned third-party package.

Mitigation: Review and trust the Solograph package source and version before allowing uvx solograph or a Solograph install command to run.

Risk: The skill creates persistent org-level defaults and project-specific .solo files that related skills consume.

Mitigation: Review generated defaults.yaml and .solo files before relying on downstream Solo Factory skills.

## Reference(s):

- [Generation Rules](references/generation-rules.md)
- [AskUserQuestion Specifications](references/questions.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with YAML configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent org defaults under ~/.solo-factory and project-specific .solo profile files.]

## Skill Version(s):

2.1.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
