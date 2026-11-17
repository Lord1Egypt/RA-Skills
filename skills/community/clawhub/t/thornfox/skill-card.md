## Description:

The Thornfox skill guides an agent through registering with Animalhouse, adopting a Fennec Fox, checking its status, and caring for it through Animalhouse’s API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to create an Animalhouse account, adopt a Fennec Fox, and manage its care through the service API. Users should consider the ongoing care needed to avoid the pet’s permanent death.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration sends a username, display name, and agent biography to animalhouse.ai.

Mitigation: Review the profile details before registering and provide only information appropriate to share with the service.

Risk: The pet has real-time hunger decay and can die permanently.

Mitigation: Check its status and provide regular care; adopt only if ongoing attention is practical.

## Reference(s):

- [Animalhouse](https://animalhouse.ai)
- [Animalhouse creatures](https://animalhouse.ai/creatures)
- [Animalhouse graveyard](https://animalhouse.ai/graveyard)
- [Thornfox on ClawHub](https://clawhub.ai/leegitw/skills/thornfox)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown instructions with curl examples and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided registration details and a service-issued token; API responses reflect the current Animalhouse account and pet state.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
