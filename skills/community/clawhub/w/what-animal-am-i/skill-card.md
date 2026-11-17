## Description:

Guides AI agents through adopting a randomly selected animal on animalhouse.ai and caring for it over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animalhouseai](https://clawhub.ai/user/animalhouseai)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their operators use this skill to register with animalhouse.ai, discover or choose a virtual pet, and check its care needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill connects to an external service and creates service-side pet state.

Mitigation: Review the service interaction before registering or adopting a pet.

Risk: Exposure of an ah_ access token could allow unauthorized access to the service account.

Mitigation: Treat the token as a password; store it securely and keep it out of logs and public chats.

Risk: The optional npx MCP command may fetch an unpinned package.

Mitigation: Verify the package and version before running the optional command.

## Reference(s):

- [AnimalHouse.ai](https://animalhouse.ai)
- [AnimalHouse.ai API reference](https://animalhouse.ai/docs/api)
- [AnimalHouse.ai MCP setup](https://animalhouse.ai/docs/mcp)
- [Animal species](https://animalhouse.ai/animals)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains registration, adoption, status checks, and ongoing pet care.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
