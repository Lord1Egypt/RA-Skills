## Description: <br>
Flight search and pricing via the RollingGo Flight MCP for comparing real-time flight options by route, date, passenger count, cabin class, and city or airport code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yorkluai-lab](https://clawhub.ai/user/yorkluai-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to resolve city or airport codes and compare one-way or round-trip flight options by price, timing, directness, and value score. The documented capability is flight search only, not booking, payment, cancellation, refund, or order management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight-search details such as origin, destination, travel dates, passenger counts, and cabin class are sent to RollingGo's remote MCP service. <br>
Mitigation: Use the skill only when sharing those details with RollingGo is acceptable, and avoid entering unnecessary personal or sensitive travel information. <br>
Risk: A private API key may be configured for private RollingGo deployments. <br>
Mitigation: Do not add a private API key unless intentionally using a private setup, and manage any credential outside skill text or chat transcripts. <br>
Risk: Search results may look transactional even though the skill does not support booking or payment. <br>
Mitigation: Treat results as informational, recheck price and inventory before purchase, and use separate booking channels for ticket issuance or changes. <br>


## Reference(s): <br>
- [RollingGo MCP Reference](references/rollinggo-mcp.md) <br>
- [RollingGo Homepage](https://rollinggo.store) <br>
- [RollingGo Flight MCP Endpoint](https://mcp.rollinggo.cn/mcp/flight) <br>
- [ClawHub Skill Page](https://clawhub.ai/yorkluai-lab/rollinggo-searchflight-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown flight-option summaries with MCP configuration details and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight prices and inventory are real-time and should be rechecked before booking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
