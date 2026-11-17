## Description:

Perform unit conversions and calculations using GNU Units.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asleep123](https://clawhub.ai/user/asleep123)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to produce GNU Units command-line conversions, calculation examples, definition lookups, and guidance for safer unit expressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GNU Units definitions file may contain outdated currency exchange rates.

Mitigation: Avoid relying on this skill for current exchange-rate decisions; use a current financial data source for currency conversion.

Risk: Unquoted unit expressions can be misread by the shell before reaching GNU Units.

Mitigation: Quote unit expressions in generated shell commands, as shown in the skill examples.

Risk: The required `units` binary could vary by package source or installation.

Mitigation: Install GNU Units from a trusted package source before using generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asleep123/skills/units)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GNU Units `units` binary for command execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
