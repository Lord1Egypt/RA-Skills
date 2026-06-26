## Description: <br>
Converts Xiaohongshu-style Markdown copy into vertical HTML card pages with template-based or optional LLM-assisted generation and browser PNG export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverfor](https://clawhub.ai/user/riverfor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operators use this skill to turn Markdown drafts into Xiaohongshu-style HTML card sets and export them as PNG images for publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional LLM mode can send Markdown content to the configured external model provider. <br>
Mitigation: Do not use LLM mode with private drafts, business notes, regulated data, or other sensitive content unless the configured provider and endpoint are approved. <br>
Risk: Generated HTML depends on a remote html2canvas CDN script to download PNG images. <br>
Mitigation: Review and approve the CDN dependency before use, or vendor a trusted local copy when offline or controlled execution is required. <br>
Risk: The security verdict is suspicious because AI-mode disclosure is not clear in the main instructions. <br>
Mitigation: Review the scripts before installing and document when data leaves the local environment. <br>


## Reference(s): <br>
- [Xiaohongshu Card Creator on ClawHub](https://clawhub.ai/riverfor/xiaohongshu-card-creator) <br>
- [html2canvas CDN runtime dependency](https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, PNG images, Shell commands, Configuration] <br>
**Output Format:** [Generated HTML page with browser-exported PNG card images and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default local generation uses templates; optional LLM mode requires provider configuration and an API key.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
