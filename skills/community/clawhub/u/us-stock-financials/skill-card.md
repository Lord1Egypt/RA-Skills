## Description:

Fetch comprehensive financial data from SEC EDGAR XBRL for US-listed companies, especially Chinese ADRs, including balance sheet, income statement, cash flow, per-share metrics, and PDF report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mli-cj](https://clawhub.ai/user/mli-cj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and finance-oriented users can retrieve SEC EDGAR XBRL financial statement data for supported US-listed companies and generate table, JSON, or PDF reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial figures could be spoofed on an intercepted network when HTTPS verification falls back to an insecure mode.

Mitigation: Use only on trusted networks, compare material outputs against SEC EDGAR, and prefer a version that removes the TLS bypass before relying on reports.

Risk: The dependency guidance recommends a system-level install pattern that can alter the Python environment.

Mitigation: Install reportlab and any related packages in a virtual environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mli-cj/skills/us-stock-financials)
- [SEC XBRL API](https://data.sec.gov/api/xbrl)
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar)
- [Built-in issuer reference](references/issuers.json)

## Skill Output:

**Output Type(s):** [text, json, files, shell commands, guidance]

**Output Format:** [Plain text tables, JSON, and optional PDF reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch live SEC EDGAR data and may write a PDF report to a user-specified path.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
