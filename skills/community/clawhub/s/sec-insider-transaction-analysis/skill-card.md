## Description:

Analyzes reported company insider transactions from Crawlora's live SEC and stored Form 3/4/5 records while preserving filing coverage and interpretation limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to prepare evidence-backed briefs on reported company insider activity by date, transaction code, owner role, and security class, with filing coverage and uncertainty made explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company or search parameters and the Crawlora API key are sent to Crawlora for SEC-data lookups.

Mitigation: Avoid sensitive unrelated query content; keep the API key scoped and rotate it according to Crawlora account practices.

Risk: Bounded results or missing stored history can give an incomplete picture of insider activity.

Mitigation: State retrieval windows and row limits, check filing coverage, and do not treat an empty response as proof of no transactions.

Risk: Reported transaction values and codes can be mistaken for profit, trading intent, or current holdings.

Mitigation: Retain filing context and security scope, label estimated consideration, and avoid inferring intent or future performance.

## Reference(s):

- [Skill release on ClawHub](https://clawhub.ai/crawlora-org/skills/sec-insider-transaction-analysis)
- [SEC insider transaction endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown brief with coverage ledger, classified transaction table, formulas, and caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source links, filing and transaction dates, amendments, duplicate flags, and unknowns; does not authorize trading.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
