## Description:

Advises on Termux/Android command compatibility and safety, using a dry-run validator that classifies commands without executing them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers using Termux on Android can check tool availability and command risk before deciding whether to run a command themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dry-run command classifier may miss unsafe behavior or compatibility issues.

Mitigation: Treat its classifications as guidance, not a security sandbox; review each command and verify the environment before running it manually.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pmuhammadagus-byte/skills/termux-compat-runner)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text with command classifications and suggested manual verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory only; does not execute proposed commands.]

## Skill Version(s):

2.0.0 (source: server release, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
