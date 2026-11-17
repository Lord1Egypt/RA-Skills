## Description:

Calculates a China-specific retirement date and retirement age from a person's role, birth year, and birth month.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acfff](https://clawhub.ai/user/acfff)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate retirement timing under China's gradual retirement policy by supplying a supported role and birth date.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calculator is specific to China's retirement policy and Chinese-only role inputs, so use outside that scope may produce misleading results.

Mitigation: Confirm the user scenario is China-specific and use one of the documented role values before relying on the output.

Risk: Retirement-policy rules may change after the 2024 policy reflected in the artifact.

Mitigation: Review current authoritative policy before using results for planning, legal, or benefits decisions.

Risk: The skill requires uv and may prompt installation through Homebrew before running the local calculation script.

Mitigation: Install uv from a trusted source and review the local script before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acfff/skills/retire-age)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and accepts Chinese role values: 男性, 女职工, 女干部.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
