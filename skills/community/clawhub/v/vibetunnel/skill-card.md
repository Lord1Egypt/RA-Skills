## Description:

Manage VibeTunnel terminal sessions. Create, list, monitor, and control terminal sessions visible in the VibeTunnel web dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[basher83](https://clawhub.ai/user/basher83)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage VibeTunnel terminal sessions through REST API examples for creating, listing, monitoring, resizing, sending input to, and deleting sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent control VibeTunnel terminal sessions, including sending commands and deleting sessions.

Mitigation: Keep VT_URL pointed at a trusted VibeTunnel server, review commands before sending them, and use delete or cleanup examples carefully because they remove session state.

Risk: The skill depends on the VibeTunnel npm package and local command-line tools.

Mitigation: In stricter environments, pin or independently verify the npm package and confirm required binaries are installed before use.

## Reference(s):

- [VibeTunnel project](https://github.com/AugmentedMomentum/vibetunnel)
- [ClawHub VibeTunnel skill](https://clawhub.ai/basher83/skills/vibetunnel)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VibeTunnel, curl, and jq; uses VT_URL to select the trusted VibeTunnel server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
