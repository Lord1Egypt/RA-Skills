## Description: <br>
XDesign helps agents turn rough visual requests into HTML decks, prototypes, animations, design systems, and exportable presentation assets using bundled themes, templates, layouts, and animation primitives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, designers, and developers use this skill to create visual deliverables such as slide decks, UI prototypes, landing pages, dashboards, animations, design-system notes, and exportable presentation files from brief or ambiguous prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML, decks, prototypes, and animations may contain incorrect content, misleading emphasis, or unsuitable visual decisions for the intended audience. <br>
Mitigation: Review generated deliverables before sharing, publishing, or using them in business settings. <br>
Risk: Some preview and export paths may use external CDNs, browser storage, popup presenter windows, or optional local tools such as Chrome, Playwright, pandoc, or juice. <br>
Mitigation: Check dependency, privacy, and distribution requirements before public use; prefer reviewed self-contained exports when needed. <br>
Risk: Optional web fetch or GitHub import workflows may introduce external content into generated design systems or deliverables. <br>
Mitigation: Confirm external-source content and licenses before reusing or distributing generated assets. <br>


## Reference(s): <br>
- [XDesign README](README.md) <br>
- [XDesign Skill Instructions](SKILL.md) <br>
- [Mode 2 Prototype Workflow](references/mode-2-prototype.md) <br>
- [Workflow Guide](references/workflow-guide.md) <br>
- [Deck Studio Catalog](references/deck-studio-catalog.md) <br>
- [Deck Studio README](deck-studio/README.md) <br>
- [HTML PPT Studio upstream component](https://github.com/lewislulu/html-ppt-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, shell command, and configuration snippets; generated deliverables may be HTML, PDF, PPTX, PNG, React code, or design-system markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests across presentation, prototype, and animation workflows; some export paths depend on optional browser or command-line tools.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
