## Description: <br>
Fetch structured financial data and filing metadata from SEC EDGAR and SEC XBRL companyfacts for US-listed companies, especially Chinese issuers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwllu](https://clawhub.ai/user/wangwllu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and financial analysts use this skill to resolve public-company CIKs, retrieve SEC companyfacts, and summarize revenue, net income, EPS, and filing metadata for quarterly or annual analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The HTTPS fallback can make retrieved SEC data less trustworthy if a network connection is intercepted. <br>
Mitigation: Prefer verified HTTPS connections, remove the insecure SSL fallback for sensitive deployments, and verify important results directly against official SEC pages. <br>
Risk: Financial, legal, audit, or compliance-sensitive work can be harmed by stale, incomplete, or misunderstood filing data. <br>
Mitigation: Use the skill output as a lookup aid and confirm material conclusions against official SEC filings before relying on them. <br>


## Reference(s): <br>
- [Issuer reference data](references/issuers.json) <br>
- [SEC XBRL companyfacts API](https://data.sec.gov/api/xbrl) <br>
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar) <br>
- [ClawHub skill page](https://clawhub.ai/wangwllu/sec-finance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown tables or JSON financial data with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries SEC EDGAR and data.sec.gov; important financial, legal, audit, or compliance-sensitive results should be verified against official SEC records.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
