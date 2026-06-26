## Description: <br>
Operate Upbit public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Upbit public markets and run read-only market-data requests for tickers, minute candles, and order book snapshots through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests can target the wrong Upbit regional host or market symbol. <br>
Mitigation: Verify the regional host and quote-first market symbol before each request. <br>
Risk: Using endpoints outside this skill's documented public scope could require unsupported private authentication. <br>
Mitigation: Keep use to the documented public market-data endpoints and do not use this v1 skill for account or order operations. <br>
Risk: A remote schema URL can change over time and affect reproducibility. <br>
Mitigation: Use the packaged local schema or a pinned schema URL when reproducible behavior matters. <br>


## Reference(s): <br>
- [Upbit OpenAPI Skill on ClawHub](https://clawhub.ai/jolestar/upbit-openapi-skill) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/upbit-public.openapi.json) <br>
- [Packaged schema source URL](https://raw.githubusercontent.com/holon-run/uxc/main/skills/upbit-openapi-skill/references/upbit-public.openapi.json) <br>
- [Official Upbit Open API overview](https://global-docs.upbit.com/reference/api-overview) <br>
- [Publisher profile](https://clawhub.ai/user/jolestar) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public Upbit market-data operations; no credentials are required for the included endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
