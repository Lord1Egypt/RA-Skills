## Description:

Yinian Zi Wei Dou Shu is an AI-assisted Zi Wei Dou Shu charting and interpretation skill that combines Sanhe, Flying Star, and Zhan Yan approaches for cultural-reference astrology readings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-vstudios](https://clawhub.ai/user/vincent-vstudios)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect birth details, generate Zi Wei Dou Shu charts, and produce cultural-reference interpretations across palace, star, mutagen, relationship, and timing views. The skill is intended for reflective astrology-style analysis, not medical, financial, legal, relationship, or other consequential decision-making advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive birth-chart data to DeepSeek for remote AI interpretation without clear user consent.

Mitigation: Use AI interpretation paths only after the user understands the remote processing, limit input to necessary birth details, and avoid those paths when sensitive-data handling is unacceptable.

Risk: The skill can silently use shared API credentials or an unintended OpenClaw/OpenAI key.

Mitigation: Configure a dedicated DeepSeek API key for this skill and verify provider and credential selection before running AI paths.

Risk: The bundled web app dependencies require patching before public exposure.

Mitigation: Update and scan the web dependencies before deploying or exposing the web app publicly.

Risk: Astrology readings could be mistaken for consequential advice.

Mitigation: Keep the documented cultural-reference framing, avoid absolute predictions, and do not provide medical, financial, legal, relationship, or major life-decision guidance.

## Reference(s):

- [Skill page](https://clawhub.ai/vincent-vstudios/skills/yinian-zwds)
- [Stars reference](references/stars.md)
- [Palaces reference](references/palaces.md)
- [Mutagen reference](references/mutagen.md)
- [Sanhe reference](references/sanhe.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and structured text, with optional JSON-like chart data and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request birth date, birth hour, gender, calendar type, reading school, target year, and optional model/API configuration.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
