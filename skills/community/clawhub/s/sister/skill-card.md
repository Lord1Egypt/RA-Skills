## Description:

Distill your sisters - real sisters, besties, and female content creators - by capturing how they talk, their emotional intelligence, humor, supportive energy, and user-provided memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to build local profiles from their own memories and descriptions, then generate personality-style responses or group-chat simulations based on those profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently build detailed plaintext profiles and interaction logs about real people.

Mitigation: Install only when local plaintext storage is acceptable, review stored profiles regularly, and delete unwanted profile folders under ~/.sister-skill/sisters/.

Risk: Broad memory prompts may encourage entry of sensitive personal information about the user or third parties.

Mitigation: Avoid entering sensitive details such as health, finances, trauma, private conflicts, secrets, or third-party information given without consent.

Risk: Generated personality-style responses may be mistaken for, or used to impersonate, real people.

Mitigation: Use generated responses as user-controlled simulations and keep responsibility with the operator; do not present outputs as statements from the real person.

## Reference(s):

- [Sister Archetypes Reference Guide](references/sister-archetypes.md)
- [Sister.skill on ClawHub](https://clawhub.ai/realteamprinz/skills/sister)
- [Publisher profile](https://clawhub.ai/user/realteamprinz)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Natural-language responses, Markdown profile files, and JSONL interaction log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local plaintext profiles and logs under ~/.sister-skill/sisters/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
