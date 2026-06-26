## Description: <br>
Integrated travel planner combining FlyAI ticket prices, Gaode and Tencent map POI, Meituan food recommendations, and fallback McDonald's options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to assemble travel plans with ticket pricing, map and POI checks, route comparisons, food recommendations, and fallback dining options. It is intended for travel planning prompts such as trip planning, ticket booking, and food discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe local command execution paths may affect the host machine. <br>
Mitigation: Install only in an isolated environment and review or remove shell=True command paths before use. <br>
Risk: Embedded or exposed API keys may be present. <br>
Mitigation: Rotate and remove embedded keys, then provide credentials through environment variables or a managed secret store. <br>
Risk: Watchdog, deployment, status, or debug endpoints may expose controls or operational details. <br>
Mitigation: Delete or gate watchdog and deployment scripts behind explicit operator control, and clean up status or debug endpoints before public exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timo2026/travel-swarm) <br>
- [Publisher profile](https://clawhub.ai/user/timo2026) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or HTML travel plans with setup guidance for required API keys] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include map screenshots, food recommendations, POI comparisons, and ticket price details when external APIs are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
