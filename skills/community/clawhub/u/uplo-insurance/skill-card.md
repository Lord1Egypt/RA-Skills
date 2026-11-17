## Description:

AI-powered insurance knowledge management. Search policy documents, claims records, underwriting guidelines, and actuarial data with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance underwriters, claims professionals, compliance analysts, actuarial teams, and product teams use this skill to search organization-specific policy forms, claims records, underwriting guidance, actuarial data, reinsurance terms, and regulatory filings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm MCP server while using a sensitive UPLO token.

Mitigation: Verify and pin the MCP server package version or run an audited local build, use a narrowly scoped token, and run the server in a contained environment.

Risk: Connected insurance datasets may include sensitive claims, actuarial, reinsurance, regulatory, or full organization context.

Mitigation: Connect only authorized datasets and review access controls before enabling exports or broad knowledge searches.

Risk: Coverage, claims, or regulatory answers can be risky if they omit exact source language or jurisdiction context.

Mitigation: Require policy form numbers, edition dates, applicable jurisdictions, and knowledge-owner handoffs for coverage or regulatory questions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/roojenkins/skills/uplo-insurance)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)
- [README.md](artifact/README.md)
- [identity-patch.md](artifact/identity-patch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text responses grounded in UPLO knowledge base search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include policy citations, form numbers, jurisdiction notes, and knowledge-owner handoffs.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
