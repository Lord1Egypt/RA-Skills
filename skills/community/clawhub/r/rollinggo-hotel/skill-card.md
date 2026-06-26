## Description: <br>
Hotel search and pricing via the RollingGo CLI for destination-based hotel discovery, filtering, hotel details, room pricing, and hotel tag lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamtzlong](https://clawhub.ai/user/dreamtzlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search hotels, compare current room details and pricing, inspect valid hotel tags, and prepare booking links through the RollingGo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RollingGo API key and can handle hotel search details. <br>
Mitigation: Use per-skill secret injection, avoid placing real keys directly on command lines, and install only if RollingGo is trusted with those details. <br>
Risk: The runtime guidance installs or executes rollinggo@latest by default. <br>
Mitigation: Pin a reviewed RollingGo CLI version in sensitive environments instead of always resolving the latest package. <br>


## Reference(s): <br>
- [RollingGo Hotel page](https://clawhub.ai/dreamtzlong/rollinggo-hotel) <br>
- [RollingGo service homepage](https://mcp.agentichotel.cn) <br>
- [RollingGo API key application](https://mcp.agentichotel.cn/apply) <br>
- [RollingGo NPX Reference](references/rollinggo-npx.md) <br>
- [RollingGo UV Reference](references/rollinggo-uv.md) <br>
- [Claw Host Environment Reference](references/claw-host-env.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented result handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RollingGo CLI output, JSON by default, with table output only for hotel search.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
