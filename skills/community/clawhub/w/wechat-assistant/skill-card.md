## Description:

Wechat Assistant captures visible Windows WeChat chat records, analyzes message patterns and requirements, manages a local reply knowledge base, generates draft replies for human review, and creates chat visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luemery](https://clawhub.ai/user/luemery)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill on Windows to capture and analyze WeChat Desktop conversations, generate reviewed reply drafts, maintain a local communication-style knowledge base, and produce relationship or timeline charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read visible WeChat chats and save private message content and derived analysis in plaintext local files.

Mitigation: Use a dedicated working folder, limit exports to the chats needed for the task, avoid sharing generated files without review, and delete or segregate files that contain sensitive conversations.

Risk: Reply-history and knowledge-base files may retain sensitive message text and personal communication patterns.

Mitigation: Review generated reply history and knowledge-base content regularly, remove sensitive entries, and keep those files outside shared or synchronized folders unless explicitly intended.

Risk: Generated replies may not match the user's intent or may be inappropriate for the conversation.

Mitigation: Keep human review enabled for approve, modify, or reject decisions before using any suggested reply.

## Reference(s):

- [Wechat Assistant Data Format Specification](references/format_spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus JSON and PNG files produced by the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on Windows with WeChat Desktop visible; generated chat records, analyses, knowledge-base data, and reply history may be stored as local plaintext files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
