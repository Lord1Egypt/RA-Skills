## Description:

Control and query LifeSmart Smart Station IoT devices registered in the RootONLocal app by querying local device and zone information, then calling the LifeSmart LocalWeb API to get or set device state and read measurements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kcobstkin](https://clawhub.ai/user/kcobstkin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent resolve natural-language smart-home requests into RootONLocal and LifeSmart LocalWeb calls for querying or controlling local IoT devices. It is intended for same-device use with a running RootONLocal app and configured Local Web credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read reusable local smart-home credentials and enumerate rooms and devices.

Mitigation: Use it only on a trusted machine and network, keep credentials in memory rather than persistent storage, and restrict access to the local API where possible.

Risk: The skill can send commands that change real devices, including HVAC, plugs, blinds, and IR power toggles.

Mitigation: Require explicit user confirmation for device-changing actions and treat ambiguous or unsupported device matches as errors.

Risk: HTTP or certificate-bypass configurations can weaken transport protections.

Mitigation: Prefer HTTPS where available, avoid HTTP configurations, and limit any certificate bypass to trusted private-network stations.

## Reference(s):

- [RootONLocal Monorepo](https://github.com/Kcobstkin/RootONLocal_Monorepo)
- [ClawHub skill page](https://clawhub.ai/kcobstkin/skills/rootonlocal-localweb204)
- [api-spec.md](artifact/api-spec.md)
- [localweb-spec.md](artifact/localweb-spec.md)
- [device-types.md](artifact/device-types.md)
- [examples.md](artifact/examples.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, JSON, configuration]

**Output Format:** [Markdown guidance with HTTP request examples and JSON response structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to return structured success or error JSON after local device discovery and LifeSmart LocalWeb calls.]

## Skill Version(s):

2.0.4 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
