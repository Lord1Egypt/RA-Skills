## Description:

xhs 全流程助手，覆盖小红书内容策划、文案与标题生成、封面制作、笔记发布及日常运营管理。适用于写笔记、生成标题/封面、发布或保存草稿、站内搜索、评论互动（点赞/收藏/回复）等小红书相关任务。支持从内容创作到发布执行的一站式流程；封面 AI 生图可选配置 GEMINI_API_KEY、IMG_API_KEY 或 HUNYUAN_API_KEY。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

Creators, operators, and agents use this skill to plan Xiaohongshu content, create titles and bodies, prepare optional cover images, save drafts, publish after explicit confirmation, reply to comments or messages, and check visible dashboard metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate actions in a user's Xiaohongshu account.

Mitigation: Review drafts and replies before sending, and keep publish confirmation explicit in the current chat turn.

Risk: Optional cover-image generation may require external API keys.

Mitigation: Provide GEMINI_API_KEY, IMG_API_KEY, or HUNYUAN_API_KEY only when optional image generation is intended.

## Reference(s):

- [Xiaohongshu Creator Site](https://creator.xiaohongshu.com)
- [Post Templates](references/post-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown result summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include action, account, title, mode, result status, details, and next step.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
