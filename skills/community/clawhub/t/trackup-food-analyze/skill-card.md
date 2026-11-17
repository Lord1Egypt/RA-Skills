## Description:

Analyze a food image with AISpark TrackUp production APIs, using AnalyzeWholeFood for full analysis and dedicated endpoints for macros, ingredients, health insight, and keyword-based food search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trackup](https://clawhub.ai/user/trackup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze food images or lookup foods by keyword through AISpark TrackUp APIs while preserving API-returned nutrition values exactly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Food images, base64 image data, food keywords, and nutrition-analysis context are sent to an external deepeat.ai service.

Mitigation: Use the skill only when that data sharing is acceptable for the user and environment.

Risk: The documented /tmp image workflow can expose sensitive local image data on shared systems.

Mitigation: Use a private temporary directory with restrictive permissions and remove temporary image payload files after the request.

Risk: The proxy bypass example can evade managed network controls if used in workplace environments.

Mitigation: Unset proxy variables only when direct outbound access is explicitly authorized.

## Reference(s):

- [TrackUp Food Analyze ClawHub page](https://clawhub.ai/trackup/skills/trackup-food-analyze)
- [deepeat.ai service endpoint](https://deepeat.ai)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with JSON and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns API-provided nutrition fields, health insight fields, food-search results, and error guidance without inventing missing values.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
