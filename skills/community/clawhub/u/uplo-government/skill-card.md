## Description:

AI-powered government knowledge management. Search policy documents, regulatory filings, public records, and inter-agency coordination data with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Government analysts, policy staff, counsel, budget offices, and program managers use this skill to search agency knowledge, compare policy and regulatory requirements, coordinate audit or rulemaking responses, and prepare grounded briefing materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned runtime package execution can introduce unexpected MCP server behavior during installation or launch.

Mitigation: Pin and review the MCP server package before use, and run it in a controlled environment with minimal filesystem and network access.

Risk: API-token use can expose government knowledge if credentials are over-scoped or mishandled.

Mitigation: Use a least-privilege UPLO token, store it as a secret, rotate it regularly, and limit access to approved users.

Risk: Full organizational exports may include sensitive, pre-decisional, classified, or law-enforcement-sensitive materials.

Mitigation: Restrict export and search access by classification tier, require authorized review for exported context, and follow agency handling rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-government)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline tool calls, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an UPLO instance URL, API key, and the government pack; responses should cite authoritative policy, regulatory, or organizational sources when available.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
