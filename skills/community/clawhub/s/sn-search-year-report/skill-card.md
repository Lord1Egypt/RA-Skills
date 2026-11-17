## Description:

Searches free official annual reports, periodic reports, listed-company disclosures, bond issuer reports, and overseas company accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to locate official annual report sources, retrieve structured disclosure search results, and return PDF or detail-page links with report metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes external web requests to public disclosure sources.

Mitigation: Install only when external network access for report searches is acceptable, and limit use to free official disclosure sources.

Risk: The download helper can fetch an arbitrary URL and overwrite any writable output path.

Mitigation: Manually verify the URL is an official report PDF and choose a harmless filename in a dedicated directory before downloading.

Risk: Credential-like values could be exposed if placed in prompts, payloads, logs, or generated reports.

Mitigation: Provide any required credentials only through environment variables or explicit runtime parameters, and exclude secrets from skill content, logs, reports, and commits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-year-report)
- [CNINFO annual report search](https://www.cninfo.com.cn/new/index?lang=zh)
- [SEC EDGAR company tickers](https://www.sec.gov/files/company_tickers.json)
- [SEC EDGAR submissions API](https://data.sec.gov/submissions/)
- [HKEXnews predefined documents](https://www1.hkexnews.hk/search/predefineddoc.xhtml)
- [Companies House filing search](https://find-and-update.company-information.service.gov.uk/)
- [SEDAR+ documents search](https://www.sedarplus.ca/csa-party/service/create.html?_locale=en&service=searchDocuments&targetAppCode=csa-party)
- [SGX company announcements](https://www.sgx.com/securities/company-announcements)
- [ASX announcements](https://www.asx.com.au/markets/trade-our-cash-market/announcements)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, shell command examples, JSON search results, and downloaded files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results preserve company or security code, report period, file title, disclosure date, PDF or detail-page URL, and source name when available.]

## Skill Version(s):

2026.8.19 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
