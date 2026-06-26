## Description: <br>
Generate, edit, and read PowerPoint presentations with PptxGenJS, XML editing workflows, or markitdown text extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fusuvae-art](https://clawhub.ai/user/fusuvae-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to create new presentation decks, edit existing PPTX files, or extract and review presentation text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JavaScript and PPTX compile steps may affect confidential or important decks if run without review. <br>
Mitigation: Use a sandbox and review generated JavaScript before running compile steps for sensitive presentations. <br>
Risk: Global dependency installs may introduce package trust or environment contamination concerns. <br>
Mitigation: Avoid global installs in sensitive environments unless the packages are trusted; prefer isolated project or sandbox environments. <br>
Risk: Broad presentation-related triggers may activate the skill for general PPT, PPTX, slide, deck, or presentation requests. <br>
Mitigation: Confirm the user wants PowerPoint creation, editing, or inspection before applying the skill to broad presentation tasks. <br>


## Reference(s): <br>
- [PptxGenJS documentation](https://gitbrent.github.io/PptxGenJS/) <br>
- [Microsoft markitdown](https://github.com/microsoft/markitdown) <br>
- [Slide Page Types](references/slide-types.md) <br>
- [Design System](references/design-system.md) <br>
- [Editing Existing Presentations](references/editing.md) <br>
- [QA Process and Common Pitfalls](references/pitfalls.md) <br>
- [PptxGenJS Tutorial](references/pptxgenjs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript/PptxGenJS snippets, XML editing guidance, and generated PPTX or code files when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local slide modules, extracted markdown, editable XML trees, and PPTX outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
