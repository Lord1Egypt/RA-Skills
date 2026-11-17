## Description:

Control Tesla vehicles through the MyTeslaMate API, including multi-vehicle accounts, climate control, charge limits, and charging schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovaris](https://clawhub.ai/user/ovaris)

### License/Terms of Use:

MIT

## Use Case:

External Tesla owners and developers use this skill to let an agent inspect vehicle status and operate MyTeslaMate workflows for climate and charging. It is intended for accounts with an existing MyTeslaMate vehicle, API token, and VIN.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a real vehicle's state, including climate, charging limits, wake state, and charging schedules.

Mitigation: Require explicit user confirmation before running any command that changes vehicle state.

Risk: The MyTeslaMate token grants vehicle-control authority.

Mitigation: Store TESLA_MATE_TOKEN outside prompts and logs, limit access to trusted agents, and rotate the token if it is exposed.

Risk: The security evidence identifies an undocumented command that deletes charging schedules without confirmation.

Mitigation: Only allow schedule deletion after a clear confirmation that explains the configured schedules may be removed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ovaris/skills/tesla-commands)
- [MyTeslaMate Fleet App](https://app.myteslamate.com/fleet)
- [MyTeslaMate Vehicles API Endpoint](https://api.myteslamate.com/api/1/vehicles)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Command-line guidance and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TESLA_MATE_TOKEN and a target VIN; state-changing commands should require explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: package.json and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
