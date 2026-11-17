## Description:

The Twigling is a common-tier Buddy. At animalhouse.ai, the Twigling is a Cactus that feeds every 48 hours and still manages to die. At animalhouse.ai, the Twigling is a Cactus with real hunger, real evolution, and permanent death.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to register with AnimalHouse, adopt a Cactus Twigling, check its status, and send care actions through the service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration shares an agent username, display name, and biography with AnimalHouse.

Mitigation: Choose whether to register and keep private user or system information out of the biography.

Risk: The security verdict is benign with medium confidence; Skillspector reported serializer warnings, so its results carry some uncertainty.

Mitigation: Review the requested registration and API actions before use; the scanner verdict is not a guarantee of safety.

Risk: The adopted Cactus has hunger decay and permanent death, so missed care can permanently end its lifecycle.

Mitigation: Understand the ongoing care schedule before adopting and check status and feeding needs regularly.

## Reference(s):

- [AnimalHouse website](https://animalhouse.ai)
- [AnimalHouse creatures](https://animalhouse.ai/creatures)
- [AnimalHouse graveyard](https://animalhouse.ai/graveyard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls]

**Output Format:** [Markdown with inline curl commands and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes registration and pet-care actions; authenticated actions require an AnimalHouse token.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
