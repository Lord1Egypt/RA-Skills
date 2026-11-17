## Description:

工作伴侣｜四件小事判官（Workday Companion / Daily Decision Helper）：面向上班族、学生实习、自由职业和远程办公，在开工、午饭、低电量、下班四个高摩擦时刻先给判断、再给动作，最多追问一个关键字段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[killsnake01](https://clawhub.ai/user/killsnake01)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, students, interns, freelancers, and remote workers use this skill to reduce decision fatigue at four workday moments: starting work, choosing lunch, recovering from low energy, and planning after work. It returns a short judgment card first, asks at most one key follow-up, and avoids inventing restaurants, routes, health advice, or external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shareable image cards may expose personal details from real workday context, especially in rendered text or alt text.

Mitigation: Before sharing a generated card, remove real names, workplaces, addresses, routes, payment details, and health information from both visible text and alt text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killsnake01/skills/workday-companion)
- [Skill Definition](SKILL.md)
- [Module Contracts](references/module-contracts.md)
- [Image Model Adapter](adapters/image-model.md)
- [Public Listing Pack](references/public-listing-pack.json)
- [Card Schema](schemas/card.schema.json)
- [Smoke Cases](references/smoke-cases.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown short cards, optional JSON/SVG/HTML image-card payloads, and concise shell commands when installation is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image-card outputs should be privacy-reviewed before sharing, including alt text.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
