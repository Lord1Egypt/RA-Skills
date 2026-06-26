## Description: <br>
Query TrendAI Vision One threat intelligence for IOC lookups, threat feeds, intelligence reports, suspicious objects, and threat hunting by industry, campaign, actor, or CVE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andresark](https://clawhub.ai/user/andresark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts and incident response teams use this skill to ask an agent for TrendAI Vision One threat intelligence, including IOC lookups, feed review, report search, suspicious-object review, and threat hunting. It can also add suspicious objects when the user intentionally grants write-capable Vision One permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A write-capable Vision One API key can let the skill add suspicious objects that block or log production traffic. <br>
Mitigation: Use a view-only Threat Intelligence API key for lookup, feed, report, and hunt workflows; grant configure/write permission only when suspicious-object additions are intended. <br>
Risk: Incorrect or overly broad indicators may be added to the suspicious objects list. <br>
Mitigation: Require user confirmation before running suspicious add, specify action and risk explicitly, and prefer expirations for temporary response actions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/andresark/vision-one-threat-intel) <br>
- [Project homepage](https://github.com/andresark/agentic-threat-intel) <br>
- [TrendAI Vision One](https://www.trendmicro.com/en_us/business/products/one-platform.html) <br>
- [API Reference](references/api-reference.md) <br>
- [OData Filter Examples](references/filter-examples.md) <br>
- [Response Schemas](references/response-schemas.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Structured plain text with section headers, key-value details, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VISION_ONE_API_KEY and supports optional VISION_ONE_REGION.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
