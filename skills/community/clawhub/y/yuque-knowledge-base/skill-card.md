## Description:

Yuque (语雀) knowledge base management for searching, reading, creating, editing, and organizing Yuque documents, repositories, and tables of contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lt5227](https://clawhub.ai/user/lt5227)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to let shell-capable agents search, read, create, update, delete, and organize content in their Yuque knowledge bases through Yuque OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yuque API tokens may be stored in plaintext config.json.

Mitigation: Prefer the YUQUE_TOKEN environment variable, avoid committing config.json, and rotate the token if it is exposed.

Risk: A configurable base_url can receive the Yuque token and document data if changed from the intended service.

Mitigation: Verify base_url remains https://www.yuque.com before running scripts that authenticate or transfer content.

Risk: The skill can delete documents, change visibility, and reorganize table-of-contents nodes without built-in confirmations.

Mitigation: Require manual confirmation for destructive or visibility-changing actions and review target repository, document, and TOC identifiers before execution.

## Reference(s):

- [Yuque OpenAPI v2 Reference](references/api-reference.md)
- [Yuque](https://www.yuque.com)
- [ClawHub skill release page](https://clawhub.ai/lt5227/skills/yuque-knowledge-base)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, Python scripts, configuration JSON, and Yuque API JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yuque API token; scripts use Python standard library and return JSON to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
