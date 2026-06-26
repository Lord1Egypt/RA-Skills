## Description: <br>
Uses browser automation to fetch real-time A-share market data from Eastmoney and Sina Finance, including major indices, northbound capital flow, market breadth, and limit-up/limit-down counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading teams use this skill to collect A-share market snapshots for quantitative research, portfolio monitoring, financial analysis, and market sentiment tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-driven collection may bypass anti-scraping protections on financial websites without clear authorization or safety limits. <br>
Mitigation: Install only when authorized to automate the listed sources; prefer official or licensed market-data APIs, source allowlists, explicit user control, and rate limits. <br>
Risk: Market data from website pages may be delayed, incomplete, or affected by source layout changes. <br>
Mitigation: Validate outputs against authoritative market-data sources before using them for analysis, monitoring, or trading workflows. <br>


## Reference(s): <br>
- [Stock Browser Fetcher on ClawHub](https://clawhub.ai/linbo405/stock-browser-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Data] <br>
**Output Format:** [Structured JSON market snapshot] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes date, Shanghai/Shenzhen/ChiNext index values, northbound flow, advancing and declining counts, and limit-up/limit-down counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
