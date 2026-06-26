## Description: <br>
Drafts and fills services agreement templates, including consulting contracts, contractor agreements, statements of work, and professional services agreements, producing signable DOCX files from Common Paper and Bonterms standard forms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and business operators use this skill to choose a standard services agreement template, collect contract fields, and produce a DOCX agreement or preview for legal review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted rendering may receive contract details such as party names, scope, dates, and pricing. <br>
Mitigation: Confirm that sharing agreement values with the hosted Open Agreements service is acceptable, and use the local CLI path for confidential matters. <br>
Risk: Local CLI usage passes user-supplied and template-derived values into shell commands and temporary files. <br>
Mitigation: Enforce the documented filename, template-name, shell metacharacter, control-character, secure temp-file, heredoc quoting, and cleanup rules before rendering. <br>
Risk: Generated agreements may contain incorrect or unsuitable legal terms. <br>
Mitigation: Review the DOCX output with appropriate legal judgment before signing. <br>


## Reference(s): <br>
- [Services Agreement on ClawHub](https://clawhub.ai/stevenobiajulu/services-agreement) <br>
- [Open Agreements](https://openagreements.org) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [open-agreements on npm](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements README](https://github.com/open-agreements/open-agreements#use-with-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON values, shell commands, DOCX file paths, download URLs, or markdown previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote MCP output returns an expiring DOCX download URL; Local CLI output writes a DOCX file; preview mode returns markdown only.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
