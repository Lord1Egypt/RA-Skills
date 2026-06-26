## Description: <br>
Formats completed Markdown drafts for Xiaohongshu, guides editor review, prepares semi-automated publishing, and supports post-publication data review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[little-ke](https://clawhub.ai/user/little-ke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to turn finalized Markdown drafts into Xiaohongshu-ready posts, coordinate user-confirmed publishing, and review performance after posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing actions can create real public Xiaohongshu posts from the user's account. <br>
Mitigation: Require explicit user confirmation before running the publish step and rely on the browser's final confirmation before submission. <br>
Risk: The workflow depends on an external browser automation script and saved login session that were not included in the reviewed package. <br>
Mitigation: Inspect and trust the referenced xhs_publish.cjs helper before use, confirm which account it controls, and understand where the saved login session is stored and how to remove it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/little-ke/xiaohongshu-publish-workflow) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before publication; the referenced Playwright publishing helper is not included in the reviewed package.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
