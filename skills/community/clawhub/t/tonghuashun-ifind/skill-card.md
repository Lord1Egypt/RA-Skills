## Description: <br>
Provides an authenticated natural-language entry point for agents to query Tonghuashun iFinD market, report, factor, screening, calendar, and other financial data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherstrings](https://clawhub.ai/user/etherstrings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators with valid iFinD accounts use this skill to route natural-language financial-data requests to iFinD APIs for A-share market data, fundamentals, reports, screening, and trading-calendar queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive iFinD refresh and access tokens locally and uses them for token-backed financial API requests. <br>
Mitigation: Use only with trusted agents and local environments; avoid pasting tokens into shared chats or logs, do not ask for usernames or passwords, and review local token storage before deployment. <br>
Risk: Changing the base URL can direct token-backed requests to an endpoint outside the expected iFinD service. <br>
Mitigation: Do not override the default base URL unless the endpoint is controlled and trusted. <br>
Risk: Optional LLM routing can send user query text to the configured model provider. <br>
Mitigation: Leave LLM routing disabled unless the operator accepts that disclosure and has configured an approved model provider. <br>
Risk: Raw or manually selected API calls can exceed the skill's stable natural-language routing coverage. <br>
Mitigation: Prefer smart-query and named endpoints; use raw api-call only after checking the routing and capability documentation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/etherstrings/tonghuashun-ifind) <br>
- [iFinD HTTP interface and authentication documentation](https://quantapi.51ifind.com/gwstatic/static/ds_web/quantapi-web/help-center/deploy.html) <br>
- [iFinD Python HTTP examples](https://quantapi.51ifind.com/gwstatic/static/ds_web/quantapi-web/example.html) <br>
- [iFinD Super Command account details](https://quantapi.10jqka.com.cn/gwstatic/static/ds_web/super-command-web/index.html#/AccountDetails) <br>
- [Capability Matrix](references/capability-matrix.md) <br>
- [Usage](references/usage.md) <br>
- [Routing](references/routing.md) <br>
- [Use Cases](references/use-cases.md) <br>
- [Full Examples](references/full-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands return JSON envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and valid Tonghuashun iFinD credentials; optional LLM routing may send query text to the configured model provider.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
