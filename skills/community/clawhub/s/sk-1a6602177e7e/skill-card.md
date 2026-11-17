## Description:

面向本科生的中文情景化问答助手，围绕学业、宿舍、金钱、身心状态和安全防坑问题给出具体回应，并在识别心理或人身安全危机时切换为严肃转介。

This skill is for research and development only.

## Publisher:

[dora233](https://clawhub.ai/user/dora233)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking undergraduate students, or agents assisting them, use this skill to triage concrete college-life dilemmas and produce grounded, nonjudgmental guidance with crisis-aware routing.

### Deployment Geography for Use:

Global, with guidance grounded in Chinese student support resources and policies.

## Known Risks and Mitigations:

Risk: Time-sensitive hotline, legal, medical, and campus-policy details may become outdated or vary by school.

Mitigation: Verify official sources before relying on those details, and use official emergency services directly in emergencies.

Risk: Mental-health and safety responses could be mistaken for professional crisis intervention.

Mitigation: Keep the skill's crisis-routing posture: suppress humor for high-risk situations and direct users to 12356, 110, 120, campus psychology centers, or trusted people as appropriate.

Risk: The release license and referenced non-commercial source constraints need human confirmation before commercial distribution.

Mitigation: Confirm the MIT-0 server license, the artifact's non-commercial statement, and any CC BY-NC-SA obligations before publication or reuse.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [Crisis protocol](artifact/references/crisis-protocol.md)
- [Sources and authorization archive](artifact/references/sources.md)
- [Profile slots](artifact/references/profile-slots.md)
- [Academic knowledge base](artifact/references/kb/01-academic.md)
- [Dorm knowledge base](artifact/references/kb/03-dorm.md)
- [Money knowledge base](artifact/references/kb/07-money.md)
- [Health knowledge base](artifact/references/kb/08-health.md)
- [Safety knowledge base](artifact/references/kb/10-safety.md)
- [大学生活质量指北 source project](https://github.com/CollegesChat/university-information)
- [ClawHub skill page](https://clawhub.ai/dora233/skills/sk-1a6602177e7e)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Chinese-language Markdown guidance or JSON routing output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crisis routing can suppress humor and direct users to emergency or official support resources.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
