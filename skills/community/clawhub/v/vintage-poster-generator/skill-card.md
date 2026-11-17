## Description:

AI vintage poster generator that creates retro art prints, old-school travel posters, 1950s-1970s style illustrations, antique advertising art, and nostalgic wall art from text prompts via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, marketplace sellers, and agents use this skill to generate vintage-style poster images from text prompts and optional reference image UUIDs. It returns a direct image URL after submitting and polling an external image-generation task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to pass an API token on the command line, which can expose the token through shell history or local process inspection.

Mitigation: Use a limited-scope token where possible and avoid placing real tokens directly in reusable shell history or shared command logs.

Risk: Prompts, reference image UUIDs, and the API token are sent to the external Neta/TalesOfAI service.

Mitigation: Review prompts and reference IDs for sensitive content before use, and disclose the external service dependency to users before deployment.

Risk: The server security verdict is suspicious because external-service behavior and token handling are incompletely disclosed in the main skill file.

Mitigation: Review the skill before installing, scan it before deployment, and prefer an immutable or pinned install source when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/vintage-poster-generator)
- [Publisher Profile](https://clawhub.ai/user/blammectrappora)
- [Neta API Token Page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Plain text image URL with Markdown shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token, accepts portrait, landscape, square, and tall size options, and can use a reference image UUID for style inheritance.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
