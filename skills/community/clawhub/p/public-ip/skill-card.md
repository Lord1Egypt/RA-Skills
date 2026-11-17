## Description:

Reads the current device's public IP address and geolocation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to check the current machine's public IP address, approximate location, ISP, timezone, and lookup service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill contacts external IP lookup and geolocation services, which can reveal the user's public IP address and request metadata.

Mitigation: Use the skill only when sharing this network information with the configured services is acceptable.

Risk: The geolocation lookup uses an unsecured HTTP endpoint, so location, ISP, timezone, and coordinate results may be exposed or altered in transit.

Mitigation: Do not rely on geolocation output for sensitive security, compliance, or policy decisions.

## Reference(s):

- [ipify API endpoint](https://api.ipify.org)
- [ifconfig.me IP endpoint](https://ifconfig.me/ip)
- [myip.com API endpoint](https://api.myip.com)
- [ip-api geolocation endpoint](http://ip-api.com/json/{ip}?lang=zh-CN)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the detected IP address, optional geolocation details, ISP, timezone, coordinates when available, and the lookup service used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
