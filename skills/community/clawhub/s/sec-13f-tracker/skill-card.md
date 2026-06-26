## Description: <br>
Track top fund managers' holdings via SEC 13F filings. Fetches quarterly filings from SEC EDGAR, compares quarter-over-quarter changes (new positions, increases, decreases, exits), and generates analysis reports with cross-fund convergence insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to monitor selected institutional investors' public 13F filings, compare quarter-over-quarter position changes, and identify cross-fund convergence in holdings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tracker clears common HTTP and HTTPS proxy environment variables before contacting SEC EDGAR. <br>
Mitigation: Review whether direct outbound SEC EDGAR access is acceptable for the deployment network, or modify the script before use in environments that require enforced proxies. <br>
Risk: Cron or channel posting can make SEC report generation recurring and visible to others. <br>
Mitigation: Enable scheduled runs and channel delivery only when intentional, and review recipients and posting cadence before deployment. <br>
Risk: The skill writes local holdings caches and Markdown reports. <br>
Mitigation: Run in an isolated virtual environment or workspace and review generated data/ and reports/ content before sharing or retaining it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reed1898/sec-13f-tracker) <br>
- [SEC EDGAR company search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany) <br>
- [SEC submissions endpoint used by tracker](https://data.sec.gov/submissions/CIK{cik}.json) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration] <br>
**Output Format:** [Markdown reports, JSON cache files, and setup/run command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes cached holdings under data/ and dated plus latest reports under reports/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
