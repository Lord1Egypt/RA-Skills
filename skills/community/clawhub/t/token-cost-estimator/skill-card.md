## Description: <br>
Estimate API token costs from OpenClaw session transcripts by analyzing agent sessions and comparing per-token pricing with subscription plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[npfaerber](https://clawhub.ai/user/npfaerber) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to estimate OpenClaw API token usage and approximate costs from local session transcripts. It helps compare pay-per-use pricing against subscription plans using the user's own transcript data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The estimation script reads local OpenClaw session transcripts, which may contain sensitive conversation content. <br>
Mitigation: Run it only in an environment where local transcript access is acceptable, and narrow the script to specific agents, sessions, or date ranges when broad transcript analysis is unnecessary. <br>
Risk: Cost estimates can be incomplete because transcripts may omit system prompts, tool definitions, internal retries, or current pricing changes. <br>
Mitigation: Treat estimates as planning guidance, update pricing before relying on results, and compare with provider billing data when making spending decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/npfaerber/token-cost-estimator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown with an inline Python script and explanatory tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces approximate token and cost estimates from local OpenClaw session JSONL files; pricing values may need updates before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
