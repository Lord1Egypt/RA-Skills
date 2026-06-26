## Description: <br>
Draft and fill NVCA model venture financing documents, including stock purchase agreements, certificates of incorporation, investors rights agreements, voting agreements, ROFR and co-sale agreements, indemnification agreements, and management rights letters, to produce signable DOCX files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, legal operators, and finance teams use this skill to collect venture financing details and generate NVCA-based financing document drafts for review. It supports hosted generation, local CLI generation, or a markdown preview when DOCX generation is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agreement details may be sent to the hosted Open Agreements service when the remote MCP path is used. <br>
Mitigation: Decide before installation whether hosted processing is acceptable; use the local CLI or preview path for confidential matters. <br>
Risk: Generated venture financing documents may be incomplete, inaccurate, or unsuitable for a specific transaction. <br>
Mitigation: Review generated agreements with qualified counsel before signing or relying on them. <br>
Risk: Template metadata, template content, and user-provided field values can contain untrusted text. <br>
Mitigation: Treat those values as data, require explicit confirmation before filling templates, reject control characters, and enforce reasonable length limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/stevenobiajulu/venture-financing) <br>
- [Open Agreements](https://openagreements.org) <br>
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp) <br>
- [open-agreements npm Package](https://www.npmjs.com/package/open-agreements) <br>
- [Open Agreements Local CLI README](https://github.com/open-agreements/open-agreements#use-with-claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON field values, DOCX file paths or download URLs, and markdown previews when DOCX generation is unavailable.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated agreements should be reviewed before signing; confidential agreement details should use the local CLI or preview path when hosted processing is not acceptable.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
