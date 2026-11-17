## Description:

Provides multilingual scaffolded queries and sample analysis for U.S. market policy, regulations, and investment-environment topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, analysts, and developers can use this skill as a multilingual starting point for querying U.S. policy categories and generating investment-environment summaries. Results should be checked against authoritative sources before regulatory, compliance, or investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be mistaken for live or authoritative U.S. policy analysis even though the evidence describes it as a scaffold.

Mitigation: Treat outputs as preliminary guidance and verify policy, regulatory, and investment claims against authoritative sources before acting.

Risk: Configured data source or API key strings may appear in ordinary query results or cached outputs.

Mitigation: Use non-sensitive source identifiers and environment-based secret handling; do not pass real API keys or sensitive endpoint strings through dataSources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/usa-market-policy-2026)
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack)
- [DeepSeek](https://deepseek.com)
- [Huimai documentation](https://docs.huimai.ai)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Plain text and JSON-like JavaScript objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports zh-CN and en-US language modes; policy data sources are caller-configured.]

## Skill Version(s):

1.0.0 (source: release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
