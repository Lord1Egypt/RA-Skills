## Description: <br>
帮助代理通过 zsxq-cli 在知识星球中搜索主题、查看详情、发布和编辑帖子、评论、回复、回答提问、删除主题，并管理评论、精华、标签和个人问答记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsxq](https://clawhub.ai/user/zsxq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Knowledge Planet topic workflows through an authenticated zsxq-cli session. It supports finding content, reviewing topic details, creating or changing public content, answering questions, and applying topic metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, edit, reply, answer, tag, set digest status, and delete content through a logged-in Knowledge Planet account. <br>
Mitigation: Confirm the exact group_id or topic_id, target content, and final text with the user before any account-changing command. <br>
Risk: Deleting a topic is permanent and removes the topic, comments, and answers. <br>
Mitigation: Fetch and review the topic details first, then require explicit confirmation that deletion is intended. <br>
Risk: The skill depends on the local zsxq-cli binary and its authenticated account state. <br>
Mitigation: Use only a trusted zsxq-cli installation and verify the active account before performing write or delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zsxq/zsxq-topic) <br>
- [topic +search](references/zsxq-topic-search.md) <br>
- [topic +detail](references/zsxq-topic-detail.md) <br>
- [topic +create](references/zsxq-topic-create.md) <br>
- [topic +edit](references/zsxq-topic-edit.md) <br>
- [topic +reply](references/zsxq-topic-reply.md) <br>
- [topic +answer](references/zsxq-topic-answer.md) <br>
- [topic delete](references/zsxq-topic-delete.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires zsxq-cli and an authenticated Knowledge Planet account.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
