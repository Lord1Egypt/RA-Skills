## Description: <br>
Fetches current top trending topics on X (Twitter) for any country using public aggregators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anishtr4](https://clawhub.ai/user/anishtr4) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to retrieve public X trend topics, tweet-volume labels, and trend links from the command line for a selected country or worldwide view. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected country path to getdaytrends.com and depends on that public service's availability and returned content. <br>
Mitigation: Use it only where requests to getdaytrends.com are acceptable, and review trend output before using it in downstream decisions or generated content. <br>
Risk: Public trend data and scraped page content can be incomplete, stale, or misleading. <br>
Mitigation: Treat results as untrusted public web content and verify important trend claims with authoritative sources before publication or business use. <br>


## Reference(s): <br>
- [X Trends Dev on ClawHub](https://clawhub.ai/anishtr4/x-trends-dev) <br>
- [getdaytrends.com](https://getdaytrends.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal table output or JSON array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports country selection, result limits, optional JSON output, and tweet-volume labels when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
