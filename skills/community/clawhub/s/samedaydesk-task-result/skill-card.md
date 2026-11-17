## Description:

Helps developers acquire a pinned caller, retain complete tool results, recover interrupted results, and optionally report free feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to acquire the pinned SameDayDesk caller, keep caller-owned MCP or HTTP results intact, resume lost responses, and optionally submit feedback without initiating payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Acquisition downloads a client from neomorphic.io and can install npm dependencies.

Mitigation: Use a fresh work directory, review the pinned release before running it, and opt into dependency installation only when needed.

Risk: Result and checkpoint files may contain sensitive tool output.

Mitigation: Review caller-owned files before passing them in and protect retained copies accordingly.

Risk: Recovery and optional feedback may contact caller-provided endpoints.

Mitigation: Provide only endpoints and feedback tokens you intend the skill to use; HTTP feedback requires explicit send confirmation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/epistemedeus/skills/samedaydesk-task-result)
- [Pinned caller release details](references/caller-pin.json)
- [Pinned caller descriptor](https://neomorphic.io/downloads/samedaydesk-caller-result/0.1.1/descriptor.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Files]

**Output Format:** [Markdown guidance and shell commands; JSON status and retained result files when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains the full caller result and reports distinct recovery or feedback outcomes; missing inputs prompt a next action.]

## Skill Version(s):

0.1.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
