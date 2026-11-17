## Description:

Grow firmware on any hardware through HTTP: upload C, compile on device, and apply with watchdog rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awis13](https://clawhub.ai/user/awis13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to a seed node, inspect hardware capabilities, upload C firmware, compile it on the device, and apply updates with rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-managed firmware upload, build, and apply actions can change code running on a remote device.

Mitigation: Require explicit user approval before firmware upload, build, or apply actions, and review proposed source changes before execution.

Risk: Connection details include an admin bearer token and examples use plaintext HTTP.

Mitigation: Treat the token as an admin credential, avoid exposing the service over plaintext HTTP, and run the node only on an isolated host or private network.

Risk: Compiling source fetched during setup can introduce remote-code risk.

Mitigation: Review and pin the seed source before compiling, and run the service as an unprivileged user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awis13/skills/seed)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, HTTP API examples, and C code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for node setup, authenticated HTTP requests, firmware editing, build checks, and apply workflows.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
