## Description:

AI-powered accounting knowledge management. Search bookkeeping records, tax preparation documents, audit support files, and financial statement workpapers with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill to search organizational bookkeeping, tax, audit, reconciliation, and financial statement workpaper knowledge through UPLO. It helps agents retrieve grounded accounting context, cite source records, identify knowledge owners, and avoid guessing when the knowledge base lacks an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive financial and tax records, including searched content, exported organization context, and logged conversations.

Mitigation: Install only for an approved UPLO tenant, use a narrowly scoped token, and treat searched, exported, and logged accounting content as confidential.

Risk: Bulk export and session logging can create retention, redaction, audit, and access-control exposure.

Mitigation: Avoid export_org_context and conversation logging unless the organization has approved retention, redaction, audit, and access controls.

Risk: The MCP server is launched through an unpinned npx runtime, which can introduce mutable runtime code.

Mitigation: Prefer a pinned and reviewed MCP server version before deployment.

Risk: Accounting answers may be incomplete or misleading when the UPLO knowledge base lacks current source material.

Mitigation: Cite source documents, label estimates versus actuals, and say when UPLO does not contain the answer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-accounting)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses should cite retrieved UPLO sources and respect classification levels for financial and tax records.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
