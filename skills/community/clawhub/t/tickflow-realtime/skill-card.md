## Description: <br>
Uses the TickFlow data center to query real-time quotes and K-line data for one or more symbols, including latest price, percent change, volume, trading session, and daily, weekly, or monthly bars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CengSin](https://clawhub.ai/user/CengSin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to retrieve TickFlow market quotes, compare multiple symbols, or summarize recent K-line data without exposing the API key in outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to the TickFlow API using a service API key. <br>
Mitigation: Install it only when TickFlow access is intended, use a least-privilege TICKFLOW_API_KEY, and confirm outbound requests target the TickFlow API. <br>
Risk: Market data requests may expose queried symbols or universes to the external TickFlow service. <br>
Mitigation: Avoid giving the skill unrelated sensitive data and review requested symbols before execution when confidentiality matters. <br>
Risk: The security summary notes a permissions-documentation gap. <br>
Mitigation: Review the required API key and outbound network behavior before deployment. <br>


## Reference(s): <br>
- [TickFlow API Notes](references/api.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [TickFlow OpenAPI specification](https://api.tickflow.org/openapi.json) <br>
- [TickFlow API endpoint](https://api.tickflow.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text summaries and tables, with raw or pretty-printed JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include quote summaries, comparison tables, K-line tables, API error messages, or raw TickFlow JSON; API keys are not included.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
