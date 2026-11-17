## Description:

天机我要查 (免费版) (TianJi-Open) is an enterprise public-information aggregation and due-diligence assistant that uses public web searches to produce sourced, time-stamped structured reports across business registration, ownership, operating risk, financing, news, bidding, qualifications, and intellectual property.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and business teams use this skill to collect public company information for investment due diligence, commercial counterparty checks, competitor research, industry research, and preliminary risk screening. It is intended for public-source aggregation and initial assessment, not as a substitute for legal, financial, or regulatory due diligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional accelerator can execute a locally installed baidu-search dependency with the user's privileges.

Mitigation: Prefer the built-in web-search workflow unless baidu-search has been independently installed from a trusted source and reviewed at the configured path.

Risk: Company due-diligence reports may contain outdated, incomplete, or misleading public records.

Mitigation: Require source links, credibility labels, event dates, and official-channel verification for high-risk conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chesaram/skills/tianji-open-1-0-0)
- [Search Tips](references/search-tips.md)
- [Authoritative Sources](references/sources.md)
- [Industry and Bidding Templates](references/industry-bidding-templates.md)
- [Demo Report](references/demo-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown structured report with source links, credibility labels, timestamps, and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are based on public information and include verification reminders for high-risk findings.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
