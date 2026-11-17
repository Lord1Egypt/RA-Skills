## Description:

Validate Stylelint config files for errors, deprecated rules, config structure, plugins, extends, and overrides, outputting text or JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to check Stylelint configuration files for structure errors, deprecated Stylelint 16 rules, plugin and extends issues, override problems, and CI-friendly failure conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads the local Stylelint config path supplied by the user.

Mitigation: Run it only on intended Stylelint configuration files and review file paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/stylelint-config-validator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text, JSON, or one-line summary from a local CLI validator, with Markdown command guidance for agents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes: 0 for no errors, 1 for validation errors or strict-mode issues, and 2 for missing files or parse errors.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
