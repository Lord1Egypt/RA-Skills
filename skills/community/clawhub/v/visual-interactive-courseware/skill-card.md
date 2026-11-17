## Description:

Creates Chinese-language, single-file interactive HTML courseware with SVG visualizations, teaching notes, and optional 3D content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Educators and courseware creators use this skill to turn curriculum topics into offline interactive lessons, knowledge summaries, and teacher guidance. An optional 3D workflow adds interactive models or rendered media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes instructions to remove watermarks from generated images.

Mitigation: Do not remove watermarks; use licensed, watermark-free assets or regenerate compliant images.

Risk: The optional 3D path may inspect local configuration, execute Blender, ffmpeg, or Node, and use external models.

Mitigation: Use the 3D path only with approval for local checks, tool execution, and vetted third-party assets.

Risk: An optional external model workflow may involve a BlenderKit API key.

Mitigation: Protect the key from generated files and logs, and review any access to third-party services.

Risk: Generated educational diagrams and explanations can be inaccurate.

Mitigation: Check subject facts against authoritative teaching materials and review diagrams before classroom use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/erich1566/skills/visual-interactive-courseware)
- [Courseware workflow](references/workflow.md)
- [Design guide](references/design-guide.md)
- [Audience matrix](references/audience-matrix.md)
- [Subject examples](references/subject-examples.md)
- [Optional Blender and 3D workflow](references/3d-blender-pipeline.md)
- [Blender downloads](https://www.blender.org/download/)
- [Blender MCP project](https://projects.blender.org/lab/blender_mcp)

## Skill Output:

**Output Type(s):** [HTML, Markdown, Code, Guidance]

**Output Format:** [Self-contained interactive HTML lesson with Markdown knowledge summary and teacher notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional embedded 3D models, simulations, and rendered media]

## Skill Version(s):

1.2.2 (source: server-resolved ClawHub release; skill frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
