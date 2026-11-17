## Description:

AI-powered environmental knowledge management. Search impact assessments, compliance monitoring data, sustainability reports, and environmental permits with structured extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Environmental, sustainability, compliance, legal, and project teams use this skill to query organizational environmental records, permit conditions, monitoring results, emissions inventories, remediation status, and ESG metrics through UPLO-backed knowledge tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts an unpinned external MCP package that receives a secret API key.

Mitigation: Use a narrowly scoped UPLO token, confirm the package source is approved by your organization, and prefer a pinned, reviewed package version.

Risk: The skill can expose broad organizational environmental context, including classified or restricted records.

Mitigation: Restrict bulk context export and high-sensitivity environmental records to authorized users and appropriate data classifications.

Risk: Environmental and compliance records can become stale or depend on current permits, monitoring periods, and regulatory thresholds.

Mitigation: Require responses to include source record dates, permit identifiers, compliance periods, and stale-record flags when relevant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roojenkins/skills/uplo-environmental)
- [UPLO](https://uplo.ai)
- [UPLO schemas](https://uplo.ai/schemas)
- [UPLO Sustainability related skill](https://clawhub.com/skills/uplo-sustainability)
- [UPLO Agriculture related skill](https://clawhub.com/skills/uplo-agriculture)
- [UPLO Compliance related skill](https://clawhub.com/skills/uplo-compliance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with MCP tool calls, search guidance, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured UPLO MCP access and organization-specific environmental knowledge; responses should cite records, dates, permit identifiers, regulatory programs, and compliance periods when available.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
