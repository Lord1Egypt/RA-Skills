## Description:

Automates WeChat public-account article collection, AI rewriting, storyboard and image prompt generation, cover creation, and HTML article assembly for MUX-style branded content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dally-bee](https://clawhub.ai/user/dally-bee)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers and operators use this skill to draft WeChat public-account articles from approved source material, reshape them for MUX fitness branding, and produce article HTML with image and cover guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published artifact includes a credential-like API key.

Mitigation: Rotate and remove the exposed key before use, and load credentials from a protected environment variable or secret store.

Risk: The artifact describes unscoped scraping of WeChat article URLs.

Mitigation: Restrict scraping to approved public article hosts and add request timeouts, response limits, and user confirmation.

Risk: The workflow can send third-party article content and prompts to external AI services.

Mitigation: Confirm user authorization before sending content externally and avoid submitting sensitive or restricted material.

Risk: The built-in compliance check is limited to keyword screening.

Mitigation: Use human review for legal, advertising, and platform-policy compliance before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dally-bee/skills/wechat-article-auto-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, HTML]

**Output Format:** [Markdown guidance with Python and HTML code examples; generated article deliverables are described as HTML with embedded images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article target is 1500-2000 words with 6-8 images, 900x383 cover output, and HTML under 5 MB when following the artifact guidance.]

## Skill Version(s):

1.0.0 (source: evidence release metadata, artifact/_meta.json, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
