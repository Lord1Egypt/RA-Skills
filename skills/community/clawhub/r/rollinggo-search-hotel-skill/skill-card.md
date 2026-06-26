## Description: <br>
This skill helps agents use the RollingGo CLI to search hotels, filter by destination, dates, stars, budget, tags, and distance, inspect room pricing, and return hotel detail or booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-support agents use this skill to search and compare hotels, inspect real-time room plans and prices, and provide booking or hotel detail links for a selected property. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo_API_KEY that could be exposed if stored broadly or inherited by unrelated processes. <br>
Mitigation: Inject the key per skill when possible, avoid broad shell exports, and ensure sandboxed runs receive only the required credential. <br>
Risk: The skill runs the latest RollingGo package release by default, so behavior can change when the upstream package changes. <br>
Mitigation: Confirm trust in the RollingGo CLI package before installation and re-check command help or pin versions in environments that require repeatable behavior. <br>
Risk: Hotel booking and detail links may lead users toward real transactions or sharing personal information. <br>
Mitigation: Review returned booking links and hotel details before acting on them, and avoid providing unnecessary personal or payment information through the agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-search-hotel-skill) <br>
- [RollingGo publisher profile](https://clawhub.ai/user/rollinggo-ai) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [Claw Host Environment Reference](references/claw-host-env.md) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to run RollingGo commands, parse JSON results, and surface booking URLs or hotel detail links.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
