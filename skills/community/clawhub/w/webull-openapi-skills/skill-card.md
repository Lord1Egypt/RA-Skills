## Description:

Trade stocks, options, futures, crypto, and event contracts on Webull. Query real-time and historical market data. Manage accounts and positions. Supports US, HK, JP, SG, TH, MY, UK, MX, BR, EU, ZA, and AU regions with configurable risk controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webull-openapi](https://clawhub.ai/user/webull-openapi)

### License/Terms of Use:

Apache License

## Use Case:

Developers and AI-agent users use this skill to connect assistants to Webull OpenAPI for market data queries, account and position review, authentication, and order workflows across supported regions. It is intended for careful, user-reviewed financial operations rather than autonomous investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live financial actions through Webull accounts, and server security evidence says its safety controls are not reliably enforced before live orders.

Mitigation: Review every order before execution, use preview actions where available, begin with sandbox credentials, and set WEBULL_ENVIRONMENT exactly to uat unless live trading is intentional.

Risk: Credentials and tokens for brokerage access are sensitive and could expose account data or trading permissions if mishandled.

Mitigation: Keep credentials and tokens outside the project directory, restrict account permissions where possible, and avoid sharing generated configuration files.

## Reference(s):

- [Webull OpenAPI Reference](references/api_reference.md)
- [Trading Guide](references/skill_trading.md)
- [Market Data Guide](references/skill_market_data.md)
- [Official Python SDK](https://github.com/webull-inc/webull-openapi-python-sdk)
- [Webull US API Documentation](https://developer.webull.com/apis/docs/webull-open-api-reference)
- [Webull HK API Documentation](https://developer.webull.hk/apis/docs/webull-open-api-reference)
- [Webull JP API Documentation](https://developer.webull.co.jp/apis/docs/webull-open-api-reference)
- [Webull SG API Documentation](https://developer.webull.com.sg/apis/docs/index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with CLI commands and formatted command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output includes region-aware disclaimers; successful operations write formatted data to stdout and errors to stderr.]

## Skill Version(s):

1.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
