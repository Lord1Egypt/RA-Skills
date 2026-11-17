## Description:

Collects Douyin and Bilibili video links, fetches video details, summarizes and categorizes the content, and writes the result to a Feishu Bitable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keson1521](https://clawhub.ai/user/keson1521)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to save Douyin and Bilibili videos into a Feishu Bitable with extracted metadata, content summaries, categories, topics, and watch-status tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based URL handling can mishandle or expose user-supplied video links.

Mitigation: Use only trusted Douyin and Bilibili links, validate exact HTTPS hosts before fetching, and avoid shell interpolation for untrusted URL values.

Risk: The skill can write records to Feishu Bitable using user-provided workspace configuration.

Mitigation: Require explicit confirmation before Feishu writes and verify the Base Token, Table ID, and field schema before running the write command.

Risk: Declared tool access may not fully match the commands described by the skill.

Mitigation: Review and align allowed tools with the commands the skill actually requires before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keson1521/skills/video-collector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown confirmation with extracted video metadata, summary, category, topic tags, and Feishu write status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare a JSON record for Feishu Bitable and uses configured Base Token and Table ID values supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
