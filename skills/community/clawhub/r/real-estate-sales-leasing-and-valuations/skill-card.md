## Description: <br>
Real Estate Sales Leasing and Valuations helps agents look up US property records, estimate property values and rents with comparables, search sale and rental listings, and retrieve aggregated market statistics by zip code through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to retrieve residential real-estate records, valuation and rent estimates, comparable properties, active listings, and zip-code market statistics for authorized property research. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Property addresses, coordinates, and owner-related real-estate details may be sent to AgentPMT for lookup. <br>
Mitigation: Use the skill only for authorized property research, keep inputs to the minimum needed, and avoid logging personal property details. <br>
Risk: Credentials or payment-related secrets could be exposed if included in prompts, logs, or tool inputs. <br>
Mitigation: Use the setup guidance for credential handling and do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/agentpmt/skills/real-estate-sales-leasing-and-valuations) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AgentPMT tool responses are returned as JSON and may include property addresses, coordinates, owner-related data, estimates, comparables, listing details, and market statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
