## Description:

Draft and fill Y Combinator SAFE templates for valuation-cap, discount, MFN, and pro rata side-letter startup financing documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenobiajulu](https://clawhub.ai/user/stevenobiajulu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, startup operators, and legal-support workflows use this skill to collect SAFE financing terms, choose a YC SAFE template, and generate a signable DOCX or preview for review before signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SAFE field values may include sensitive financing data and can be sent to the hosted Open Agreements service when the remote MCP path is used.

Mitigation: Confirm that hosted processing is acceptable before using the remote MCP path, and offer the local CLI path for sensitive workflows.

Risk: Local CLI usage depends on shell commands, template names, output filenames, and temporary JSON values files.

Mitigation: Use a pinned open-agreements version, validate template names and output filenames, reject control characters and shell metacharacters in values, and use a unique restricted temporary file for each run.

Risk: Generated SAFE documents may affect legal or financing obligations.

Mitigation: Require counsel or other qualified review before signing or relying on generated documents.

## Reference(s):

- [Safe skill page](https://clawhub.ai/stevenobiajulu/skills/safe)
- [Open Agreements](https://openagreements.org)
- [Open Agreements Remote MCP](https://openagreements.org/api/mcp)
- [open-agreements npm package](https://www.npmjs.com/package/open-agreements)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON values, shell commands, DOCX output paths, download URLs, or preview text depending on the available runtime.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP rendering sends SAFE field values to openagreements.org; local CLI rendering requires Node.js 20 or newer and pinned open-agreements installation.]

## Skill Version(s):

0.2.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
