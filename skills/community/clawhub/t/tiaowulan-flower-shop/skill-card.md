## Description:

跳舞兰订花技能帮助用户从固定鲜花目录中浏览、筛选、推荐花束，并完成配送信息收集、订单提交和支付引导。

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaoleaf](https://clawhub.ai/user/piaoleaf)

### License/Terms of Use:

MIT-0

## Use Case:

Flower shoppers use this agent skill to browse a fixed catalog, get recommendations by occasion, recipient, or budget, collect delivery details, submit an order, and guide payment.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill collects recipient delivery personal data, including name, phone number, address, card message, and delivery time.

Mitigation: Use only with a trusted flower-shop operator, obtain explicit user confirmation before submission, and disclose that delivery details are sent to piaoleaf.tiaowulan.com.

Risk: The order flow instructs the agent to execute a generated raw shell curl command containing user input.

Mitigation: Replace the shell command with a scoped HTTP integration that validates fields and serializes JSON or form data safely.

Risk: The authoritative scanner verdict for this release is suspicious.

Mitigation: Review the skill before installing and scan it again in the target deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piaoleaf/skills/tiaowulan-flower-shop)
- [Publisher profile](https://clawhub.ai/user/piaoleaf)
- [Order submission endpoint](https://piaoleaf.tiaowulan.com/api/trade/CreateOrder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style product cards, conversational text, and a curl command for order submission]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collects recipient name, phone number, delivery address, card message, and delivery time before order submission.]

## Skill Version(s):

1.0.3 (source: evidence.release.version; target metadata agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
