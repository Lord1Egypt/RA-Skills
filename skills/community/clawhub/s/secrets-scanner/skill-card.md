## Description:

Detect hardcoded secrets, exposed API keys, and credential misconfigurations in IaC and config files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to review user-provided IaC, configuration files, and exported AWS environment-variable metadata for hardcoded secrets and credential exposure. It returns prioritized findings and remediation guidance without requiring direct AWS account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented Lambda environment command can expose environment variable values while the skill asks for names only.

Mitigation: Provide only redacted environment variable names, avoid pasting raw Lambda get-function-configuration output, and rotate any secret values already shared through this workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anmolnagpal/skills/secrets-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration guidance]

**Output Format:** [Markdown with findings tables, remediation steps, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not output raw secret values; findings should identify locations and recommended next steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
