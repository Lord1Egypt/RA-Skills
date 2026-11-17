## Description:

Proactively maintains task state across starts, progress updates, completions, failures, and session resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent maintain a concise task state snapshot, including active work, background sessions, recent completions, and next steps, so work can resume after resets or compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatically persisted task details and operational metadata may include secrets, private URLs, internal hostnames, production commands, SSH/session details, customer data, or sensitive errors.

Mitigation: Review and redact task state before and after use, avoid recording secrets or sensitive infrastructure identifiers, and clear the state file when persistence is not needed.

Risk: Default tracking across every task and session reset can preserve more operational context than a user expects.

Mitigation: Make persistence visible to users, keep the state file easy to inspect, prune it regularly, and use opt-in persistence where policy requires.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/sunshine-agent-task-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown task-state snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains memory/tasks.md under 50 lines / 2 KB with active, completed, failed, or paused task status.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
