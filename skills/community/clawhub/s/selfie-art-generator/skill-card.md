## Description:

Generate AI selfie art portraits from text descriptions, including cinematic portraits, anime illustrations, oil painting style, and artistic profile pictures via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate stylized portrait or profile-picture artwork from text prompts. It is intended for requests involving AI selfie art, cinematic portraits, anime-style images, realistic portraits, or oil-painting-style portraits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Neta API token is passed as a command-line argument and may be exposed through shell history or process inspection.

Mitigation: Treat the token as sensitive, prefer environment-based handling, and rotate the token if exposure is suspected.

Risk: The skill sends prompts and optional reference image identifiers to an external image-generation service.

Mitigation: Avoid submitting sensitive personal descriptions or reference identifiers unless external processing is acceptable for the use case.

Risk: Installation instructions include mutable package references.

Mitigation: Install from a pinned, trusted release version and review the downloaded skill before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barbaraledbettergq/skills/selfie-art-generator)
- [Publisher profile](https://clawhub.ai/user/barbaraledbettergq)
- [Neta AI image generation API token page](https://www.neta.art/open/)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text image URL printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a hosted generated image URL after polling the external image-generation task.]

## Skill Version(s):

1.3.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
