## Description:

Send Wake-on-LAN magic packets to wake sleeping devices on a local network using saved aliases or direct MAC/IP commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofqin2026](https://clawhub.ai/user/kingofqin2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and home-lab administrators use this skill to wake known devices on a LAN and manage local Wake-on-LAN device aliases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper sends Wake-on-LAN UDP packets on the local network, including broadcast traffic.

Mitigation: Run it only on networks and devices you administer, and confirm the target MAC, IP, and port before use.

Risk: Saved aliases store MAC and IP details locally in the skill directory.

Mitigation: Limit access to the skill directory and avoid saving sensitive network inventory on shared systems.

Risk: The wakeonlan dependency is installed separately and may vary across environments.

Mitigation: Use a virtual environment and pin the dependency for reproducible deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofqin2026/skills/wake-lan)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local device aliases when the helper script is run.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
