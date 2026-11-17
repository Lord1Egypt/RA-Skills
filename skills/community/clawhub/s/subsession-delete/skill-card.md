## Description:

Delete an OpenClaw child session cleanly by removing its transcript, trajectory files, and sessions.json index entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kid0114](https://clawhub.ai/user/kid0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to remove a spawned child session from local session files and the sessions.json index after confirming the exact target session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deletion script can be steered outside the intended OpenClaw session folder by unchecked identifiers.

Mitigation: Run dry-run mode first, use a verified session key, avoid elevated privileges, and use execute mode only after target paths are confirmed inside the intended OpenClaw sessions directory.

Risk: The skill performs destructive local deletion when execute mode is used.

Mitigation: Confirm the exact session target and avoid deleting active primary sessions unless the user explicitly approves.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Shell commands, Files, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is available by default; execute mode deletes session files and updates sessions.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
