## Description:

Queries China A-share, Hong Kong equity, futures, index, funds-flow, and financial data through the Tushare Pro HTTP REST API without requiring pip or a Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloryjack](https://clawhub.ai/user/gloryjack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to prepare Tushare Pro REST requests and example code for retrieving China market data, including equities, indices, futures, funds flow, and financial data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled token setup file references a lookalike Tushare domain, which could expose credentials or API tokens.

Mitigation: Obtain credentials only from the verified Tushare domain and correct the token setup guidance before deployment.

Risk: The skill asks users to place TUSHARE_TOKEN in a local token.env file, which can leak if packaged, committed, or shared.

Mitigation: Provide TUSHARE_TOKEN through the runtime environment or a secret manager and keep real tokens out of shared skill directories.

## Reference(s):

- [Tushare Pro](https://tushare.pro)
- [Tushare Pro API endpoint](https://api.tushare.pro)
- [ClawHub skill listing](https://clawhub.ai/gloryjack/skills/tushare-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, Python snippets, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TUSHARE_TOKEN and may depend on Tushare account permissions and rate limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
