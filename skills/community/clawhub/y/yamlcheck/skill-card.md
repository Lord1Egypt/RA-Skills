## Description:

Validate YAML syntax using python3, lint configs, and convert YAML to JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate YAML files, lint common formatting issues, inspect top-level keys, and convert YAML documents to JSON during local configuration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests installing PyYAML with an unpinned pip command, which can introduce dependency supply-chain or version drift risk.

Mitigation: Install PyYAML from a trusted package source and pin the dependency version in the project or execution environment.

Risk: Validation, key previews, and conversion output may display sensitive values from local YAML configuration files.

Mitigation: Review files before running previews on secrets-bearing configurations and avoid sharing terminal output from sensitive YAML files.

## Reference(s):

- [Yamlcheck on ClawHub](https://clawhub.ai/bytesagain-lab/skills/yamlcheck)
- [bytesagain-lab publisher profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON when converting YAML input with the to-json command.]

## Skill Version(s):

3.0.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
