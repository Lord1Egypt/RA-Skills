## Description:

Recall user memories from the Notion Memory Store when personal background, preferences, past decisions, or project context would improve an agent response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smilelight](https://clawhub.ai/user/smilelight)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to retrieve relevant personal or project memories from a Notion database named Memory Store and inject them as context for the current conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently and proactively read personal Notion memory records across broad tasks without clear per-use user control.

Mitigation: Install only when users are comfortable with proactive Memory Store lookup, and keep the Notion integration limited to the intended database.

Risk: Stored memory records may influence future responses, including records that contain secrets, stale facts, or executable instructions.

Mitigation: Avoid storing secrets or executable instructions in Memory Store, and periodically review or edit memory records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smilelight/skills/recall-from-notion)
- [OpenClaw Notion dependency](https://clawhub.ai/steipete/notion)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown]

**Output Format:** [Markdown guidance with Notion API examples and recalled context blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workflow that can silently skip recall when the Memory Store database is unavailable.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
