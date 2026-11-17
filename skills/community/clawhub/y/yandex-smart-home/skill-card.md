## Description:

Helps an agent use Yandex's official IoT API to list Yandex Smart Home devices, read device state, change device or group settings, and run scenarios with a user-provided OAuth token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dima-online](https://clawhub.ai/user/dima-online)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect Yandex Smart Home inventory, issue supported device or group commands, and start named scenarios through Yandex's IoT API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can directly control physical smart-home devices and launch scenarios.

Mitigation: Require explicit user confirmation before device, group, or scenario actions, especially broad commands such as turning everything off.

Risk: Exposure of the YANDEX_IOT_TOKEN could let another party inspect or control the user's devices.

Mitigation: Keep the token out of chats, logs, and shared files; use the least-privilege token available and revoke or rotate it if exposed.

Risk: Ambiguous natural-language requests can target the wrong device, group, or scenario.

Mitigation: Fetch the current device inventory and confirm the matched target before sending commands when the user's request is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dima-online/skills/yandex-smart-home)
- [Yandex Smart Home IoT API endpoint](https://api.iot.yandex.net/v1.0)
- [Yandex OAuth application registration](https://oauth.yandex.ru/client/new)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YANDEX_IOT_TOKEN and curl; API results depend on the user's Yandex Smart Home account and token scopes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
