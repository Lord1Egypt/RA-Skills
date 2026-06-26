## Description: <br>
Guides an agent through a fixed Xiaohongshu publishing workflow for image-based or long-form posts to improve posting success rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, or operators use this skill to have an agent publish confirmed content and prepared image assets to Xiaohongshu, then report success or a retryable failure reason. <br>

### Deployment Geography for Use: <br>
Global, subject to Xiaohongshu Creator Center availability and account access. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish real Xiaohongshu posts through the currently logged-in creator account. <br>
Mitigation: Require final confirmation of the active account, exact content, media, title, and tags before clicking publish. <br>
Risk: The workflow can record published content to Feishu without a clearly scoped destination. <br>
Mitigation: Confirm the Feishu destination and logging scope before writing, or disable that step for the run. <br>


## Reference(s): <br>
- [Xiaohongshu image publishing page](https://creator.xiaohongshu.com/publish/publish?target=image) <br>
- [Xiaohongshu long-form publishing page](https://creator.xiaohongshu.com/publish/publish?target=text) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown text with status details and links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a published Xiaohongshu link, an error reason, and retry guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
