## Description: <br>
Order temporary event staff for events in US and Canadian markets through TempGuru, including requirement gathering, coverage, rate and compliance lookups, budget planning, and confirmed quote request submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kissmyabs32](https://clawhub.ai/user/kissmyabs32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and event planners use this skill to plan temporary W-2 staffing for conventions, trade shows, festivals, concerts, sporting events, corporate gatherings, brand activations, and multi-city programs. It helps gather event details, estimate rates, check availability and compliance, and submit a human-reviewed quote request after user confirmation. <br>

### Deployment Geography for Use: <br>
United States and Canada <br>

## Known Risks and Mitigations: <br>
Risk: Quote submission may send contact, company, event, role, headcount, and scheduling details to TempGuru for follow-up. <br>
Mitigation: Confirm the user intends to create a quote or lead before submission, and send only the information needed for the staffing request. <br>
Risk: Planning rate ranges or lead-time guidance could be mistaken for a final quote, reservation, or availability guarantee. <br>
Mitigation: Label estimates clearly, state that final pricing and availability come from TempGuru review, and submit a quote request only after user confirmation. <br>


## Reference(s): <br>
- [TempGuru MCP endpoint](https://mcp.tempguru.co/mcp) <br>
- [TempGuru machine-readable site overview](https://tempguru.co/llms.txt) <br>
- [TempGuru city staffing guides](https://tempguru.co/insights/{city}-event-staffing) <br>
- [TempGuru role staffing guides](https://tempguru.co/insights/{roles}-in-{city}) <br>
- [ClawHub skill page](https://clawhub.ai/kissmyabs32/skills/tempguru-event-staffing-ordering) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with structured staffing plans, rate ranges, compliance notes, and quote-request confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a TempGuru MCP server for coverage, pricing, availability, compliance, benchmarks, and opt-in quote submission.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
