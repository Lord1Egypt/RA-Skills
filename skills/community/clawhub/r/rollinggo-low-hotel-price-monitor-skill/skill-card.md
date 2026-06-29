## Description: <br>
A RollingGo hotel price monitoring, search, and booking-guidance skill that helps an agent compare current hotel rates, evaluate cancellation flexibility, recommend hotels to watch, and hand off structured price-watch requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
For travel-planning agents that need to help users monitor hotel prices, assess whether an existing booking is worth watching, search and narrow hotel options, explain cancellation and price context, and produce a host-agent-ready hotel price watch request after the user chooses a specific hotel. <br>

### Deployment Geography for Use: <br>
Global, subject to RollingGo service availability and any local travel, privacy, and booking rules that apply to the user and destination. <br>

## Known Risks and Mitigations: <br>
Risk: RollingGo API key exposure through commands, logs, or shared transcripts. <br>
Mitigation: Set RollingGo_API_KEY as an environment variable and avoid placing the key directly in reusable commands or user-visible output. <br>
Risk: Hotel searches and watch lists may reveal travel dates, destinations, booking context, and notification preferences to the RollingGo CLI/service or host agent. <br>
Mitigation: Use the skill only for hotels the user explicitly wants monitored, and avoid retaining watch state beyond the host agent's required reminder workflow. <br>
Risk: A price-watch recommendation could be mistaken for a guaranteed future discount or a completed booking action. <br>
Mitigation: Present current price and cancellation information as guidance only, avoid promises about future prices, and provide booking links for the user to complete directly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-low-hotel-price-monitor-skill) <br>
- [RollingGo publisher profile](https://clawhub.ai/user/rollinggo-ai) <br>
- [RollingGo homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance, Markdown recommendation tables, RollingGo CLI command guidance, and structured JSON handoff objects for hotel price-watch creation.] <br>
**Output Parameters:** [Hotel name or ID, city or area, check-in and check-out dates, stay length, guest and room counts, room type, booked price, current price, currency, cancellation deadline, booking platform, notification preference, watch reason, trigger rule, and missing-field notes when known.] <br>
**Other Properties Related to Output:** [Requires RollingGo_API_KEY and a RollingGo-capable runtime such as rollinggo, npx/node, or uvx/uv. The skill does not book hotels directly; the host agent handles state storage, recurring checks, price comparison, reminders, and cross-session continuity. Unknown fields are represented as null in the handoff JSON.] <br>

## Skill Version(s): <br>
1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
