## Description: <br>
通过小红书网页端发布和管理笔记，支持长文、图文、视频、定时发布、草稿管理、评论回复和数据查看。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content operators use this skill to guide an agent through Xiaohongshu web publishing workflows, including post creation, scheduling, draft handling, comment replies, and performance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent operating a logged-in Xiaohongshu account, including publishing, editing, deleting, scheduling, and replying to comments. <br>
Mitigation: Use a dedicated browser profile and require explicit preview and approval before every publish, edit, delete, scheduled post, or comment reply. <br>
Risk: Drafts, scheduled-post queues, and replied-comment records may be retained in local files. <br>
Mitigation: Review or disable local record files and avoid storing sensitive account, audience, or unpublished content data. <br>
Risk: Auto-reply behavior may post unintended or noncompliant responses from the account. <br>
Mitigation: Keep comment replies in approval-only mode, limit automation frequency, and review response content before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuritu/temp-xhs-skill) <br>
- [Xiaohongshu creator platform](https://creator.xiaohongshu.com/) <br>
- [Xiaohongshu publish page](https://creator.xiaohongshu.com/publish/publish?source=official) <br>
- [Xiaohongshu notifications](https://www.xiaohongshu.com/notification) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown instructions and checklists for browser-based publishing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to maintain local draft, schedule, and replied-comment records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
