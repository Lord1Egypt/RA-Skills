## Description:

Manage SubsTracker subscriptions and configuration through Bun CLI scripts that authenticate to a SubsTracker REST API and return JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianchenx](https://clawhub.ai/user/ianchenx)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to inspect and manage a SubsTracker instance, including subscriptions, renewals, payment history, dashboard totals, notification tests, and application configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles credentials and session data for a SubsTracker instance.

Mitigation: Use an HTTPS SUBSTRACKER_URL, protect ~/.substracker-skills with private permissions, and run the skill only from trusted working directories.

Risk: The skill can perform destructive or sensitive account changes, including deletes, password updates, webhook changes, and notification-token changes.

Mitigation: Manually confirm delete, password, webhook, and notification-token changes before allowing the agent to run them.

Risk: Secrets may be exposed if passwords or API tokens are passed directly as command-line flags.

Mitigation: Avoid putting passwords or API tokens in command-line flags; prefer protected environment variables or a private .env file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ianchenx/skills/substracker)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Configuration instructions, Guidance]

**Output Format:** [Bun CLI commands with JSON stdout and human-readable Markdown summaries or tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SUBSTRACKER_URL, SUBSTRACKER_USER, and SUBSTRACKER_PASS through environment variables or a .substracker-skills/.env file; stores a session cookie under ~/.substracker-skills/.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
