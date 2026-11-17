## Description:

SYSU Anything CLI helps agents use the sysu-anything command-line tools for SYSU campus services, including schedules, bookings, campus systems, login recovery, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qybaihe](https://clawhub.ai/user/qybaihe)

### License/Terms of Use:

MIT-0

## Use Case:

Students, staff, and agents supporting SYSU campus workflows use this skill to route natural-language campus requests into the appropriate sysu-anything CLI commands. It covers read-only lookups, login recovery, reservation and application previews, and confirmed write actions when the user explicitly approves submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and fallback paths can execute mutable npm packages such as @latest.

Mitigation: Use a pinned, verified package version for installation and one-off execution.

Risk: The deployer can overwrite local AI or project instruction files.

Mitigation: Review the destination before deployment and avoid deploying an AI IDE bundle into an existing project directory.

Risk: The local state directory can contain active campus sessions, tokens, and QR login artifacts.

Mitigation: Treat ~/.sysu-anything/ as sensitive and do not expose its contents in prompts, logs, commits, or shared artifacts.

Risk: Reservation, application, upload, account-change, and other write actions may submit real campus requests when confirmed.

Mitigation: Run query and preview commands first, and add --confirm only after the user clearly approves the exact action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qybaihe/skills/sysu-anything-cli)
- [Publisher Profile](https://clawhub.ai/user/qybaihe)
- [SYSU-Anything Repository](https://github.com/qybaihe/SYSU-Anything)
- [SYSU Anything CLI Overview](references/overview.md)
- [Authentication and State](references/auth-and-state.md)
- [Safety and Confirm Boundary](references/safety-and-confirm.md)
- [USC / BPM Reservations](references/usc.md)
- [Apple Integration](references/apple.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands, CLI options, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to request JSON output from the CLI for structured campus data.]

## Skill Version(s):

0.3.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
