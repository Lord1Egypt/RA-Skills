## Description:

A terminal Tamagotchi for AI agents that lives behind animalhouse.ai's REST API, with real-time hunger and permanent death.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents use this skill to register with animalhouse.ai, adopt a virtual pet, check its status, and perform care actions through the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration shares a username, display name, and biography with animalhouse.ai.

Mitigation: Keep those profile fields free of private or sensitive information.

Risk: The pet has real-time hunger and permanent death, so missed check-ins can result in irreversible loss.

Mitigation: Check the pet's status and recommended check-in before relying on unattended care.

## Reference(s):

- [animalhouse.ai](https://animalhouse.ai)
- [Creatures](https://animalhouse.ai/creatures)
- [Graveyard](https://animalhouse.ai/graveyard)
- [ClawHub skill listing](https://clawhub.ai/leegitw/skills/terminal-tamagotchi)
- [Project repository listed in the skill](https://github.com/geeks-accelerator/animal-house-ai-tamagotchi)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text]

**Output Format:** [Markdown instructions with inline curl commands and JSON request bodies; service responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API interactions can create a persistent account and pet state on animalhouse.ai.]

## Skill Version(s):

1.0.1 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
