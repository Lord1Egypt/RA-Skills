## Description:

Searches Xiaohongshu keywords, collects matching notes, extracts note text, engagement metrics, and comments, and helps summarize trends, sentiment, content ideas, or product feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ligoudanblabla](https://clawhub.ai/user/ligoudanblabla)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research Xiaohongshu keywords, gather note and comment data through an AgentBay browser workflow, and turn the collected material into structured market, sentiment, topic, or product-feedback summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentBay API keys may be exposed in console output or persistent logs.

Mitigation: Remove or redact key logging before using real credentials, and rotate any AgentBay key already used with this version.

Risk: Collected Xiaohongshu notes and comments may be stored locally during execution.

Mitigation: Run the skill in a contained environment, limit access to generated files and logs, and delete collected data when it is no longer needed.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ligoudanblabla/skills/xhs-search-skill)
- [Aliyun AgentBay product page](https://www.aliyun.com/product/agentbay)
- [Xiaohongshu](https://www.xiaohongshu.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and local JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AgentBay API key and Xiaohongshu login; may write local logs and collected note/comment JSON files during execution.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
