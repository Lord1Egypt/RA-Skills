## Description:

Generates custom collectible trading-card art from text prompts in MTG, Pokemon, Yu-Gi-Oh, and sports card styles using the Neta image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omactiengartelle](https://clawhub.ai/user/omactiengartelle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create finished collectible-card style image art from plain-English prompts, with optional size selection and reference-image style inheritance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Neta API token are sent to an external image-generation service.

Mitigation: Use the skill only when the Neta service is acceptable for the prompt content and token handling requirements.

Risk: Passing the API token with --token can expose it in shell history, process listings, or shared transcripts.

Mitigation: Avoid placing real tokens in reusable shell commands or logs, and rotate any token that has already been exposed.

Risk: The release evidence notes an unpinned installer path.

Mitigation: Prefer a trusted, pinned ClawHub release path when available and review or scan the skill before deployment.

## Reference(s):

- [Trading Card Generator ClawHub release](https://clawhub.ai/omactiengartelle/skills/trading-card-generator)
- [Neta API access](https://www.neta.art/open/)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text direct image URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The URL points to generated trading-card image art; generation depends on the external Neta API and a user-provided API token.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
