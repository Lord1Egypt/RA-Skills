## Description:

Validate, lint, diff, and inspect TOML configuration files, including pyproject.toml, Cargo.toml, and other TOML configs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate TOML syntax, run lint checks, inspect configuration structure, extract keys, and compare TOML files before changing or sharing project configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Show and diff operations can print TOML configuration contents, including sensitive values if present.

Mitigation: Use the skill only on files intended for inspection and review outputs before sharing them.

Risk: Python versions before 3.11 require installing the optional TOML parser dependency.

Mitigation: Prefer Python 3.11 or newer so TOML parsing uses the standard-library parser.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/toml-validator)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; script results can be text, JSON, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local TOML files selected by the user; show and diff operations can print configuration values.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
