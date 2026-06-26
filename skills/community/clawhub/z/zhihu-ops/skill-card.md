## Description: <br>
Zhihu Ops guides an agent using OpenClaw browser to perform Zhihu interaction and creator workflows, including liking, saving, commenting, replying, publishing or editing articles, asking questions, and navigating creator pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gumailianxin](https://clawhub.ai/user/gumailianxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a logged-in Zhihu browser session for visible interaction and creator workflows while reusing known page structures and button semantics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Zhihu browser session for visible account actions. <br>
Mitigation: Install and run it only when the user is comfortable with those account actions, and require explicit Zhihu URLs or current page context before acting. <br>
Risk: Public posts, article edits, comments, and replies can publish user-visible content. <br>
Mitigation: Confirm the target and final content before submission, and do not send comments, replies, posts, or edits when the user has not provided clear text. <br>
Risk: The skill suggests saving newly observed page-structure notes back into skill files. <br>
Mitigation: Deny skill-file write-back when the user does not want the skill or reference files updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gumailianxin/zhihu-ops) <br>
- [Zhihu page map](references/page-map.md) <br>
- [Zhihu home](https://www.zhihu.com) <br>
- [Zhihu creator center](https://www.zhihu.com/creator) <br>
- [Zhihu article editor](https://zhuanlan.zhihu.com/write) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Concise text status report after browser actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the resulting Zhihu URL when a publication or edit succeeds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
