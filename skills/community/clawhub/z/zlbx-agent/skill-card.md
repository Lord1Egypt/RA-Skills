## Description:

知了商机大师开放平台。当用户需要"查标讯/看商机/发起AI对话/建跟进任务/查积分"等招投标商机场景时使用。通过命令行工具 scripts/zlbx_agent.py 调用知了开放平台 API。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query bidding notices, review business opportunities, start AI conversations, create follow-up tasks, retrieve bid details, and check account balance through the ZhiLiao open platform CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed if printed, pasted into chat, logged, or sent to an untrusted endpoint.

Mitigation: Use a dedicated low-privilege API key, avoid printing or pasting the key, and rotate it if exposure is suspected.

Risk: The configurable ZLBX_AGENT_BASE endpoint can receive the bearer token.

Mitigation: Keep the default endpoint unless the replacement endpoint is fully trusted.

Risk: The skill performs account-backed API calls that may consume credits or hit rate limits.

Mitigation: Check balance before use, keep calls scoped to the user's request, and retry only after rate-limit windows pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/skills/zlbx-agent)
- [ZhiLiao developer portal](https://agent.zhiliaobiaoxun.com/developer?utm_source=skill)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZLBX_AGENT_API_KEY; API calls consume account credits and are subject to documented rate limits.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
