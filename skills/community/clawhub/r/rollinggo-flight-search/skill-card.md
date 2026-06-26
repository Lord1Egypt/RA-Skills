## Description: <br>
Search flights and airports using the RollingGo Flight CLI for flight search, airport-code lookup, cabin availability checks, and air-travel planning between cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to resolve airport or city codes and run structured one-way or round-trip flight searches with cabin, passenger, and date filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [RollingGo homepage](https://rollinggo.store) <br>
- [RollingGo API key request](https://rollinggo.store/apply) <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-flight-search) <br>
- [Claw Host Environment Reference](references/claw-host-env.md) <br>
- [RollingGo Flight Workflow Tutorials](references/flight-workflows.md) <br>
- [RollingGo Flight NPX Reference](references/rollinggo-flight-npx.md) <br>
- [RollingGo Flight UVX Reference](references/rollinggo-flight-uvx.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI result interpretation; the underlying CLI returns JSON by default and can return table output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROLLINGGO_API_KEY and a RollingGo CLI runtime such as npx, npm, uvx, uv, or the standalone binary; avoid passing real API keys on the command line.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
