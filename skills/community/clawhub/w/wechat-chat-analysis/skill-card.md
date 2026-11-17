## Description:

wechat-chat-analysis uses wechat-cli to read local WeChat chat records and produce structured relationship analysis, personality profiles, issue diagnosis, improvement suggestions, and next-reply guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiqingge](https://clawhub.ai/user/haiqingge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze local WeChat conversations for relationship stage, communication style, conversation momentum, and practical reply options. It supports both historical reviews of longer chat exports and real-time guidance for active conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private WeChat conversations and retain sensitive chat content in local plaintext cache or report files.

Mitigation: Use only with appropriate consent, review generated local files, and delete cache, history, feedback, or exported report data after use when it is no longer needed.

Risk: The package evidence indicates populated runtime chat data is bundled with the release.

Mitigation: Review and remove bundled runtime data before redistribution or installation in shared environments.

## Reference(s):

- [Chat Analysis Framework](references/analysis_framework.md)
- [Response Templates](references/response_templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with inline PowerShell/Python command examples and structured reply suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local cache, history, feedback, and exported chat report files in the skill data directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
