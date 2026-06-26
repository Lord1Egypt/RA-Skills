## Description: <br>
Evaluate tennis vacation destinations with structured scoring across transportation, accommodation, weather, and court facilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edam17](https://clawhub.ai/user/edam17) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to compare tennis vacation destinations, court options, travel logistics, lodging, weather, and budget tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel and social links may be inaccessible or incomplete, which can lead to unsupported destination details. <br>
Mitigation: Extract destination details from user-provided text first, treat links as supplementary, ask for pasted details when needed, and label missing information clearly. <br>
Risk: Flight prices from web search or the optional flight-price CLI can be stale, one-time, or confused with ongoing monitoring. <br>
Mitigation: Label flight-price sources, never invent prices, ask before using optional CLI checks, and state that the skill does not create automatic background monitoring. <br>


## Reference(s): <br>
- [Tennis Vacation Rater on ClawHub](https://clawhub.ai/edam17/tennis-vacation-rater) <br>
- [Tennis Destinations Database](references/destinations.md) <br>
- [Scoring Dimension Details](references/dimension-details.md) <br>
- [Price Monitoring Guide](references/price-monitoring-guide.md) <br>
- [Report Template](references/report-template.md) <br>
- [Link Handling Guide](references/link-handling-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown report with scores, source labels, budget estimates, and price-query advice] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses source labels for flight prices and marks unavailable travel data as needing follow-up.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
