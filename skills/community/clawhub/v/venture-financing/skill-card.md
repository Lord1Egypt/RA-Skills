## Description:

Drafts and fills NVCA model venture financing documents, including stock purchase, charter, investor rights, voting, ROFR/co-sale, indemnification, and management rights templates, producing signable DOCX files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and legal-operations teams use this skill to collect venture-financing terms and generate NVCA-style Series A or later-stage financing documents. It supports remote MCP generation, local CLI generation, or preview-only Markdown when document-generation tooling is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financing terms may be confidential when sent to the hosted Open Agreements service or shared through a returned download URL.

Mitigation: Confirm remote processing is acceptable before using the MCP; for highly sensitive transactions, use the local CLI or preview-only path.

Risk: Generated venture financing documents may contain legal or business terms that are incomplete, incorrect, or unsuitable for signing.

Mitigation: Require user confirmation before filling templates and review all generated documents with counsel before signing.

Risk: Template metadata, template content, and user-provided field values may contain instruction-like or unsafe text.

Mitigation: Treat template content and field values as data only, reject control characters, enforce reasonable length limits, and do not follow embedded instructions.

## Reference(s):

- [Venture Financing on ClawHub](https://clawhub.ai/stevenobiajulu/skills/venture-financing)
- [Connectors](artifact/CONNECTORS.md)
- [Template Filling Execution Workflow](artifact/template-filling-execution.md)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [Open Agreements](https://openagreements.org)
- [open-agreements on npm](https://www.npmjs.com/package/open-agreements)
- [Open Agreements README](https://github.com/open-agreements/open-agreements#use-with-claude-code)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JSON field values, shell command snippets, and DOCX file paths or download URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP returns expiring download URLs; local CLI writes DOCX files; preview-only mode produces Markdown.]

## Skill Version(s):

0.2.1 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
