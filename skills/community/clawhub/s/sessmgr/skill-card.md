## Description:

Manage OpenClaw sessions by naming, listing, switching, creating, renaming, saving, and deleting them to persist and recover context by name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[detain](https://clawhub.ai/user/detain)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Sessmgr to organize named conversation sessions, switch back to prior context, and manage local session-name metadata without deleting transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A session-creation path can emit agent control output before validating the requested session name.

Mitigation: Review before installing and avoid untrusted or unusual session names until the validation gap is fixed.

Risk: The skill writes persistent local session-name metadata.

Mitigation: Use trusted names and descriptions, and review stored session mappings when managing sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/detain/skills/sessmgr)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with command examples and agent control tokens]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit RELOAD_SESSION:<sessionId> or NEW_SESSION:<name> control text for the host agent.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
