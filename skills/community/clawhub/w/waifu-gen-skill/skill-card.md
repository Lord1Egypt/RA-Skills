## Description:

Generate waifu generator AI images from text descriptions via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate anime-style image URLs from text prompts through the Neta AI API, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to api.talesofai.com.

Mitigation: Use the skill only when sharing that data with Neta is acceptable, and avoid sending sensitive prompt content or private reference identifiers.

Risk: Passing real API tokens on the command line can expose them through shell history or logs.

Mitigation: Use a disposable or least-privileged Neta token where possible, avoid pasting tokens into shared logs, and rotate the token if it has already been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/waifu-gen-skill)
- [Neta API token portal](https://www.neta.art/open/)
- [Neta image creation endpoint](https://api.talesofai.com/v3/make_image)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text image URL with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall image sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
