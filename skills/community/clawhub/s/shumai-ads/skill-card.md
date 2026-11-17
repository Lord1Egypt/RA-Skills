## Description:

查询澍脉AI投放驾驶舱的真实投放数据。当用户询问广告投放表现、账户余额、哪些广告计划该止损/优化/加预算、CPA/CTR 异常,或品牌在 AI 大模型(DeepSeek/豆包/Kimi 等)中的 GEO 可见度与排名时使用。需要环境变量 SHUMAI_API_KEY。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexun-inc](https://clawhub.ai/user/dexun-inc)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers, operators, and agents use this skill to query Shumai advertising dashboard data, summarize account performance and balance, surface campaign alerts, and report GEO visibility. It is read-only and directs users to advertising platform consoles for budget or campaign changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends SHUMAI_API_KEY to Shumai's service.

Mitigation: Treat SHUMAI_API_KEY as a secret and install the skill only when connecting Codex to the trusted Shumai advertising dashboard is intended.

Risk: The skill can read and summarize advertising and account data.

Mitigation: Use it only with accounts whose advertising data the agent is allowed to access, and review summaries before acting on campaign recommendations.

Risk: Users may treat read-only diagnostic recommendations as budget or campaign changes.

Mitigation: Keep changes outside this skill and direct users to the relevant media platform backend for any budget or campaign setting updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dexun-inc/skills/shumai-ads)
- [Shumai dashboard API key setup](https://www.shumai.com.cn/admin/)
- [Shumai MCP endpoint](https://www.shumai.com.cn/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Concise Chinese Markdown or text responses with preserved numeric values and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill summarizes read-only Shumai API responses and preserves returned numbers without modification or estimation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
