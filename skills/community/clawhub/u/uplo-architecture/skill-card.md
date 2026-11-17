## Description:

AI-powered architecture knowledge management. Search building designs, code compliance records, project specifications, and BIM data with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Architecture teams and their agents use this skill to query UPLO-backed organizational knowledge for building designs, code compliance records, project specifications, BIM metadata, directives, and subject-matter experts. It is intended for grounded lookup, context-aware analysis, citation-backed answers, and conversation logging against an approved UPLO instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server package.

Mitigation: Use a pinned or administrator-approved MCP server package before deploying with sensitive organizational data.

Risk: The skill can export or log organizational context to a remote UPLO service.

Mitigation: Install only with a trusted UPLO instance and avoid confidential conversations unless logging is approved.

Risk: The skill requires an API token for the UPLO MCP server.

Mitigation: Use a narrowly scoped, revocable API token and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-architecture)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should cite UPLO sources, respect classification tiers, and avoid fabricating answers when the knowledge base lacks support.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
