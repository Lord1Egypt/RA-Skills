## Description:

Control and monitor Tesla vehicles through the Tessie API, including vehicle status, climate, charging, locks, location, and software update actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biguntroll](https://clawhub.ai/user/biguntroll)

### License/Terms of Use:


## Use Case:

External users and developers with a Tessie API token use this skill to let an agent check Tesla vehicle state and run supported Tessie vehicle actions. Typical tasks include battery, location, climate, charging, lock, trunk, and software update workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can remotely query and control a real Tesla, including sensitive actions such as unlocking, opening trunks, changing charging, disclosing location, and scheduling software updates.

Mitigation: Require explicit user confirmation before executing vehicle-control actions or disclosing location, and review the exact VIN and requested action before running commands.

Risk: A Tessie API token grants access to vehicle data and commands if exposed.

Mitigation: Use only a Tessie token controlled by the user, avoid storing it in broadly readable shell profiles, and rotate the token if exposure is suspected.

Risk: Vehicle state, VIN, and location output can reveal private information.

Mitigation: Limit status and location checks to user-requested tasks, avoid sharing raw outputs unnecessarily, and redact sensitive fields when presenting results outside the local session.

## Reference(s):

- [Tessie API Reference](references/api.md)
- [Tessie Developer Reference](https://developer.tessie.com/reference)
- [Tessie API Token Settings](https://my.tessie.com/settings/api)
- [ClawHub Skill Page](https://clawhub.ai/biguntroll/skills/tesla-tessie)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; invoked scripts return JSON or concise status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-controlled TESSIE_API_KEY environment variable and, for most actions, a target vehicle VIN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
