## Description: <br>
Analyzes retail store traffic and conversion funnels from AIoT customer and behavior data, combining customerFunnel and behaviorFunnel metrics to diagnose traffic and conversion efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail operators and analysts use this skill to inspect store traffic, customer funnel stages, trial behavior, conversion rates, and period-over-period changes. It is intended to support diagnosis of declining traffic, weak trial depth, and reduced intent-to-purchase conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches store business data through an external local API client with unclear credential scope. <br>
Mitigation: Use only in an environment where the API client, account credentials, and accessible store IDs are trusted and understood. <br>
Risk: Running the analysis can expose or process sensitive store traffic and conversion data. <br>
Mitigation: Confirm the requested store ID and date range before execution and restrict results to authorized users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/retail-traffic-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Console text and structured JSON-like analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns funnel metrics, conversion rates, per-customer metrics, and diagnostic findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
