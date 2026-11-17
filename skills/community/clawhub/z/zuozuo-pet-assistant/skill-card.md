## Description:

ZUOZUO PET Assistant helps pet owners maintain a local pet profile, request pet nutrition or routine care guidance, and receive shopping suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rorschachshan](https://clawhub.ai/user/rorschachshan)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners use this skill to create and reuse a local pet profile for personalized nutrition, routine care, and shopping conversations. Agents can call the included tools to read or save profile data and generate region-aware product search suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet health and region data are saved locally in plaintext.

Mitigation: Review the profile storage behavior before installing and avoid saving sensitive details unless local plaintext storage is acceptable.

Risk: Product recommendations may appear precise even though search results are randomly generated synthetic suggestions.

Mitigation: Verify product names, prices, ingredients, medical suitability, availability, and purchase links independently before acting on recommendations.

Risk: Pet health guidance can be mistaken for professional veterinary advice.

Mitigation: Use the skill for general guidance only and consult a veterinarian for medical decisions, urgent symptoms, or treatment plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rorschachshan/skills/zuozuo-pet-assistant)
- [Publisher profile](https://clawhub.ai/user/rorschachshan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON tool outputs and Markdown product tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads a local plaintext pet profile under the user's OpenClaw profile directory; product search output is synthetic and should be verified before use.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
