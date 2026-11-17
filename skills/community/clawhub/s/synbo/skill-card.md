## Description:

Bayesian optimization for chemical reactions using the synbo package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boeingart](https://clawhub.ai/user/boeingart)

### License/Terms of Use:

MIT-0

## Use Case:

Chemistry researchers and reaction engineers use this skill to prepare reaction spaces, generate descriptors, initialize Bayesian optimization campaigns, and recommend follow-up experimental conditions from prior reaction results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation steps rely on mutable external installers and packages.

Mitigation: Use pinned and verified installers and package versions, and avoid running installation commands from an elevated shell.

Risk: The workflow writes configuration, descriptor, reaction-space, and result files under user-selected project paths.

Mitigation: Confirm exact paths before execution and review generated files before overwriting proprietary reaction data.

Risk: Recommended experiment conditions can be misleading if reaction spaces, descriptors, metrics, or prior results are incomplete or incorrect.

Mitigation: Verify all prerequisites and input data before running initialization or optimization and review recommendations before laboratory use.

## Reference(s):

- [SynBO ClawHub skill page](https://clawhub.ai/boeingart/skills/synbo)
- [Condition descriptors](reference/get_desc.md)
- [Initialization workflow](reference/initialize.md)
- [Optimization workflow](reference/optimize.md)
- [Installation guide](reference/installation.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with Python and shell commands; scripts produce CSV and Excel files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommended reaction conditions, descriptors, and optimization results are written under the configured project directory.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
