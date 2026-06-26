## Description: <br>
Use the we-promise/sure REST API with X-Api-Key auth for accounts, transactions, categories, tags, merchants, imports, holdings, trades, valuations, chats, official docs URLs, self-update workflow from upstream OpenAPI, and ClawHub publish readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashanzzz](https://clawhub.ai/user/ashanzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect and operate Sure financial resources through documented API endpoints, with wrapped commands for common flows and raw endpoint access for official endpoints that are not yet wrapped. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write to and delete Sure financial/account data. <br>
Mitigation: Prefer wrapped CLI commands, review current state first, use dry-run where supported, and require explicit approval before any write or delete. <br>
Risk: The raw request helper can reach destructive official endpoints, including account reset or deletion paths. <br>
Mitigation: Avoid raw helper calls for destructive paths unless the operator has reviewed the endpoint, payload, and account impact. <br>
Risk: The skill requires access to a Sure API key for a financial account. <br>
Mitigation: Load credentials only from secure environment configuration and do not paste API keys into chat or non-secure files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ashanzzz/sure-api) <br>
- [Sure API endpoint summary](references/api_endpoints_summary.md) <br>
- [Sure OpenAPI snapshot](references/openapi.yaml) <br>
- [Sure upstream repository](https://github.com/we-promise/sure) <br>
- [Sure upstream API docs](https://github.com/we-promise/sure/tree/main/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SURE_BASE_URL and SURE_API_KEY from secure environment configuration; write-capable wrapped commands require explicit confirmation flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
