## Description:

Use when the user wants to generate or edit raster images with Gemini through yummycli, including prompt-only generation, single-image editing, and multi-image reference editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yummysource](https://clawhub.ai/user/yummysource)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to turn image-generation or image-editing requests into yummycli Gemini commands, including prompt-only generation, single-image edits, and multi-image reference edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to Gemini through a third-party CLI.

Mitigation: Avoid confidential or regulated images unless approved, and disclose only content appropriate for the configured Gemini account.

Risk: The skill depends on a third-party npm CLI.

Mitigation: Install in a sandboxed environment and review the dependency source and version before use.

Risk: The skill requires GEMINI_API_KEY access.

Mitigation: Expose only the required GEMINI_API_KEY to the execution environment and avoid sharing broader credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yummysource/skills/yummy-gen-image)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yummycli command flags for prompt text, reference images, output path, model, aspect ratio, and image size.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
