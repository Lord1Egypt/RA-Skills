## Description:

Rebuilds and validates a reusable OBS streaming scene pack via agentic-obs and mcporter for local or remote OBS setups, LAN-served browser overlays, recording smoke tests, and browser-source troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowcrab-dev](https://clawhub.ai/user/snowcrab-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, stream operators, and agent builders use this skill to create and validate OBS scene packs, attach browser overlays, configure OBS connection targets, apply transition and audio defaults, and run recording or streaming checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The overlay server can expose workspace files over LAN.

Mitigation: Run it only from a workspace without secrets, bind it to a trusted interface where possible, or serve a dedicated public overlay directory.

Risk: The stream dry-run helper can start real streaming if OBS is configured for a live destination.

Mitigation: Use the dry-run helper only after confirming OBS points to a test destination, or skip it and rely on recording smoke tests.

Risk: The scripts mutate OBS scenes, transitions, audio settings, recording state, streaming state, and agentic-obs target configuration.

Mitigation: Back up OBS scenes first, verify the target OBS host and port, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snowcrab-dev/skills/streaming-obs-bootstrap)
- [Publisher profile](https://clawhub.ai/user/snowcrab-dev)
- [Scene Map](references/scene-map.md)
- [Networking Notes](references/networking.md)
- [Troubleshooting](references/troubleshooting.md)
- [v0.2.0 Feature Notes](references/v0.2-features.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Files, Guidance]

**Output Format:** [Markdown with inline bash commands, shell scripts, OBS configuration actions, and HTML overlay files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May mutate OBS scenes, OBS recording or streaming state, agentic-obs configuration, and local HTTP server state.]

## Skill Version(s):

0.2.0 (source: server release metadata and PUBLISH.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
