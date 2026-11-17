## Description:

仅适用于北京市企业职工基本养老保险退休金测算。支持依据北京政策参数计算基础养老金、个人账户养老金、过渡性养老金，并对未退休用户做未来缴费策略优化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[park-william](https://clawhub.ai/user/park-william)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect Beijing enterprise pension inputs, calculate pension components, and compare future contribution strategies for unretired users. It is limited to Beijing enterprise employee pension rules, including flexible workers covered under that pension channel.

### Deployment Geography for Use:

Beijing, China

## Known Risks and Mitigations:

Risk: The skill processes and persists sensitive pension and contribution records locally.

Mitigation: Use redacted copies where possible, run the skill in a dedicated working directory, and delete generated temporary JSON and Markdown files after use.

Risk: Local write behavior can create result files and update pension parameter data.

Mitigation: Restrict parameter updates to the bundled data/beijing_params.json file and review parameter changes before reuse.

Risk: Generated confirmation Markdown can contain user data and should not be treated as trusted instructions.

Mitigation: Use confirmation forms only for human review and avoid feeding them back to an agent as authoritative directions.

Risk: Dependency ranges are not fully pinned, which can affect reproducibility.

Mitigation: Prefer pinned dependency versions when installing for repeatable calculations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/park-william/skills/retirecalc-beijing)
- [Policy links bundled with the skill](artifact/references/policy-links.md)
- [北京市基本养老保险规定](https://www.beijing.gov.cn/gongkai/zfxxgk/zc/gz/202112/t20211216_2562734.html)
- [京劳社养发〔2007〕29号](https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/200804/t20080414_567067.html)
- [京劳社养发〔2007〕21号](https://www.beijing.gov.cn/zhengce/zhengcefagui/qtwj/200804/t20080414_567066.html)
- [2025年度北京市参保人员社会保险待遇通告](https://rsj.beijing.gov.cn/xxgk/2024zcwj/202511/t20251107_4265291.html)
- [2025年度北京市社保缴费工资基数上下限解读](https://rsj.beijing.gov.cn/xxgk/2024zcjd/202509/t20250918_4204887.html)
- [渐进式延迟法定退休年龄决定](https://www.gov.cn/yaowen/liebiao/202409/content_6974294.htm)
- [北京市灵活就业补贴说明](https://www.beijing.gov.cn/fuwu/bmfw/bmzt/lhjyry/202507/t20250709_4145233.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown explanations with JSON calculator results and generated confirmation forms]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include pension component amounts, source parameters, assumptions, missing-field review notes, and contribution strategy comparisons.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
