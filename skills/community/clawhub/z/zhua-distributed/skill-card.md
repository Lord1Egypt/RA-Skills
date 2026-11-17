## Description:

Zhua Distributed describes a distributed Zhua deployment pattern and includes helper scripts for initializing a master instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beipian261](https://clawhub.ai/user/beipian261)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan distributed Zhua deployments across master, compute, and storage node roles and to initialize a local master configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is incomplete for its promised distributed memory, synchronization, load balancing, and failover behavior.

Mitigation: Review implementation status before deployment and do not rely on it for real cross-device state or task synchronization until those mechanisms are documented and implemented.

Risk: The master initialization script writes a configuration file under the user's home directory using the supplied instance name.

Mitigation: Use a simple safe instance name such as zhua-master, avoid slashes or dot-dot path segments, and evaluate the script in an isolated environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
