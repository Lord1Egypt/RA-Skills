## Description:

知识星球主题管理工具，帮助代理搜索和查看主题，并在用户确认后发布、编辑、评论、回答、删除或管理主题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxq](https://clawhub.ai/user/zsxq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate a logged-in ZSXQ account for topic discovery and topic lifecycle management, including posts, comments, official answers, tags, digests, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated actions can read or change ZSXQ community content through the user's logged-in account.

Mitigation: Install only when account operation is intended, and verify the exact group, topic, and content before any create, edit, reply, answer, tag, digest, or delete action.

Risk: Topic deletion is irreversible and removes the target topic and related discussion.

Mitigation: Confirm the topic ID and visible topic content with the user before issuing the delete command.

Risk: Posting, editing, replying, answering, tagging, or digesting content may change what community members see.

Mitigation: Treat those operations as public write actions and require explicit user confirmation of the final content or setting change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsxq/skills/zsxq-topic)
- [topic +search](artifact/references/zsxq-topic-search.md)
- [topic +detail](artifact/references/zsxq-topic-detail.md)
- [topic +create](artifact/references/zsxq-topic-create.md)
- [topic +edit](artifact/references/zsxq-topic-edit.md)
- [topic +reply](artifact/references/zsxq-topic-reply.md)
- [topic +answer](artifact/references/zsxq-topic-answer.md)
- [topic delete](artifact/references/zsxq-topic-delete.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires zsxq-cli and an authenticated ZSXQ account.]

## Skill Version(s):

1.3.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
