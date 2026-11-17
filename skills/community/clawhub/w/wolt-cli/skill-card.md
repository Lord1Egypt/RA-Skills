## Description:

Use Nikita's local Wolt CLI to browse venues, inspect menus/items/options, and run profile, cart, and checkout-preview actions for wolt.com from terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mekedron](https://clawhub.ai/user/mekedron)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to operate a local Wolt CLI for venue discovery, menu and item inspection, profile review, cart updates, and checkout preview workflows. It is useful for food-search and basket-preparation tasks that need structured terminal output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require users to handle live Wolt credentials in terminal commands and local configuration.

Mitigation: Use a pinned, verified CLI release, avoid exposing tokens in shared terminals, logs, screenshots, or shell history, and confirm credential storage permissions before use.

Risk: Credential refresh data can be persisted locally by the CLI.

Mitigation: Review where credentials are stored, restrict local file permissions, and rotate or revoke credentials after testing when appropriate.

Risk: Cart, favorite, address, or configuration commands can mutate a real account state.

Mitigation: Start with read-only commands and require explicit user confirmation before cart, favorites, address, or configure operations.

Risk: Checkout preview could be misunderstood as final order placement.

Mitigation: Describe checkout preview only as pricing and basket validation; do not present it as placing an order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mekedron/skills/wolt-cli)
- [Tool repository](https://github.com/mekedron/wolt-cli)
- [Command Reference](references/command-reference.md)
- [Workflows](references/workflows.md)
- [Output and Errors](references/output-and-errors.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON/YAML parsing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers machine-readable CLI output and surfaces warnings or error envelopes when present.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
