## Description:

Guides development agents through an operator-reviewed handoff for Docker operations that cannot run inside their sandbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsmartinez99](https://clawhub.ai/user/jsmartinez99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when a sandboxed agent needs a Docker operation on the host. It guides preparation of Docker commands, operator review and execution, result checking, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker commands handed off for host execution can affect host resources or bypass sandbox isolation.

Mitigation: Require explicit operator approval for each command file; reject privileged, host-mounted, or Docker-socket-mounted runs unless separately justified.

Risk: Unpinned images can change between review and execution.

Mitigation: Prefer pinned image digests and check the recorded output and cleanup after each run.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown instructions with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host commands require operator review before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
