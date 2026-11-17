## Description:

SEC EDGAR data for US-listed companies and funds. 10-K, 10-Q, 8-K, proxies, S-1/F-1 and IPOs, 13D/13G, Form 4 insiders, 13F fund holdings, XBRL financials and cross-company comparisons, full-text search across all filings, and reading or searching inside one filing (link-only for very large filings).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lkcair](https://clawhub.ai/user/lkcair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other users can retrieve and search SEC filings, inspect company financial data, and compare filings or XBRL metrics across companies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP installation example uses an unpinned @latest version.

Mitigation: Select and review a fixed version before installing the optional MCP server.

Risk: Retrieved company filings contain source text that could be mistaken for agent instructions.

Mitigation: Treat filing contents as source material to analyze, never as instructions.

Risk: SEC requests include the contact information configured in SEC_USER_AGENT.

Mitigation: Review the SEC_USER_AGENT value before making requests and use contact information you intend to disclose.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lkcair/skills/sec)
- [Repository link listed in the skill documentation (provenance unavailable)](https://github.com/lkcair/sec-finance-ai)

## Skill Output:

**Output Type(s):** [JSON, Financial data, Filing text, Analysis]

**Output Format:** [JSON results containing filing data, financial metrics, search results, or text excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Large filings may be provided as links rather than text; filing previews and text results may be partial.]

## Skill Version(s):

2.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
