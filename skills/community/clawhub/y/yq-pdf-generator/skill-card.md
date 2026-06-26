## Description: <br>
Provides an HTML-to-PDF export workflow that prepares printable HTML, deploys it to a persistent page, and gives browser print-to-PDF instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn HTML documents, presentations, and URLs into browser-printable pages for PDF export when preserving print styling matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided HTML or URLs may be deployed to a long-lived hosted page without enough consent or scoping. <br>
Mitigation: Use only non-confidential content, confirm publication with the user before deployment, and avoid private URLs, credentials, customer data, or drafts unless an explicit cleanup and access-control process is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-pdf-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, HTML, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and HTML/CSS snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite /workspace/dist/index.html and return a persistent hosted page for browser print-to-PDF.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
