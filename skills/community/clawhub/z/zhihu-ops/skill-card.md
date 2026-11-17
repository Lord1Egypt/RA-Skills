## Description:

Zhihu Ops guides an agent using OpenClaw browser to perform Zhihu interaction, publishing, editing, navigation, and review workflows while reusing observed page structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumailianxin](https://clawhub.ai/user/gumailianxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a logged-in Zhihu account through a browser for likes, favorites, comments, replies, article publishing, article editing, questions, creator-center navigation, and comment-management review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform public account actions on Zhihu, including posting, editing, commenting, replying, liking, and favoriting.

Mitigation: Review requests carefully before those actions and require clear user intent and content before public posts, edits, comments, or replies.

Risk: Browser page structure or element references may change, which can lead to failed or incorrect targeting.

Mitigation: Re-observe the current page, prefer visible button text and nearby context, and verify that the intended action succeeded.

Risk: Persisting newly observed page details can change future automation behavior.

Mitigation: Do not allow the skill to update its reference files unless preserving those page observations is intended.

## Reference(s):

- [Zhihu Page Map](artifact/references/page-map.md)
- [ClawHub Skill Page](https://clawhub.ai/gumailianxin/skills/zhihu-ops)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include action status, failure points, and resulting Zhihu URLs when available.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
