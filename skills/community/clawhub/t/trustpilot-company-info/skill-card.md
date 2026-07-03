## Description: <br>
Looks up public Trustpilot company profiles by domain and returns profile metadata including TrustScore, review counts, categories, verification status, contact fields, and optional reply behavior metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to enrich company domains with public Trustpilot reputation and profile data for lead-list enrichment, supplier vetting, brand monitoring, competitor comparison, and due-diligence workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence says the skill encourages bypassing Trustpilot anti-bot controls and scaling collection across stealth sessions. <br>
Mitigation: Use only for authorized, low-volume lookups that respect Trustpilot site limits and terms; do not use stealth, proxy, or multi-fingerprint scaling guidance. <br>
Risk: Trustpilot profile data can be incomplete or change over time. <br>
Mitigation: Treat the returned scrapedDateTime as part of the result and refresh data before making material decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/trustpilot-company-info) <br>
- [Trustpilot review page pattern](https://www.trustpilot.com/review/{domain}) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON objects with browser navigation and eval command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional response metrics flag expands the returned JSON fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
