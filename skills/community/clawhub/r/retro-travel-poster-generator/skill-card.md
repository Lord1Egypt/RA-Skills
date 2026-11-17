## Description:

Generates vintage-style travel poster images from text descriptions using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, sellers, and developers use this skill to generate retro travel-poster image URLs for print-on-demand products, wall art, postcards, travel branding, Airbnb listings, and related visual assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Neta API token, prompt text, and optional reference image ID to api.talesofai.com for image generation.

Mitigation: Use a low-privilege or disposable Neta token, avoid entering tokens into shell history, and review prompt and reference data before running the skill.

Risk: The main skill instructions under-disclose the actual API domain receiving the token.

Mitigation: Confirm comfort with sending data to api.talesofai.com and prefer a pinned release or verified artifact instead of a floating install command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blammectrappora/skills/retro-travel-poster-generator)
- [Neta API Access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports optional size selection and reference image UUID input.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
