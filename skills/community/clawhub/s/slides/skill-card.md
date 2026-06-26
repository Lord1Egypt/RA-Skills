## Description: <br>
Create, edit, and automate presentations with programmatic tools, visual consistency, and project-based learning of user style preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, creators, consultants, educators, and developers use this skill to create, edit, automate, and validate presentation decks across PowerPoint, Google Slides, and web-based slide formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update local presentation memory, style guides, templates, and project notes under ~/slides/. <br>
Mitigation: Review the contents of ~/slides/ periodically and avoid storing secrets or sensitive credentials in those files. <br>
Risk: Optional slide tooling or npm/npx-based workflows may install or execute third-party packages. <br>
Mitigation: Review requested package installs before running them and use trusted package sources. <br>
Risk: Google Slides automation can require credentials. <br>
Mitigation: Use a dedicated least-privilege Google credential only when cloud slide automation is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/slides) <br>
- [Programmatic Slide Tools](artifact/tools.md) <br>
- [Visual Design Rules for Slides](artifact/design.md) <br>
- [Deck Structures by Type](artifact/formats.md) <br>
- [Memory Setup - Slides](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with code blocks, configuration snippets, and generated or edited presentation files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local slide memory, style guides, project notes, templates, and deck versions under ~/slides/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
