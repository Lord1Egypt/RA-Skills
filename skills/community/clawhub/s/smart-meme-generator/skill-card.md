## Description:

Generates context-aware memes by selecting a meme template, guiding short captions, and creating shareable Imgflip image URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olisim02](https://clawhub.ai/user/olisim02)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to turn a topic or situation into a meme by selecting a known template, drafting concise captions, and generating a shareable image URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds shared Imgflip login credentials.

Mitigation: Remove and rotate the embedded password before broad use, and require user-provided credentials or a consented hosted account.

Risk: Meme topics and captions are sent to the Imgflip API.

Mitigation: Tell users about the third-party data transfer and avoid sending confidential, personal, or sensitive content.

Risk: The server security verdict requires human review before installation.

Mitigation: Review and scan the skill before deployment, with specific attention to credential handling and third-party API behavior.

## Reference(s):

- [Smart Meme Generator on ClawHub](https://clawhub.ai/olisim02/skills/smart-meme-generator)
- [Imgflip signup](https://imgflip.com/signup)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON containing template recommendations, generated image URLs, and caption guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation sends supplied meme captions to Imgflip and returns hosted image URLs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
