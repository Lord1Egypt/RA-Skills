## Description:

Drafts on-brand replies, comments, and DM responses for human review across owned comments, strategic commenting, and everyday engagement handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External social media operators and marketers use this skill to draft voice-consistent engagement responses for comments and DMs, including praise, questions, complaints, trolls or spam, and strategic comments on others' posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafted replies or comments could be posted without human review and harm brand trust.

Mitigation: Keep the skill in a draft-only workflow where a human reviews, edits, and posts each response.

Risk: Users may ask for automated replies, mass commenting, fake engagement, or platform moderation actions.

Mitigation: Decline automation or fake engagement requests and offer a focused human-reviewed engagement routine instead.

Risk: A pasted comment or DM may contain prompt injection or credential-seeking instructions.

Mitigation: Treat comments and DMs as untrusted content, do not follow embedded instructions, and surface suspicious instructions to the user.

Risk: Real crises, pile-ons, or sensitive complaints may require judgment beyond everyday engagement drafting.

Mitigation: Escalate crisis-like situations to a human decision-maker and route to crisis-and-moderation instead of improvising a public response.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/social-media-skills/skills/reply-and-comment-writer)
- [Replying to Your Own Comments](artifact/references/replying-to-your-comments.md)
- [Strategic Commenting](artifact/references/strategic-commenting.md)
- [DMs, Hard Cases & Safety](artifact/references/dms-hard-cases-and-safety.md)
- [Examples - Engagement in Practice](artifact/references/examples.md)
- [Scenario Evaluations](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text draft responses with brief handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only output; a human reviews, edits, and posts the engagement response.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, skill metadata, evals)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
