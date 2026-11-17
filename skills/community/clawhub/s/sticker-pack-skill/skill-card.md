## Description:

Generate sticker pack images from text descriptions via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blammectrappora](https://clawhub.ai/user/blammectrappora)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate sticker-style images from text prompts, optionally choosing an image size or reference image ID for style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference image IDs, and the Neta/TalesOfAI API token are sent to an external image service.

Mitigation: Avoid sensitive prompt content and use a low-privilege or disposable API token for this skill.

Risk: The token is passed on the command line, where it may be exposed through shell history or local process inspection.

Mitigation: Use short-lived tokens where possible, avoid pasting long-lived credentials into shared shells, and rotate any token that may have been exposed.

Risk: Release evidence flags the install and data-flow disclosures as incomplete.

Mitigation: Review the skill source and install from a pinned or otherwise verifiable release before deployment.

## Reference(s):

- [Sticker Pack Skill on ClawHub](https://clawhub.ai/blammectrappora/skills/sticker-pack-skill)
- [Neta API token setup](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with progress and error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a direct generated image URL after polling the external image service.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
