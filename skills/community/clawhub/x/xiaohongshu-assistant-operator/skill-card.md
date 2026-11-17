## Description:

Automates daily Xiaohongshu content creation, publishing, controlled promotion, and comment engagement for one specified creator account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a950701zz](https://clawhub.ai/user/a950701zz)

### License/Terms of Use:


## Use Case:

Authorized account operators or creator assistants use this skill to plan, generate, publish, validate, and manage daily Xiaohongshu notes and replies for the named creator account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish and reply publicly for a specific Xiaohongshu account without explicit approval controls in the artifact.

Mitigation: Use it only for an account you control or are authorized to operate, and require preview, approval, logging, rate limits, and an easy disable path before publishing or replying.

Risk: Hard-coded creator mentions and promotion rules can create unwanted branding or marketing content.

Mitigation: Review each generated post and reply before use, and add a control that can disable mandatory mentions or promotion for individual outputs.

## Reference(s):

- [Xiaohongshu Assistant Operator ClawHub Page](https://clawhub.ai/a950701zz/skills/xiaohongshu-assistant-operator)
- [Cold Start Strategy](references/cold-start-strategy.md)
- [Comment Reply Logic](references/comment-reply-logic.md)
- [Dynamic Adjustment Logic](references/dynamic-adjustment.md)
- [Marketing Control System](references/marketing-control.md)
- [Persona Template](references/persona-template.md)
- [Risk Control Rules](references/risk-control.md)
- [Schedule System](references/schedule-system.md)
- [Strict Publish Validation Protocol](references/strict-publish-validation.md)
- [Topic Decision Engine](references/topic-decision-engine.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown post drafts, reply drafts, operating decisions, and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Artifact rules cap generated posts at 400 characters and limit default operation to up to 3 posts and 3 interaction cycles per day.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
