## Description:

AI tattoo design generator for creating custom tattoo concept art, ink illustrations, tattoo reference sheets, flash designs, sleeve ideas, minimalist tattoo art, tribal patterns, and fine line sketches through the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users, tattoo artists, and studios use this skill to generate tattoo concept images and reference sheets from text prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned npx install path can install a changed release.

Mitigation: Prefer the ClawHub install path or a pinned, trusted installer, and review the skill before running it.

Risk: Passing a real API token directly on the command line can expose it in shell history or shared logs.

Mitigation: Pass tokens through secure local practices, avoid literal tokens in command history, and do not share logs that may contain credentials.

Risk: Prompts and optional reference image identifiers are sent to an external image generation service.

Mitigation: Avoid sensitive or regulated prompts and review the external service terms before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/omactiengartelle/skills/tattoo-design-generator)
- [Neta API Access](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Markdown with inline bash commands and a direct image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; supports portrait, landscape, square, and tall sizes plus an optional reference image UUID.]

## Skill Version(s):

1.0.0 (source: evidence release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
