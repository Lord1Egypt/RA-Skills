## Description: <br>
Token consumption monitoring and optimization analysis for querying LLM usage, costs, provider balances, prompt-style statistics, and optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyaok1](https://clawhub.ai/user/wangyaok1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use TokFlow to inspect local LLM token usage, spending, model and provider statistics, balances, and prompt-style optimization opportunities. The skill helps answer cost and usage questions by querying a local TokFlow API and summarizing the returned JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive LLM usage, spending, provider balance, and prompt-statistics data to the agent. <br>
Mitigation: Install only when the local TokFlow backend is trusted, and avoid balance or prompt-stat queries when account or session-derived usage information should not be surfaced in chat. <br>
Risk: Queries depend on a local backend at localhost:8001, so responses may fail or be stale if that service is unavailable or not synchronized. <br>
Mitigation: Confirm TokFlow is running locally and verify important cost, balance, or optimization conclusions against the source service before acting on them. <br>


## Reference(s): <br>
- [TokFlow ClawHub page](https://clawhub.ai/wangyaok1/tokflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Natural-language summaries derived from JSON API responses, with shell commands when invocation details are needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted TokFlow backend on localhost:8001; balance and prompt-stat commands may surface account, spending, usage, and session-derived statistics.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
