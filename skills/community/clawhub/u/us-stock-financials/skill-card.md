## Description: <br>
Fetches comprehensive financial data from SEC EDGAR XBRL for US-listed companies, especially Chinese ADRs, including balance sheet, income statement, cash flow, per-share metrics, and PDF report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mli-cj](https://clawhub.ai/user/mli-cj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to retrieve SEC EDGAR XBRL financial statements for US-listed companies by company name, ticker, alias, or CIK. It supports tabular review, JSON output, and optional PDF report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the network helper silently weakens HTTPS checks if normal secure fetching fails. <br>
Mitigation: Review or patch the network helper before installing; remove the insecure TLS fallback or require an explicit debug opt-in. <br>
Risk: The skill can produce financial data that users may rely on for financial decisions. <br>
Mitigation: Treat outputs as data retrieval results for review, not financial advice; verify material figures against authoritative SEC filings before making decisions. <br>
Risk: The documented PDF dependency installation uses a system-wide pip flag. <br>
Mitigation: Install reportlab in a virtual environment instead of modifying system Python packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mli-cj/us-stock-financials) <br>
- [Built-in issuer aliases](references/issuers.json) <br>
- [SEC EDGAR XBRL API](https://data.sec.gov/api/xbrl) <br>
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, PDF files, shell commands, guidance] <br>
**Output Format:** [Command-line table text, JSON, or generated PDF report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to SEC endpoints; PDF output requires reportlab.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
