## Description:

曲阜师范大学（曲阜师大 / 曲师 / QFNU / 曲园）在校生校园生活与学业事务助手，用于回答校园生活、教务、资助、服务系统、住宿交通、就业考研等事务，并支持平均学分绩点估算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zexuan2008](https://clawhub.ai/user/zexuan2008)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially QFNU students and campus-support agents, use this skill to answer student-facing questions about academic policy, campus services, funding, housing, transport, official lookup paths, and GPA or eligibility self-checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campus deadlines, fees, phone numbers, quotas, and policy details may change after the bundled references were verified.

Mitigation: Verify time-sensitive items on official QFNU pages before giving definitive guidance, and state the applicable year, source, and lookup path.

Risk: The skill discusses identity authentication and default credential handling, which can expose sensitive account information if handled carelessly.

Mitigation: Do not ask users to share identity-card numbers, candidate numbers, or passwords; direct account actions to official systems and advise changing initial passwords immediately.

Risk: The GPA calculator provides estimates and may not match official course inclusion rules for degree, award, or recommendation decisions.

Mitigation: Use the script only for self-check calculations and tell users that the university education system, college review, and current official notices are authoritative.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zexuan2008/skills/qfnulife)
- [学业与教务](references/academic.md)
- [校园服务与信息系统](references/campus-services.md)
- [奖助学金与资助](references/funding.md)
- [校园生活：校区、食宿、交通、作息](references/living.md)
- [官方网址与电话速查表](references/official-links.md)
- [曲阜师范大学官网](https://www.qfnu.edu.cn)
- [曲阜师范大学教务处](https://jwc.qfnu.edu.cn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with optional inline shell commands for GPA calculations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes official lookup paths and cautions for time-sensitive campus policies; GPA calculations are estimates and not authoritative records.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
