## Description:

Adds TikTok-style text overlays to images and videos with styled fonts, backgrounds, strokes, and timed animations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmuweili](https://clawhub.ai/user/xmuweili)

### License/Terms of Use:

MIT

## Use Case:

Developers and content automation agents use this skill to add styled text overlays to image and video files, including multiple captions, timed video text, backgrounds, strokes, and fade animations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned Python dependencies for local media processing.

Mitigation: Install it in a virtual environment or container and avoid administrator-level installs.

Risk: The skill reads and writes local image and video files supplied by the user or calling agent.

Mitigation: Use trusted input paths and review output paths before running file-writing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmuweili/skills/tiktok-overlay)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with Python examples and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or returns edited image and video files through local Python utilities.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
