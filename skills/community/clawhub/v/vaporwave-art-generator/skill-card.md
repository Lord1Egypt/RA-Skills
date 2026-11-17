## Description:

AI vaporwave art generator - create synthwave, retrowave, and aesthetic vaporwave images with neon grids, 80s retro colors, palm trees, and lo-fi vibes using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate vaporwave, synthwave, and retrowave image URLs from text prompts, with optional output sizing and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference UUIDs, and the Neta API token are sent to the Neta/TalesOfAI service.

Mitigation: Use only prompts and references that are appropriate for that external service, and use a limited or revocable token.

Risk: Passing long-lived tokens directly on the command line can expose them through shell history or process inspection.

Mitigation: Prefer short-lived or revocable tokens and avoid storing sensitive tokens in shell history.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/vaporwave-art-generator)
- [Publisher Profile](https://clawhub.ai/user/omactiengartelle)
- [Neta API Token Setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL printed to stdout, with status messages on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports landscape, portrait, square, and tall image dimensions; optional reference image UUID for style inheritance.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
