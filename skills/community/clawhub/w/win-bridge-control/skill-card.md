## Description:

Bridge: Cross-OS UI automation for Windows Host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2059247714](https://clawhub.ai/user/2059247714)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill from WSL2 to control a Windows host desktop for tasks such as clicking buttons, taking screenshots, and moving the cursor. Use it only in a controlled Windows session where host UI automation is intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a Windows desktop from WSL2 through broad host-side shell execution.

Mitigation: Install only when Windows host UI control is intentional; require explicit confirmation before each host action and use a constrained Windows account or session with sensitive applications closed.

Risk: Weak prompt handling and a mutable npm dependency can lead to unintended or changed host actions.

Mitigation: Prefer an exact reviewed package version and a non-shell wrapper or broker that validates prompts and limits allowed actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Linux WSL2 environment with Windows cmd.exe and Node available.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
