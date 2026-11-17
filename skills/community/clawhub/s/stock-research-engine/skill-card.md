## Description:

Generates Chinese-language stock research briefs for A-share, Hong Kong, and U.S. equities when given a ticker, company name, or investment-analysis request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttyyyy8517-ship-it](https://clawhub.ai/user/ttyyyy8517-ship-it)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to produce concise, structured Chinese-language equity research briefs from stock symbols, company names, or stock-analysis prompts. It supports single-name and batch stock analysis across A-share, Hong Kong, and U.S. markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investment analysis output may influence financial decisions.

Mitigation: Treat conclusions as research analysis rather than financial advice, and verify figures, sources, and assumptions before acting.

Risk: The skill relies on current public financial data and may produce stale or incomplete analysis if sources are unavailable or outdated.

Mitigation: Use dated queries, cross-check key figures across sources, and flag older financial data before relying on the brief.

Risk: Broad company or ticker questions may trigger the stock research workflow when the user intended a lighter answer.

Mitigation: Confirm the intended depth of analysis when a prompt is ambiguous or when a full research brief would be disproportionate.

## Reference(s):

- [Stock Research Analysis Framework](references/analysis-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown investment research brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically 2000-4000 Chinese characters, with dated financial data, source freshness checks, and separated facts and opinions.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
