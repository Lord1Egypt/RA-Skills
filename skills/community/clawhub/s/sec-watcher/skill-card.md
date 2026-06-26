## Description: <br>
Monitor SEC EDGAR filings for AI and technology companies, summarize filing significance, filter by filing type, and surface high-signal regulatory events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sukanto-m](https://clawhub.ai/user/sukanto-m) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, analysts, and developers use this skill to check recent SEC EDGAR filings for AI and technology companies, inspect form-specific disclosures, and receive plain-English summaries of material events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill mixes real SEC filing results with unsupported promotional intelligence claims that users could mistake for actual analysis. <br>
Mitigation: Treat Signal Report preview, pattern detection, and cross-source analysis language as advertising unless separately verified. <br>
Risk: Company and ticker searches are sent to sec.gov when the fetcher runs. <br>
Mitigation: Use only queries appropriate for public SEC EDGAR lookups and avoid entering confidential watchlists or sensitive research targets. <br>


## Reference(s): <br>
- [SEC Watcher on ClawHub](https://clawhub.ai/sukanto-m/sec-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/sukanto-m) <br>
- [EDGAR Full-Text Search API Reference](references/edgar-api.md) <br>
- [SEC EDGAR full-text search endpoint](https://efts.sec.gov/LATEST/search-index) <br>
- [Signal Report](https://signal-report.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, analysis] <br>
**Output Format:** [Markdown summaries and optional JSON from the fetcher script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; sends company and ticker searches to sec.gov; no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
