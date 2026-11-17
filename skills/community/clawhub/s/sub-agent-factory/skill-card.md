## Description:

Rapidly spawn and configure specialized sub-agents using templates for research, coding, and analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to provision specialized sub-agent workspaces and generate starter SKILL.md instructions for delegated coding, research, or analysis tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe agent names can cause the provisioning script to write outside the intended agents directory.

Mitigation: Run the script only with trusted, simple agent names until path validation confines output to the agents directory.

Risk: Unsafe role text can be injected into generated agent instructions.

Mitigation: Use trusted, single-line role descriptions until generated YAML and instruction text are escaped or validated.

Risk: Repeated runs may overwrite an existing generated SKILL.md.

Mitigation: Check the target agent directory before provisioning until the script refuses accidental overwrites.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and generated SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local agent folders and inbox/outbox/workspace directories when its provisioning script is run.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
