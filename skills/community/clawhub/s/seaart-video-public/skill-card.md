## Description:

Use this skill to generate high-quality AI videos using the SeaArt platform (seaart.ai), supporting Text-to-Video and Image-to-Video generation with multiple models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seaartpublic](https://clawhub.ai/user/seaartpublic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create SeaArt text-to-video or image-to-video generations, choose supported models and aspect ratios, and receive the generated video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a SeaArt session token and its instructions can lead an agent to reveal whether or how the token is configured.

Mitigation: Use non-disclosing token presence checks, never print `SEAART_TOKEN`, and keep the token in a private local configuration.

Risk: Prompts, image URLs, and the SeaArt session token are sent to SeaArt endpoints.

Mitigation: Install and use the skill only when the user trusts SeaArt with the submitted creative content and account credential.

Risk: Broad activation for video requests may call an external generation service when the user did not explicitly intend to use SeaArt.

Mitigation: Prefer explicit SeaArt requests or confirm the service choice before submitting generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seaartpublic/skills/seaart-video-public)
- [SeaArt platform](https://www.seaart.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and a generated video URL returned as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, and a SEAART_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
