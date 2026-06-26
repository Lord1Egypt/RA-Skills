## Description: <br>
Stock Sector Hunter searches current A-share market information to identify active Shanghai and Shenzhen sectors and leading stocks, with filters for 00 and 60 stock-code prefixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenhulove333](https://clawhub.ai/user/wenhulove333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather same-day A-share sector momentum signals and format leading Shanghai or Shenzhen stocks for review. The output is informational market screening material, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs networked financial lookups and may return incomplete, stale, or misleading market signals. <br>
Mitigation: Treat results as informational screening output only and verify market data with trusted financial sources before acting on it. <br>
Risk: The package requires a search API credential and invokes networked helper tooling. <br>
Mitigation: Install only in an environment where WEB_SEARCH_API_KEY is scoped appropriately and review outbound network behavior before use. <br>
Risk: The release includes auxiliary stock-screening scripts beyond the main documented search workflow. <br>
Mitigation: Review the bundled scripts before running them and avoid granting unnecessary filesystem or credential access. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wenhulove333/stock-sector-hunter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style sector and stock lists with stock codes, signal labels, and an informational-use disclaimer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on live network search or market data availability and a configured WEB_SEARCH_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
