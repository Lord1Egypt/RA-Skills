## Description:

Guides agents in writing Rez package commands() sections using the rex environment API, string expansion, execution order, and build-time branching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to draft and review Rez package environment configuration, including path changes, shell aliases, and build-specific behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated package commands can alter the Rez shell environment through sourced scripts, aliases, unset variables, or PATH and PYTHONPATH changes.

Mitigation: Review generated commands and environment changes before using them in a Rez package.

## Reference(s):

- [rez-package-commands on ClawHub](https://clawhub.ai/loonghao/skills/rez-package-commands)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for Rez package commands() and the rex environment API.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
