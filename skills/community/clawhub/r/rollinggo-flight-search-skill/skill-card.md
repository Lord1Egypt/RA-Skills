## Description: <br>
Uses the RollingGo Flight CLI to look up airport codes and flight search results for structured flight-query workflows, without booking, check-in, seat selection, or payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-assistant agents use this skill to parse flight-search requests, resolve city or airport codes, and query one-way or round-trip flight results through RollingGo Flight CLI. It is limited to search and reference workflows, not transaction completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires ROLLINGGO_API_KEY, which is a sensitive credential. <br>
Mitigation: Store the key in per-skill configuration or an equivalent scoped secret store, and avoid broad host-wide environment exposure unless intentionally shared. <br>
Risk: The skill documents latest-version package execution and installation flows. <br>
Mitigation: Use npx, npm, or uvx from a reviewed version when possible, and record the reviewed package version for reproducible operation. <br>
Risk: The reference material includes curl or irm pipe-to-shell installer commands. <br>
Mitigation: Inspect and verify installer scripts before execution, or prefer package-manager based installation paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/rollinggo-flight-search-skill) <br>
- [RollingGo homepage](https://rollinggo.store) <br>
- [RollingGo API key application](https://rollinggo.store/apply) <br>
- [NPX runtime reference](references/rollinggo-flight-npx.md) <br>
- [UVX runtime reference](references/rollinggo-flight-uvx.md) <br>
- [Flight workflow tutorial](references/flight-workflows.md) <br>
- [Host environment configuration](references/claw-host-env.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and CLI output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ROLLINGGO_API_KEY; CLI stdout returns JSON by default or table output when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
