## Description:

Control your Tesla vehicles - lock/unlock, climate, location, charge status, and more, with support for multiple vehicles via Tesla Fleet API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to authenticate with a Tesla account, inspect vehicle status, and run remote vehicle commands such as lock, unlock, climate, charging, location, horn, lights, and wake actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can issue real vehicle state-changing commands, including unlock, climate, charging, horn, lights, and wake actions.

Mitigation: Use it only in trusted sessions and require explicit confirmation before running state-changing commands.

Risk: Location output can reveal the precise position of a vehicle.

Mitigation: Avoid sharing location output and treat generated map links as sensitive personal data.

Risk: The local Tesla token cache can grant continued account access if exposed.

Mitigation: Protect ~/.tesla_cache.json with local file permissions and avoid copying it into shared logs, repositories, or support bundles.

Risk: The skill depends on the third-party teslapy package for Tesla API access.

Mitigation: Prefer pinning and reviewing the dependency before installation or deployment.

## Reference(s):

- [Tesla Fleet API Documentation](https://developer.tesla.com/docs/fleet-api)
- [Unofficial Tesla Owner API Documentation](https://tesla-api.timdorr.com)
- [ClawHub Tesla Skill](https://clawhub.ai/mvanhorn/skills/tesla)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [CLI text with optional JSON for vehicle data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TESLA_EMAIL and stores a local Tesla token cache at ~/.tesla_cache.json.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
