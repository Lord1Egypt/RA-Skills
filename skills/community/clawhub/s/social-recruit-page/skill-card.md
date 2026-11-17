## Description:

Generates a high-end black-and-gold vertical recruitment poster for private circles, paid communities, and premium clubs, with optional Feishu image delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyken](https://clawhub.ai/user/jackyken)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, community operators, and agent users use this skill to produce configurable recruitment poster images for private circles, paid communities, and premium clubs. It can also post the generated image to Feishu when the user intentionally supplies app credentials and a recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local poster generation can render unescaped user content in Chromium.

Mitigation: Treat configuration content as trusted input and avoid pasting untrusted HTML.

Risk: The skill can contact external services and upload generated images when Feishu sending is enabled.

Mitigation: Enable Feishu delivery only when intentional, and supply app credentials and recipients only for approved destinations.

Risk: The server security verdict is suspicious and recommends review before installation.

Mitigation: Review and scan the skill before deployment, especially in environments that restrict local browser execution or outbound network access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackyken/skills/social-recruit-page)
- [Google Fonts stylesheet used by the poster template](https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, API Calls]

**Output Format:** [PNG image file plus Markdown usage guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional JSON configuration for poster content and optional Feishu credentials for image upload and message delivery.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
