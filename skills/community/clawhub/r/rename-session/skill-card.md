## Description:

Rename or auto-generate a friendly label for an OpenClaw-style session by editing sessions.json directly, with random zh/en labels, locale detection, multi-agent detection, listing, retry verification, and XDG-compliant history storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to list, rename, or auto-label OpenClaw-compatible local sessions without using a client UI. It is intended for local session metadata management where direct edits to sessions.json are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits local OpenClaw-compatible session metadata directly, so an incorrect root, agent, session key, or label can change the wrong session record.

Mitigation: Use --root and --agent deliberately, list sessions first when uncertain, and back up sessions.json when labels are important.

Risk: Optional installation through an unpinned npx command can fetch changing third-party code.

Mitigation: Prefer a reviewed or pinned install path for environments where reproducibility or supply-chain review matters.

Risk: Concurrent writers, filesystem permission issues, read-only disks, or full disks can prevent reliable label updates.

Mitigation: Run the command when other tools are not actively changing sessions.json and review the command's verification and error output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skills/rename-session)
- [Testing Plan](references/TESTING.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line text output and markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local sessions.json labels and a local XDG history.json file when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
