## Description:

Shift-style continuity notes with ownership, limits, hazards, protected targets, receipts, and exact next action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when pausing work, changing the lead model, mining session history, or preparing a fresh model to continue work safely. It guides the agent to create a concise handover note covering current state, completed work, active ownership, hazards, limits, protected targets, receipts, rollback, and the exact next action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handover notes may include secrets or unrelated private details when summarizing local session and workspace state.

Mitigation: Give the agent a clear task or session scope and review the resulting note for secrets or unrelated private details before using it across sessions.

Risk: A stale or overly broad handover note can cause a follow-on agent to duplicate work, trust outdated state, or cross protected boundaries.

Mitigation: Use the skill's required sections for ownership, hazards, limits, protected targets, receipts, rollback, and exact next action, and verify volatile state before acting on the handover.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinguy/skills/session-handover)
- [Server-resolved GitHub source](https://github.com/pinguy/Skills/tree/main/skills/session-handover)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown handover note with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update durable workspace notes such as SESSION_NOTES.md, daily memory entries, or active blackboards.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
