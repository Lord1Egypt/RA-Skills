## Description: <br>
A Chinese-language hotel price monitoring and booking guidance skill that helps users compare current hotel prices, search candidate hotels, and prepare structured hotel price watch requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to decide whether an existing hotel booking is worth monitoring, compare candidate hotels for a planned trip, and hand off confirmed hotel price watch details to host agent scheduling or reminder tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a third-party RollingGo CLI and API key and may share hotel names, dates, occupancy, preferences, and existing booking prices with that provider and the host agent. <br>
Mitigation: Install only when the publisher is trusted, share the minimum travel and booking details needed for the task, and review provider handling of hotel search and watch data. <br>
Risk: API keys can be exposed if they are pasted into commands, logs, or chat transcripts. <br>
Mitigation: Prefer setting RollingGo_API_KEY as an environment variable, avoid passing secrets directly in command text, and rotate the key if exposure is suspected. <br>
Risk: Ongoing hotel price watches may create persistent reminders or stored watch details outside the skill itself. <br>
Mitigation: Confirm the host agent's scheduling, storage, notification, stop, and deletion behavior before creating a persistent watch. <br>
Risk: Hotel price, availability, cancellation policy, and booking-link information can change and should not be treated as a guaranteed lowest price or booking commitment. <br>
Mitigation: Use current RollingGo query results, avoid price guarantees, and have the user verify cancellation terms and booking details before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-hotel-price-monitor-skill) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with tables, inline shell commands, and structured JSON handoff objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce hotel recommendations, price-monitoring summaries, RollingGo CLI command guidance, and ready-for-host-agent watch request payloads.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
