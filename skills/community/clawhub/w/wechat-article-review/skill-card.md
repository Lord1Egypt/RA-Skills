## Description:

Reviews WeChat public-account articles and drafts to produce a concise summary, diagnostic conclusions, prioritized improvement suggestions, and reusable deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, operations, marketing, and media teams use this skill to assess whether a WeChat article or draft will persuade its audience and to turn article material into prioritized edits and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted article drafts, URLs, uploaded-document references, audience details, goals, and brand constraints are sent to a remote AI Skills service.

Mitigation: Do not submit confidential or unapproved content; obtain authorization for sensitive drafts before use.

Risk: The runner can be redirected with AISKILLS_BASE_URL, which may send API credentials and submitted content to an unintended endpoint.

Mitigation: Keep AISKILLS_BASE_URL at the default trusted endpoint unless you control the replacement service and use HTTPS.

Risk: The skill output may contain incorrect or misleading copy review guidance.

Mitigation: Have a knowledgeable reviewer check recommendations before publishing or applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/wechat-article-review)
- [Publisher profile](https://clawhub.ai/user/allinherog-star)
- [Form schema](references/form-schema.json)
- [Skill metadata](references/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style recommendations in a JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summaries, diagnostic findings, action suggestions, and reusable deliverables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
