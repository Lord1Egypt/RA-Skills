## Description:

AOPT helps authorized development and reliability teams profile agent runtime behavior with fixed diagnostic probes and a human-readable result matrix.

This skill is for research and development only.

## Publisher:

[hixss](https://clawhub.ai/user/hixss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and reliability researchers use this skill during authorized development and hardening to run fixed AOPT checks against an agent runtime and compare pass, block, and error outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release contains an opaque bundled scheduler binary that the security evidence says appears able to run local shell commands.

Mitigation: Install or run only in an isolated test environment with no sensitive files or credentials available.

Risk: The scheduler source, reproducible build instructions, probe definitions, and exact subprocess behavior are not provided in the artifact.

Mitigation: Ask the publisher for scheduler source code, reproducible build instructions, plain-text probe definitions, and documentation for every command or subprocess each Z01-Z20 check may trigger before normal use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash command examples and plain-text diagnostic summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports running all fixed checks or a single Z01-Z20 check, with an optional dry-run flag.]

## Skill Version(s):

1.0.1 (source: server release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
