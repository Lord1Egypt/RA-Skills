## Description:

Use when the user wants to generate a video with Gemini Veo through yummycli, including text-to-video, image-to-video (single starting frame), and reference-image-guided generation (up to 3 images).

This skill is ready for commercial/non-commercial use.

## Publisher:

[yummysource](https://clawhub.ai/user/yummysource)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to translate text-to-video, image-to-video, and reference-guided video requests into validated Gemini Veo commands through yummycli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party executable CLI.

Mitigation: Install only a trusted, pinned, and reviewed version of @yummysource/yummycli.

Risk: Shell-style command templates can be unsafe if prompts or file paths are assembled into command strings.

Mitigation: Pass prompts and file paths as literal CLI arguments and expose only the required GEMINI_API_KEY.

Risk: Generated video commands can fail when model, duration, resolution, image count, or output path constraints are invalid.

Mitigation: Validate model compatibility, duration, resolution, image count, and .mp4 output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yummysource/skills/yummy-gen-video)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require yummycli, GEMINI_API_KEY, and the related yummy-shared skill.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
