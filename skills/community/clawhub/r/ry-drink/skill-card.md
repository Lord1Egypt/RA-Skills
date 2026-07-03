## Description: <br>
瑞玥餐饮API lets a restaurant service agent retrieve live shop, menu, table, appointment, member, transaction, order, and payment-link information and perform reservation and dining-order actions through tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhimibuhui](https://clawhub.ai/user/zhimibuhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External restaurant customers use a merchant AI service agent to check live shop, menu, table, appointment, member, transaction, and order information, make or change reservations, adjust dining orders, and request payment links. Operators should deploy it in a controlled merchant/OpenClaw environment with trusted session-bound identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real bookings and dining orders, cancel reservations or orders, and generate payment links. <br>
Mitigation: Require explicit user confirmation before booking changes, cancellations, order changes, and payment-link generation. <br>
Risk: The skill can access member, transaction, appointment, and order information tied to customer identifiers. <br>
Mitigation: Enable access only after proper session binding and ensure phone or member identifiers are provided by the trusted platform context. <br>
Risk: The skill calls an internal restaurant service endpoint and depends on trusted transport controls. <br>
Mitigation: Install only in a controlled merchant/OpenClaw environment where the internal API endpoint is trusted, and prefer HTTPS or documented internal transport protections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhimibuhui/skills/ry-drink) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Tool manifest](artifact/tools.json) <br>
- [Tool routing notes](artifact/tool-router.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Guidance] <br>
**Output Format:** [Plain text user-facing responses with JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Many operations require session-bound shop, tenant, SaaS, phone, member, reservation, or order identifiers.] <br>

## Skill Version(s): <br>
1.0.28 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
