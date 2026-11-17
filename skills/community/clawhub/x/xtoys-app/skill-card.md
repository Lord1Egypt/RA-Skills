## Description:

Control xtoys.app devices via webhook for remote intimate device control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasuganosora](https://clawhub.ai/user/kasuganosora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send webhook commands that control configured xtoys.app devices, including selecting supported body-part actions, setting intensity, testing connectivity, listing actions, and stopping current stimulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged stop and pause commands can report success without actually sending a stop request, which is safety-critical for physical device control.

Mitigation: Review carefully before installing, use an independent stop method in xtoys.app or on the device itself, and do not rely on this skill as a safeword mechanism until fixed.

Risk: Runtime dependencies are declared with minimum versions only.

Mitigation: Prefer pinned dependency versions before deployment.

## Reference(s):

- [Xtoys.app](https://xtoys.app)
- [ClawHub skill page](https://clawhub.ai/kasuganosora/skills/xtoys-app)
- [Publisher profile](https://clawhub.ai/user/kasuganosora)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python examples, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an xtoys.app webhook ID provided by environment variable, command-line option, or config file.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
