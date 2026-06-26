## Description: <br>
Uses the RollingGo CLI to search hotels, filter results, read hotel tags, and fetch room pricing based on destination, dates, star ratings, budget, tags, and distance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamtzlong](https://clawhub.ai/user/dreamtzlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find and compare hotels, retrieve current room and price details, and guide users to booking links using RollingGo data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo API key and sends hotel-search details to the RollingGo service. <br>
Mitigation: Use a dedicated RollingGo API key, keep it in skill-scoped environment configuration, and avoid placing real keys directly in command examples. <br>
Risk: The documented default execution path uses the latest RollingGo package, which can change over time. <br>
Mitigation: Pin or review the RollingGo package when tighter supply-chain control is required. <br>


## Reference(s): <br>
- [RollingGo NPX reference](references/rollinggo-npx.md) <br>
- [RollingGo UV reference](references/rollinggo-uv.md) <br>
- [Claw host environment reference](references/claw-host-env.md) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [ClawHub skill page](https://clawhub.ai/dreamtzlong/rollinggo-hotel-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON] <br>
**Output Format:** [Markdown guidance with CLI command examples and RollingGo JSON or table outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RollingGo_API_KEY and a RollingGo CLI runtime through rollinggo, npx, node, uvx, or uv.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
