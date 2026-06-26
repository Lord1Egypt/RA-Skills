## Description: <br>
唯品会购物返利与订单管理工具，追踪唯品会返利订单状态，统计品牌特卖省钱金额，管理唯品券使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to organize Vipshop rebate orders, coupon reminders, expected rebate timing, brand sale notices, and savings summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may share more Vipshop account, order, coupon, rebate, balance, payment, or session information than the skill needs. <br>
Mitigation: Share only the order, coupon, rebate, or balance details required for the current task; do not provide passwords, cookies, session tokens, or payment credentials. <br>
Risk: Rebate timing, sale calendars, coupon expiry, and balance figures may be incomplete or stale if the user-provided data is outdated. <br>
Mitigation: Treat generated tracking summaries and reminders as planning aids and verify important order, coupon, and balance details against Vipshop or the relevant rebate source before taking action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fangshan101-coder/weipinghui) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with order, rebate, coupon, and brand sale sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; the skill provides structured shopping-management guidance and reminders.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
