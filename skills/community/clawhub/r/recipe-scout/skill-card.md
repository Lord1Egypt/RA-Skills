## Description:

Find and normalize Chinese recipes from structured sources first, then export clean recipe notes to Obsidian markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cylqqqcyl](https://clawhub.ai/user/cylqqqcyl)

### License/Terms of Use:

MIT-0

## Use Case:

Home cooks, recipe curators, and agents use this skill to discover Chinese recipes, compare candidate sources, normalize ingredients and steps, and optionally create Obsidian recipe notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipe notes may be written to an unintended Obsidian vault or fallback export path.

Mitigation: Confirm the destination path before export and return the written file paths for user review.

Risk: Browser fallback may use an available browser profile or session for recipe pages that require rendering or login.

Mitigation: Prefer web search and fetch for structured recipe pages, and use browser access only when rendering or transcript interaction is necessary.

Risk: Social or incomplete recipe sources can provide missing or unreliable ingredient amounts, timings, or technique details.

Mitigation: Prioritize structured recipe sources, mark low-confidence social-source details clearly, and avoid fabricating measurements or cooking times.

## Reference(s):

- [Recipe Scout ClawHub Page](https://clawhub.ai/cylqqqcyl/skills/recipe-scout)
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)
- [Obsidian Recipe Note Template](artifact/references/obsidian-template.md)
- [Query Formulation Examples](artifact/references/query-examples.md)
- [Extraction Schema](artifact/references/schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown responses and optional Obsidian-compatible recipe note files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source confidence, normalized recipe fields, shopping lists, and exported file paths when note export is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
