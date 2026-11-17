## Description:

Use when the user needs Tonghuashun iFinD market, report, factor, screening, calendar, or other financial data, and all data must come from iFinD after successful authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherstrings](https://clawhub.ai/user/etherstrings)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers with Tonghuashun iFinD accounts use this skill to ask natural-language questions about market, financial, report, screening, and trading-calendar data while keeping data retrieval on iFinD.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill caches iFinD API tokens locally.

Mitigation: Use it only in environments where local token storage is acceptable, and avoid exposing tokens in visible command lines or command logs.

Risk: Optional LLM routing can send confidential financial query text to an external provider.

Mitigation: Leave LLM routing disabled for confidential queries unless the chosen provider and base URL are explicitly trusted.

Risk: Custom base URLs can redirect authentication or data requests to an untrusted destination.

Mitigation: Keep the default iFinD endpoint unless a custom endpoint has been independently trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/etherstrings/skills/tonghuashun-ifind)
- [iFinD HTTP API and Authentication Documentation](https://quantapi.51ifind.com/gwstatic/static/ds_web/quantapi-web/help-center/deploy.html)
- [iFinD Python HTTP Example](https://quantapi.51ifind.com/gwstatic/static/ds_web/quantapi-web/example.html)
- [iFinD Super Command Account Details](https://quantapi.10jqka.com.cn/gwstatic/static/ds_web/super-command-web/index.html#/AccountDetails)
- [Capability Matrix](references/capability-matrix.md)
- [Usage Guide](references/usage.md)
- [Routing Rules](references/routing.md)
- [Use Cases](references/use-cases.md)
- [Full Examples](references/full-examples.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires iFinD authentication; optional LLM routing can be enabled through environment variables.]

## Skill Version(s):

0.5.1 (source: server release evidence and usage documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
