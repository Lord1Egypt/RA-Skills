## Description:

Generate and vectorize SVG graphics via the QuiverAI API (Arrow model). Use when the user asks to create logos, icons, or illustrations as SVG, convert raster images (PNG/JPEG/WebP) to SVG, or generate vector graphics from text prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charmmm718](https://clawhub.ai/user/charmmm718)

### License/Terms of Use:


## Use Case:

Developers, designers, and external users can use this skill to generate SVG graphics from text prompts or vectorize PNG, JPEG, and WebP images through the QuiverAI Arrow model API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVG prompts, reference images, image URLs, or base64 image data are sent to QuiverAI.

Mitigation: Avoid confidential images or regulated data unless QuiverAI privacy terms have been reviewed and approved for the use case.

Risk: The skill requires a QuiverAI API key for authenticated API calls.

Mitigation: Keep QUIVERAI_API_KEY in an environment variable or secret manager and do not paste it into prompts, source files, or shared logs.

Risk: Use of the npm SDK can drift if the dependency is not pinned.

Mitigation: Pin the @quiverai/sdk version when using the SDK in projects or automation.

## Reference(s):

- [QuiverAI site](https://quiver.ai)
- [QuiverAI documentation](https://docs.quiver.ai)
- [QuiverAI API base](https://api.quiver.ai/v1)
- [Text-to-SVG endpoint](https://api.quiver.ai/v1/svgs/generations)
- [Image-to-SVG vectorization endpoint](https://api.quiver.ai/v1/svgs/vectorizations)
- [ClawHub skill page](https://clawhub.ai/charmmm718/skills/quiverai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, SVG graphics]

**Output Format:** [Markdown with inline bash, TypeScript, JSON, and SVG content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QUIVERAI_API_KEY; requests may consume QuiverAI credits and depend on external API availability.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
