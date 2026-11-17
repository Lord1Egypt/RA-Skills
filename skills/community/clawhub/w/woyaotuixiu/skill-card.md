## Description:

此 Skill 用于计算中国用户的退休时间和社保缴费总额，当用户询问退休时间、退休年龄、社保缴费、退休规划或灵活就业社保时，支持根据2025年1月1日起实施的延迟退休政策计算退休年龄，并根据工资、城市和就业类型估算从现在到退休需要缴纳的社保总金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[feversaga](https://clawhub.ai/user/feversaga)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect retirement-planning inputs for Chinese social-insurance scenarios, calculate a projected retirement date, and estimate remaining employee or flexible-employment social-insurance payments. The output should be treated as planning guidance rather than official pension, benefits, legal, or financial advice.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill shows shell command templates that include user-provided values.

Mitigation: Run the bundled calculator with a subprocess argument array, or strictly validate and quote each user-provided value before execution.

Risk: The included social-insurance base data is from 2024 and may be outdated.

Mitigation: Tell users the calculation is for reference only and verify current city social-insurance bases and policy details before relying on the result.

## Reference(s):

- [中国退休政策与社保缴费参考](references/retirement_policy.md)
- [ClawHub skill page](https://clawhub.ai/feversaga/skills/woyaotuixiu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional shell command examples and JSON calculation results from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on user-provided birth date, gender, female worker/cadre status, city, monthly salary or selected contribution base, employment type, and housing-fund inclusion.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
