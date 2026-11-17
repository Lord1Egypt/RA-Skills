## Description:

Smart Illustrator helps an agent analyze articles, slide scripts, or cover topics and produce contextual illustration prompts, diagram source, image-generation commands, and markdown outputs for article images, presentation infographics, and social cover images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axtonliu](https://clawhub.ai/user/axtonliu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, technical writers, course instructors, and developers use this skill to turn article or lesson content into illustration plans, batch infographic prompts, cover concepts, and markdown files with image references. It is suited to blog posts, newsletters, presentation B-roll, course visuals, and platform-specific thumbnails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article text, prompts, and reference material may be sent to Gemini or pasted into Gemini Web during image generation.

Mitigation: Use non-sensitive content unless the user has approved sharing it with the external image-generation service.

Risk: The evidence security review flags unpinned external scripts and dependencies, plus shell and temporary-file patterns that should not be executed blindly.

Mitigation: Inspect and pin external scripts and dependencies before use, review generated commands, and adapt temporary-file handling to the local environment.

Risk: Generated outputs may carry Axton branding or watermark assumptions from the bundled style guidance.

Mitigation: Remove or customize the branding before using generated images in commercial materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axtonliu/skills/smart-illustrator)
- [Smart Illustrator README](artifact/README.md)
- [Cover Best Practices](artifact/references/cover-best-practices.md)
- [Excalidraw JSON Guide](artifact/references/excalidraw-guide.md)
- [Excalidraw Export Selectors](artifact/references/excalidraw-export-selectors.md)
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Mermaid documentation](https://mermaid.js.org/)
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli)
- [Excalidraw](https://excalidraw.com/)
- [Gemini API](https://ai.google.dev/)
- [Bun](https://bun.sh/)
- [Playwright](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON prompts, Mermaid or Excalidraw source snippets, shell commands, configuration examples, and image file references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or reference PNG images, editable diagram source files, copied JSON prompts, and article markdown with inserted image links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
