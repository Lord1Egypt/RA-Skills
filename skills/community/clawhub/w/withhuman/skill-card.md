## Description:

Explains how withHuman routes agent tool calls through approval policies and human review, and how agents should respond to pending, denied, or expired decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[withhuman](https://clawhub.ai/user/withhuman)

### License/Terms of Use:

MIT-0

## Use Case:

Agent developers and operators use this skill to understand withHuman's approval model and guide agents through held, denied, expired, or cancelled tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval requests may expose tool arguments and context to reviewers.

Mitigation: Before configuring withHuman, review which arguments and context reviewers can see, and assess installation and pipeline skills separately.

Risk: Users may assume this informational guide connects an approval service.

Mitigation: Configure withHuman separately; installing this guide does not connect an approval service.

## Reference(s):

- [How withHuman works](https://withhuman.ai/docs/concepts/how-withhuman-works.md)
- [Agent Approval Protocol specification](https://agentapprovalprotocol.io)
- [withHuman Agent Approval Protocol reference](https://withhuman.ai/docs/reference/agent-approval-protocol.md)
- [withHuman documentation](https://withhuman.ai/docs.md)
- [withHuman self-hosted edition](https://github.com/withHumanAI/withHuman)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Explanatory text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Explains approval concepts and agent responses; directs setup questions to related withHuman skills.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
