## Description:

Helps agents create adults-only images, videos, edits and text through SpicyAPI, with model selection, price quotes and consent checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spicyapi-owner](https://clawhub.ai/user/spicyapi-owner)

### License/Terms of Use:

MIT-0

## Use Case:

Adult creators and developers use this skill to choose SpicyAPI models, draft prompts, request price quotes and generate consenting-adult images, videos, edits or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected local media are sent to SpicyAPI.

Mitigation: Review what is submitted and avoid sensitive or identifiable imagery without consent.

Risk: Generation can create billable jobs.

Mitigation: Review the quoted maximum charge before approval or set a cost ceiling.

Risk: Adult generation may involve minors or non-consensual depictions of real people.

Mitigation: Refuse sexual content involving minors and require documented consent for identifiable adults.

Risk: Exposure of the SpicyAPI credential could permit unauthorized use.

Mitigation: Use a dedicated SPICY_API_KEY and do not print, log or commit it.

## Reference(s):

- [SpicyAPI website](https://spicyapi.ai)
- [Listed repository](https://github.com/Spicy-API/nsfw-ai-skill)
- [Model reference](references/models.md)
- [Prompting guide](references/prompting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Images, Videos]

**Output Format:** [Markdown guidance, CLI text or JSON, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation requires a price quote and user approval or a preset cost ceiling.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
