## Description: <br>
MiniMax PDF creates, fills, and reformats visually polished PDFs using a token-based design system and a print-ready rendering pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to generate polished reports, proposals, resumes, portfolios, and similar PDFs, fill existing PDF form fields, or reformat existing Markdown, text, PDF, or JSON documents into a designed PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency repair path can install Python packages, Playwright, and Chromium into the execution environment. <br>
Mitigation: Run the skill in an isolated virtual environment or container and preinstall reviewed dependencies instead of using the auto-fix path on a system Python. <br>
Risk: Cover rendering can fetch remote fonts or cover images and can render local image paths. <br>
Mitigation: Use reviewed local assets, avoid confidential local paths, and disable or control network access unless remote rendering is acceptable. <br>


## Reference(s): <br>
- [MiniMax PDF README](README.md) <br>
- [MiniMax PDF Design System](design/design.md) <br>
- [ClawHub Release Page](https://clawhub.ai/yhlorra/yh-minimax-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PDF files with supporting JSON, HTML, and Markdown or shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce generated PDFs, filled PDFs, reformatted PDFs, content.json, tokens.json, cover HTML, and QA output depending on the selected route.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
