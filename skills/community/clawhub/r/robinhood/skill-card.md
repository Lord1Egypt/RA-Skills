## Description:

Registers a Robinhood skill for organizing public financial-services pages, product information, fee rules, help content, and notices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to summarize public Robinhood product, fee, help, security, and announcement information. It is intended for public information organization only, not account access, transaction execution, investment advice, tax advice, or permission bypass.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public financial information may be time-sensitive, region-specific, or superseded by newer Robinhood pages.

Mitigation: Verify dates, regions, fees, terms, and product availability against current official Robinhood pages before relying on the summary.

Risk: Summaries of public financial-services materials could be mistaken for investment, tax, lending, or legal advice.

Mitigation: Present outputs as informational summaries only and avoid recommendations, predictions, transaction guidance, or personalized advice.

Risk: Requests involving account access, balances, identity data, bank details, or private transactions exceed the skill scope.

Mitigation: Restrict use to public pages and decline workflows that require login, private data, account actions, transfers, or trade execution.

## Reference(s):

- [Robinhood Homepage](https://robinhood.com/)
- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/robinhood)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries, tables, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should identify page dates and applicable regions when summarizing time-sensitive financial information.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
