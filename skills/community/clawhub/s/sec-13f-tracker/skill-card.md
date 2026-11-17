## Description:

Track top fund managers' holdings via SEC 13F filings, compare quarter-over-quarter changes, and generate analysis reports with cross-fund convergence insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reed1898](https://clawhub.ai/user/reed1898)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to fetch SEC EDGAR 13F filings for selected fund managers, compare current and prior quarters, and produce holdings-change reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tracker clears proxy environment variables before making SEC network requests, which can bypass managed or audited network controls.

Mitigation: Require review or removal of the proxy-clearing behavior before managed-network deployment, or gate it behind an explicit opt-in direct-network mode.

Risk: The Python dependency is specified as requests>=2.28.0, allowing future dependency changes at install time.

Mitigation: Pin and review the requests dependency before production or scheduled use.

## Reference(s):

- [SEC EDGAR Company Search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany)
- [SEC submissions endpoint](https://data.sec.gov/submissions/CIK{cik}.json)
- [ClawHub skill page](https://clawhub.ai/reed1898/skills/sec-13f-tracker)
- [Publisher profile](https://clawhub.ai/user/reed1898)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON cache files, terminal status text, and setup or run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates data/ caches and reports/latest.md plus dated 13F report files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
