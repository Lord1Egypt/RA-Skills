## Description: <br>
Smart Illustrator helps Claude Code generate article illustrations, slide infographics, and cover images using Gemini, Excalidraw, or Mermaid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axtonliu](https://clawhub.ai/user/axtonliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, newsletter writers, technical bloggers, course instructors, and developers use this skill to turn existing article or slide content into contextual illustrations, diagrams, thumbnails, and Markdown-ready image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected document content or reference images may be sent to external image-generation services. <br>
Mitigation: Avoid using confidential or regulated source material unless external API processing is acceptable for that data. <br>
Risk: Prompt-only and generation flows may copy prompts to the clipboard and leave prompt, configuration, learning, image, or diagram files on disk. <br>
Mitigation: Review generated local artifacts and clipboard contents, and remove sensitive files after use. <br>
Risk: Output quality can vary because the skill depends on model behavior, input structure, and local helper tools. <br>
Mitigation: Review generated images, diagrams, and Markdown before publication, and keep editable Mermaid or Excalidraw sources for correction. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/axtonliu/smart-illustrator) <br>
- [Cover Best Practices](artifact/references/cover-best-practices.md) <br>
- [Excalidraw Guide](artifact/references/excalidraw-guide.md) <br>
- [Excalidraw Export Selectors](artifact/references/excalidraw-export-selectors.md) <br>
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) <br>
- [Gemini API Key Setup](https://aistudio.google.com/apikey) <br>
- [Gemini](https://gemini.google.com/) <br>
- [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli) <br>
- [Bun Runtime](https://bun.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown instructions, JSON prompts, Mermaid or Excalidraw source, shell commands, PNG image files, and Markdown documents with inserted image links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in prompt-only mode, generate or reference image assets, preserve editable diagram source files, and write generated artifacts beside the input document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
