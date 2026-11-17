## Description:

Editorial review for news-style submissions: normalize metadata and body, check consistency, links, policy risk, author identity, byline, and timing, then recommend approve, reject, or delete with actionable author feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manwjh](https://clawhub.ai/user/manwjh)

### License/Terms of Use:

MIT-0

## Use Case:

Editors, moderators, and publication operators use this skill to review news-style submissions across Markdown, JSON, HTML, plain text, or conversation input. It produces a normalized editorial report covering metadata consistency, links, content risk, author identity and timing, a publish/reject/delete recommendation, and author-facing feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend reject or delete outcomes for submitted content.

Mitigation: Treat the report as decision support and require the user or host platform to perform any actual publication, rejection, or deletion action.

Risk: The skill may flag legal, medical, financial, copyright, or other policy-sensitive content but is not a substitute for specialist final review.

Mitigation: Route high-risk or regulated submissions to the appropriate human reviewer before publication or removal.

## Reference(s):

- [Zen Editorial Review on ClawHub](https://clawhub.ai/manwjh/skills/zen-editorial-review)
- [ZenHeart homepage](https://zenheart.net)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with tables and actionable feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a single recommended action: approve, reject, or delete; does not perform publication or deletion actions.]

## Skill Version(s):

2.0.2 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
