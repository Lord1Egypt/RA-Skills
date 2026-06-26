## Description: <br>
Automates daily Xiaohongshu content creation, publishing, marketing, and engagement for creator ID 4740535877 with strict persona and promotion controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a950701zz](https://clawhub.ai/user/a950701zz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators or authorized account operators use this skill to run a daily Xiaohongshu workflow for one named creator account, including topic selection, post drafting, publishing validation, and comment engagement. It is intended only for operators authorized to act on creator ID 4740535877. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a named Xiaohongshu account and publish public content. <br>
Mitigation: Install and run it only when authorized to operate creator ID 4740535877. <br>
Risk: Posts and comments may be published without explicit human approval. <br>
Mitigation: Use draft or preview mode, or add approval before each post and comment. <br>
Risk: Scheduled publishing and interaction cycles can continue without clear stop controls. <br>
Mitigation: Set daily limits, keep the documented posting and interaction caps, and provide a stop mechanism before scheduled operation. <br>
Risk: Separately supplied helper scripts could affect publishing behavior. <br>
Mitigation: Review any helper script before execution and stop after a failed retry as described in the risk-control guidance. <br>


## Reference(s): <br>
- [Cold Start Strategy](references/cold-start-strategy.md) <br>
- [Comment Reply Logic](references/comment-reply-logic.md) <br>
- [Dynamic Adjustment Logic](references/dynamic-adjustment.md) <br>
- [Marketing Control System](references/marketing-control.md) <br>
- [Persona Template](references/persona-template.md) <br>
- [Risk Control Rules](references/risk-control.md) <br>
- [Schedule System](references/schedule-system.md) <br>
- [Strict Publish Validation Protocol](references/strict-publish-validation.md) <br>
- [Topic Decision Engine](references/topic-decision-engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown and short-form post text with operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated posts are constrained to image-text mode, at most 400 characters each, with no more than 3 posts and 3 interaction cycles per day.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
