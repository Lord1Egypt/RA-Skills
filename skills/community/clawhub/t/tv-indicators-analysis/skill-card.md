## Description:

通过调用Prana平台上的远程 agent 执行 TradingView 技术指标相关的分析与计算，并将结果返回给调用方

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochengzhen](https://clawhub.ai/user/xiaochengzhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request TradingView technical-indicator analysis or related market calculations through Prana for securities such as Chinese equities. It is intended for analysis requests and should not be used with personal, brokerage, account, or credential data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-analysis prompts are sent to the Prana remote service.

Mitigation: Use the skill only for non-sensitive analysis prompts and avoid personal, account, brokerage, or credential data.

Risk: The skill stores a persistent Prana API key in OpenClaw.

Mitigation: Install only after reviewing the credential requirement and restrict or rotate the key according to the user's environment policy.

Risk: The skill can expose a browser-openable skill history link.

Mitigation: Treat returned history links as sensitive and share them only with intended recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaochengzhen/skills/tv-indicators-analysis)
- [Prana service homepage](https://www.prana.chat/)
- [Prana agent-run endpoint](https://www.prana.chat/api/claw/agent-run)
- [Prana skill history endpoint](https://www.prana.chat/api/claw/skill-purchase-history-url)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text or Markdown responses, with shell commands and JSON API payloads when configuration or remote execution is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a persistent PRANA_SKILL_API_FLAG value for Prana requests and can return a browser-openable skill history link.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
