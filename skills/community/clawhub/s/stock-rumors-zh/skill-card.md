## Description: <br>
Scans AISA for market-rumor signals related to M&A, insider activity, analyst actions, social media, and regulatory events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents supporting market intelligence workflows use this skill to request AISA scans for recent rumor and early-signal categories, then rank signals by potential impact. The output is informational and should be independently verified before any trading or business decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns rumor and early-signal analysis that may be unconfirmed or misleading. <br>
Mitigation: Treat results as informational only and independently verify sources before acting on them. <br>
Risk: The skill sends prompts to an external AISA-compatible API using an API key. <br>
Mitigation: Use a dedicated AISA_API_KEY and avoid submitting private trading strategies, personal financial details, or other sensitive data. <br>
Risk: Changing the AISA_BASE_URL can redirect requests to a different endpoint. <br>
Mitigation: Leave AISA_BASE_URL unset unless the alternate endpoint is intentionally configured and trusted. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/aisadocs/stock-rumors-zh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown market-rumor report with an optional appended JSON summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and Python 3; supports focus filters for all, M&A, insider, analyst, or social signals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
