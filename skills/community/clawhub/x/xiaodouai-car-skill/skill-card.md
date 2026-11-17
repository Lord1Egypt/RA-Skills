## Description:

智能租车助手，一站式解决用户的租车需求，包括租车信息的查询，租车预定，租车下单，取消租车订单。当用户有租车意图时，自动触发该技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jsoncool](https://clawhub.ai/user/jsoncool)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要租车的用户，协助查询可租车型和价格、准备订单信息，并处理订单取消请求。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 取消订单可能产生费用，且当前扣款与退款金额尚未核实。

Mitigation: 取消已支付订单前，先通过服务提供方核实具体扣款和退款金额，并取得用户明确确认；存在费用疑问时优先引导用户使用官方应用处理。

Risk: 租车流程会处理身份信息，手机号查询还可能自动注册账户。

Mitigation: 在收集或查询前说明用途并取得用户同意；确认身份时使用脱敏信息，并避免在对话或日志中暴露完整身份号码和用户标识。

## Reference(s):

- [接口说明](references/接口说明.md)
- [小豆租车服务接口](https://interface.xiaodouzuche.com/xiaodou/)
- [ClawHub 技能发布页](https://clawhub.ai/jsoncool/skills/xiaodouai-car-skill)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [自然语言文本及结构化租车选项、价格和订单信息]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [车型与价格取决于服务端返回结果。]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
