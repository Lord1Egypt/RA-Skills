## Description:

Control Xiaomi/Mi Home devices through the Home Assistant REST API for lights, switches, sensors, climate devices, fans, media players, and scenes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangqiulong](https://clawhub.ai/user/huangqiulong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and smart-home operators use this skill to configure Home Assistant access, discover Xiaomi/Mi Home entities, query device state, and issue REST API service calls from natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a long-lived Home Assistant token to control devices.

Mitigation: Configure the token through a protected local mechanism, do not paste real tokens into chat, and prefer a dedicated low-privilege Home Assistant account where possible.

Risk: Broad service-call and bulk-control examples can affect multiple smart-home devices.

Mitigation: Review target entity IDs before execution and avoid live tests or bulk commands against critical devices unless the impact is understood.

Risk: Home Assistant traffic may expose device-control credentials if sent over an untrusted endpoint.

Mitigation: Use HTTPS or a trusted local Home Assistant endpoint before running live commands.

## Reference(s):

- [Home Assistant REST integration](https://www.home-assistant.io/integrations/rest/)
- [ClawHub skill page](https://clawhub.ai/huangqiulong/skills/xiaomi-homne-ha)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq or Node.js helpers, HA_URL, and HA_TOKEN for live Home Assistant operations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
