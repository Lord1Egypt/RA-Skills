## Description:

Automates delivery lane diagnosis by scanning recovery tickets and delivery artifacts, classifying blockers, attempting bounded recovery actions, and recording diagnosis results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and delivery engineers use this skill to diagnose multi-lane delivery workflows, update recovery tickets, and trigger bounded recovery actions when expected artifacts or publishing receipts are missing. It is intended for recovery automation where human escalation is required for credential, account, or policy blockers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke publishing or recovery commands that affect external channels.

Mitigation: Require explicit approval gates and dry-run validation before enabling live publishing paths.

Risk: The skill can modify operational recovery tickets and runner logs.

Mitigation: Run with scoped workspace permissions and review ticket updates for accuracy before relying on automated closeout.

Risk: The skill checks credential-bearing configuration such as environment files.

Mitigation: Use secret-safe validation that confirms required keys without exposing secret values.

Risk: Fixed temporary payload paths can expose or collide with run data.

Mitigation: Use per-run private temporary files for generated publishing payloads and receipts.

Risk: Incorrect dates can cause the skill to diagnose or update the wrong delivery day.

Mitigation: Validate date inputs and artifact paths before any recovery action is executed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/ray-delivery-diagnosis)
- [Publisher profile](https://clawhub.ai/user/x-rayluan)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact diagnosis template](artifact/TEMPLATE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, JSON diagnosis artifacts, ticket updates, runner logs, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include delivery diagnosis JSON files, recovery ticket log entries, status changes, blocker receipts, and escalation notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
