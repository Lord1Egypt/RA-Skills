## Description:

Y2K aesthetic generator for nostalgic early-2000s and 2010s throwback photos, including flash-photography selfies, Snapchat-era looks, low-res iPhone vibes, butterfly clips, frosted makeup, and dreamy mall-photo nostalgia via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate nostalgic Y2K and 2010s-style images from text prompts for social content, profile pictures, invitations, and moodboards. Agents can run the CLI with a Neta token, optional output size, and optional reference image UUID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passing the Neta API token directly on the command line can expose it through shell history, process listings, or logs.

Mitigation: Use a safer token handling method where possible, avoid entering real tokens directly in shared shell commands, and rotate any token that may have been exposed.

Risk: The documented npx install path is unpinned.

Mitigation: Prefer a pinned version or a trusted installer path before using the skill in a production or shared environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/omactiengartelle/skills/y2k-aesthetic-generator)
- [Publisher profile](https://clawhub.ai/user/omactiengartelle)
- [Neta API token signup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text output containing a direct image URL, with Markdown usage examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
