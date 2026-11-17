## Description:

Generates nostalgic selfie photos with Snapchat-style filter effects such as puppy ears, flower crowns, dog tongues, sparkle overlays, and bunny noses using the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate 2016-style social media selfie images from text prompts, optionally choosing image size or a reference image UUID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed through shell history when passed directly on the command line.

Mitigation: Use a trusted execution environment, avoid reusing exposed tokens, and rotate the Neta API token if it may have been disclosed.

Risk: Prompts and optional reference identifiers are sent to the Neta/TalesOfAI service.

Mitigation: Avoid sending sensitive personal photos, names, or identifying prompts unless the user accepts sharing them with that service.

Risk: Install commands run third-party skill code.

Mitigation: Install only from the server-resolved publisher and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/snapchat-filter-art-generator)
- [Neta API token signup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text image URL with command-line progress and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
