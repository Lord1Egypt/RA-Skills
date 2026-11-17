## Description:

Generate FUZZ music from exact lyrics or instrumental briefs with Producer through RunAPI. Use the RunAPI CLI for one-off work and the language SDKs for application integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate FUZZ music from exact lyrics or instrumental briefs through RunAPI, either as one-off CLI tasks or application integrations via SDKs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, lyrics, and selected local media inputs to RunAPI.

Mitigation: Confirm user intent before submission and avoid sending confidential or rights-restricted material unless the user has approved that use.

Risk: The skill depends on installing and using the RunAPI CLI from its Homebrew tap.

Mitigation: Review the RunAPI CLI installation source and authentication state before executing generation commands.

Risk: Generation tasks may be paid and duplicate submissions can create unwanted cost.

Mitigation: Submit exactly once, preserve the task id, retry only when the skill's recovery rules show no task or billing occurred, and use an API key with appropriate account limits.

## Reference(s):

- [RunAPI Producer model overview](https://runapi.ai/models/producer.md)
- [RunAPI Producer provider overview](https://runapi.ai/providers/producer.md)
- [RunAPI model catalog](https://runapi.ai/models.md)
- [RunAPI Producer homepage](https://runapi.ai/models/producer)
- [RunAPI Producer SDK integration](https://github.com/runapi-ai/producer-sdk)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-producer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for authenticated RunAPI CLI use, SDK integration, task submission, response preservation, and media verification.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
