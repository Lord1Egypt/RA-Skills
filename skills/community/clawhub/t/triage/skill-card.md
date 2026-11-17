## Description:

Prioritizes competing tasks into P0-P3 by cost of delay and decides what to do first, what waits, and when to interrupt current work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and knowledge workers use this skill to classify competing work, incoming interruptions, tickets, alerts, deadlines, and backlog items by cost of delay so they can decide what to handle now, next, later, or not at all.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence task ordering and interruption decisions, including treating broad urgency language as a triage signal.

Mitigation: Run the documented P0-P3 level tests, ask a closed question at the P0/P1 boundary, and state the assigned priority so the user can correct it.

Risk: Standing priority rules could overfit to a user's corrections if applied without confirmation.

Mitigation: Use the observe, propose, confirm ladder and store or auto-apply a standing rule only after the user explicitly agrees.

Risk: Interrupting current work can leave active work in a fragile state.

Mitigation: Interrupt mid-task only for P0 by default and save a resume note before switching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/triage)
- [Clawic triage skill page](https://clawic.com/skills/triage)
- [Batch triage guidance](artifact/batch.md)
- [Bug, ticket, and alert triage guidance](artifact/bugs.md)
- [Deadline triage guidance](artifact/deadlines.md)
- [Interrupt handling guidance](artifact/interrupts.md)
- [Priority learning protocol](artifact/patterns.md)
- [Urgency signal guidance](artifact/signals.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style task priorities, reordered queues, concise rationale, questions, and optional local configuration or preference notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or update local priority preferences only after explicit user confirmation.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
