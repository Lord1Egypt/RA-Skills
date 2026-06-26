## Description: <br>
Generate and export presentations using Slidev when the user explicitly asks for Slidev, Markdown slides, a previewable slides.md, or PDF/PPTX/HTML export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laofahai](https://clawhub.ai/user/laofahai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and presentation authors use this skill to create visually designed Slidev slide decks from a topic or outline, preview them locally, and export them to HTML, PDF, PPTX, PNG, or Markdown when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup and export workflow can initialize projects and install npm dependencies. <br>
Mitigation: Run the skill in a dedicated Slidev project directory and review dependency installation before allowing it. <br>
Risk: The export wrapper may add Slidev or export dependencies to the current project directory. <br>
Mitigation: Use the export wrapper only from the intended slide project and avoid running it from unrelated repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/laofahai/slidev-ppt-generator) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Presentation Design Reference](references/presentation-design.md) <br>
- [Prompting Reference](references/prompting.md) <br>
- [Tech Share Template](templates/tech-share.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown slide deck files with Slidev frontmatter, inline code blocks, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a Slidev project and produce exported HTML, PDF, PPTX, PNG, or Markdown files when the user requests export.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
