## Description:

Jielong CLI helps an agent manage Jielong activities through the `jielong` command-line tool, including creating, viewing, modifying, deleting, starting, ending, and restarting activities, handling paid signup and check-in activities, managing form fields, and reviewing or deleting signup records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liu-tao-hash](https://clawhub.ai/user/liu-tao-hash)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to operate Jielong activity workflows from natural-language requests, including activity creation, signup management, status changes, field configuration, and attendance or paid registration handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update a global CLI package.

Mitigation: Install only when the user trusts the `jielong-cli` npm package, prefer a pinned package version, and confirm installation or update before execution.

Risk: The skill can open browser login flows and expose account identity details.

Mitigation: Ask before starting login, show only the minimum account confirmation details needed, and mask phone numbers, user IDs, OpenIDs, and other persistent identifiers.

Risk: The skill can modify, delete, clear, start, stop, restart, or create paid activity records.

Mitigation: Require explicit user confirmation for every destructive, account-changing, or paid-operation action, and summarize the target activity by name rather than by internal identifiers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liu-tao-hash/skills/tianba-jielong)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that invoke the global `jielong` CLI and JSON configuration for complex activity creation.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
