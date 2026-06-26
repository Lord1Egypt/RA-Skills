## Description: <br>
RollingGo Hotel Search helps agents search hotels, filter candidates, inspect hotel details and room pricing, and look up hotel tags through the RollingGo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnChenKai](https://clawhub.ai/user/cnChenKai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to search hotel candidates by destination, dates, budget, stars, tags, and distance, then inspect current room plans, pricing, cancellation details, and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external RollingGo CLI package. <br>
Mitigation: Install only if comfortable with that external package, and consider pinning or reviewing the CLI version for production use instead of always using latest. <br>
Risk: Hotel-search details are sent to the RollingGo provider. <br>
Mitigation: Avoid sensitive travel details unless the user accepts provider processing for the search. <br>
Risk: The artifact includes a shared public API key. <br>
Mitigation: Use a dedicated RollingGo API key for production or sensitive searches, and store it in an environment variable rather than command lines where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnChenKai/rollinggo-searchhotel-skill) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [RollingGo API Key Configuration](references/env.md) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The RollingGo CLI returns result payloads on stdout, JSON by default, with errors on stderr and documented exit codes for network or validation failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
