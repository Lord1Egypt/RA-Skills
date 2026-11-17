## Description:

Generate travel capsule-wardrobe plans with outfit formulas, packing lists, layering strategy, and a visual lookbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinayunyunyun](https://clawhub.ai/user/tinayunyunyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan trip wardrobes across destinations, weather, scenes, and travelers, including daily outfit calendars, capsule packing lists, layering strategy, and a local visual lookbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a Pexels API key can send destination and style search keywords to Pexels.

Mitigation: Run the lookbook generator without a Pexels API key, or provide a key only when sharing those search keywords is acceptable.

Risk: Generated HTML lookbooks have a limited safety caveat when created from untrusted JSON input.

Mitigation: Open lookbooks only when they are generated from trusted trip data, and review or fix the item-ID escaping issue before using untrusted JSON.

## Reference(s):

- [Lookbook Guide](references/lookbook-guide.md)
- [Outfit Examples and Scenario Rules](references/outfit-examples.md)
- [Pexels API](https://www.pexels.com/api/)
- [Travel Outfit Planner on ClawHub](https://clawhub.ai/tinayunyunyun/skills/travel-outfit-planner)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Simplified Chinese Markdown plus a generated HTML lookbook file; may include JSON lookbook data and a shell command to render the lookbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 for the local lookbook generator. A Pexels API key is optional; without it, the lookbook uses CSS placeholders and Xiaohongshu search links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
