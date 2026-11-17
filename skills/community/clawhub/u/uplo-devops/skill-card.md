## Description:

AI-powered DevOps knowledge management. Search runbooks, infrastructure documentation, CI/CD pipelines, and incident response procedures with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, platform engineers, and on-call responders use this skill to search DevOps runbooks, infrastructure documentation, CI/CD procedures, incident history, directives, and knowledge gaps through an UPLO-backed MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server package is installed through an unpinned runtime npm invocation.

Mitigation: Use a pinned or internally mirrored MCP server version before deployment.

Risk: The skill can expose broad organizational context through export capabilities.

Mitigation: Use a narrowly scoped UPLO token, restrict access to full organizational exports, and verify server-side classification, auditing, and redaction controls.

Risk: The skill depends on the configured UPLO service and its npm package source.

Mitigation: Install only after confirming the UPLO service and package source are trusted by the deploying organization.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-devops)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline commands and structured DevOps guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call MCP tools that search organizational knowledge, retrieve directives, flag outdated material, report knowledge gaps, and export organizational context.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
