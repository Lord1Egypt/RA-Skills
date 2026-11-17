## Description:

Wechat Workflow helps agents create WeChat Official Account cover images and articles, publish Markdown drafts, verify Sogou indexing, track article status, and suggest future topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators of WeChat Official Accounts use this skill to prepare article content, publish Markdown drafts for review, validate search indexing, and monitor follow-up publishing status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat Official Account API credentials.

Mitigation: Avoid entering real secrets on the command line, keep credentials in protected local storage or environment variables, and rotate any secrets that were printed in logs.

Risk: The skill can create WeChat draft content and contact WeChat and Sogou services.

Mitigation: Review each generated article and WeChat draft before public publication, and run the skill only where those network calls are expected.

Risk: The skill may write persistent files under the local OpenClaw workspace and install a global npm package when the publishing CLI is missing.

Mitigation: Inspect local workspace files after use, confirm package installation permissions in advance, and prefer a controlled environment for publishing workflows.

## Reference(s):

- [Writing Techniques](references/写作技巧.md)
- [High-Engagement Methodology](references/爆款方法论.md)
- [Human-Style Writing Guide](references/去AI味指南.md)
- [Khazix Skills Integration Reference](https://github.com/KKKKhazix/khazix-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, shell commands, configuration snippets, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create WeChat draft entries and local tracking or credential files when invoked.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
