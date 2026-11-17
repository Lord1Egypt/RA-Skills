## Description:

AI-powered legal knowledge management. Search contracts, compliance requirements, legal cases, and policy documents with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Legal teams and employees use this skill to search organization-specific contracts, compliance materials, legal cases, policy documents, and legal review workflows. It helps agents retrieve source-grounded legal knowledge, identify responsible knowledge owners, and avoid substituting general legal advice for organizational records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive legal knowledge and export broad organizational context.

Mitigation: Review the skill before installing, use a least-privilege UPLO token, and confirm that full organization-context export is approved for the legal data in scope.

Risk: Conversation logging may capture privileged or confidential legal matters.

Mitigation: Require user consent for logging privileged matters or disable conversation logging where legal confidentiality requirements apply.

Risk: The MCP server package install is not pinned in the artifact and receives the API token.

Mitigation: Use a pinned or otherwise verified MCP server package before running the skill with real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-legal)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)
- [Publisher profile](https://clawhub.ai/user/roojenkins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an UPLO instance URL and API key; UPLO-derived answers should cite the relevant source documents.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
