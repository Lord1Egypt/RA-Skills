## Description:

Check whether a Brazilian company is active and has public sanctions or federal tax debt. Use prepared records, then live checks, supplier batches or change monitoring when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrpbr](https://clawhub.ai/user/wrpbr)

### License/Terms of Use:

MIT-0

## Use Case:

External users, procurement teams, and analysts use this skill to check Brazilian company registration status, public sanctions, federal tax debt, and supplier changes. It helps them choose prepared records or targeted live checks and report evidence, dates, and unknowns for individual or batch reviews.

### Deployment Geography for Use:

Brazil

## Known Risks and Mitigations:

Risk: Supplier identifiers or internal notes may be disclosed to Radar CNPJ.

Mitigation: Share identifiers only when organizational policy permits it, and exclude internal notes.

Risk: Paid reports or monitoring may create spending or ongoing coverage obligations.

Mitigation: Check available free records and existing access, set an authorized spending limit, and verify monitoring duration and cancellation options.

Risk: The remote service's implementation and data retention were not verified during review.

Mitigation: Limit submitted information to what the check requires and follow organizational data-sharing rules.

## Reference(s):

- [Radar CNPJ MCP server](https://radar-cnpj.com/mcp)
- [Company lookup API](https://radar-cnpj.com/api/cnpj/{cnpj}?temas=dados,sancoes,divida)
- [Current pricing](https://radar-cnpj.com/api/pricing)
- [Payment terms](https://radar-cnpj.com/api/billing)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Evidence-based company screening summaries and tables, with JSON or CSV records when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source and reference dates, and distinguishes unchecked data from checked blocks with no records.]

## Skill Version(s):

1.0.11 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
