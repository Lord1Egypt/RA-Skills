## Description:

SHIFT routes coding, research, and quick tasks from one OpenClaw agent to specialized sub-identities, then synthesizes their responses in a single conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[palxislabs](https://clawhub.ai/user/palxislabs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use SHIFT to route coding, research, analysis, and quick-answer requests to configured specialist model personas while keeping one conversational interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegation can send selected chat history, MEMORY.md excerpts, and referenced file contents to the model providers configured for its personas.

Mitigation: Reduce contextBridge.historyTurns, avoid delegating tasks that reference sensitive files, use transparent mode, and review each configured provider's data policy before sensitive work.

Risk: Local .shift session files can retain delegation context, sub-identity outputs, consultation files, and cost-tracking data.

Mitigation: Periodically purge the .shift session directory and set contextBridge.archiveAfterMinutes to a short retention window.

Risk: Consultations and broad routing can trigger additional model calls and increase spend.

Mitigation: Evaluate first with costManagement.trackOnly enabled, then enforce costBudgetPerHour and alertThreshold settings before routine use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/palxislabs/skills/shift)
- [README](artifact/README.md)
- [Specification](artifact/SPEC.md)
- [Artifact Metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with optional code blocks, shell commands, configuration snippets, and session file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local session files, delegation context files, consultation outputs, and cost-tracking records under the OpenClaw workspace.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact _meta.json reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
