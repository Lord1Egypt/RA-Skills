## Description:

Transform raw Roblox gameplay footage into platform-ready promotional clips for TikTok, YouTube Shorts, Instagram Reels, and YouTube using smart trimming, aspect ratio conversion, music sync, captions, and brand overlays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cogniwatchdev](https://clawhub.ai/user/cogniwatchdev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content creators, and marketing teams use this skill to turn Roblox gameplay recordings into promotional clips and trailers optimized for short-form social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg wrapper inputs can expose unsafe text or path handling when titles, CTAs, subtitle paths, music paths, or output paths are untrusted.

Mitigation: Use trusted values for text and file paths, review command inputs before execution, and avoid passing untrusted user-controlled strings into rendering commands.

Risk: Rendering commands may replace existing output files.

Mitigation: Write outputs to a controlled directory, use unique output names, and keep backups of source media and prior exports.

Risk: Documentation may overstate implemented automated editing behavior.

Mitigation: Validate the actual script output on representative sample footage before relying on automated edits in production workflows.

Risk: The package runs local Python and FFmpeg media-processing scripts with third-party dependencies.

Mitigation: Pin and review Python dependencies before team or production use, and run the workflow only on trusted media files.

## Reference(s):

- [Platform Specifications](artifact/references/platform-specs.md)
- [Brand Templates](artifact/references/brand-templates.md)
- [Assets README](artifact/assets/README.md)
- [ClawHub Skill Release](https://clawhub.ai/cogniwatchdev/skills/roblox-clip-transformer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated media-processing files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions and command patterns for local FFmpeg, Whisper, and Python media workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
