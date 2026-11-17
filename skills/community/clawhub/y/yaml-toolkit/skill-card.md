## Description:

YAML处理工具 helps agents inspect, validate, parse, transform, and generate YAML content for predictable cross-language and cross-version use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to work with YAML files, including format checks, parsing, conversion, generation, and repair. It is intended for YAML-focused agent workflows rather than human-judgment-heavy decision tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review marked the skill suspicious because it requests read, write, and command execution authority broader than its YAML helper instructions justify.

Mitigation: Review before installation, restrict use to YAML files intended for inspection or modification, and approve only commands directly needed for the task.

Risk: The artifact describes API key configuration and sensitive data handling, so secrets could be exposed if included in YAML files, outputs, or logs.

Mitigation: Use environment variables for secrets, avoid placing credentials in YAML content, and redact generated output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/yaml-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and optional shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before writing files or executing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
