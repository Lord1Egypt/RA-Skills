## Description:

Smart Image Finder helps AI agents find, generate, download, and verify images for articles, dashboards, thumbnails, and content creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinbao19](https://clawhub.ai/user/justinbao19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to locate authentic news images, search image results through Brave, generate concept images, download image files, and verify that downloaded content is usable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, article URLs, and image generation prompts may be sent to external services and image hosts.

Mitigation: Avoid sensitive search terms, protect the Brave API key, and review service and image licensing terms before publication.

Risk: Downloaded files may be inaccessible, low quality, non-image responses, or unsuitable for reuse.

Mitigation: Use the provided verification steps before relying on downloaded files and manually review image quality, content, and publishing rights.

## Reference(s):

- [Smart Image Finder on ClawHub](https://clawhub.ai/justinbao19/skills/smart-image-finder)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use BRAVE_API_KEY for Brave Image Search and may write downloaded image files into the workspace.]

## Skill Version(s):

1.0.4 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
