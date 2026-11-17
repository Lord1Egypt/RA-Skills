## Description:

Xiwu Inventory helps an agent manage a local home inventory through the xiwu CLI, including item lookup, add, consume, update, expiry alerts, and purchase-suggestion context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnqxu](https://clawhub.ai/user/johnqxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query, update, and summarize household inventory stored in a local xiwu database. It supports routine inventory management, expiry review, and purchase-planning context without choosing notification channels or calling commerce services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install an unpinned global xiwu-niangzi package.

Mitigation: Install only after trusting the package source; prefer a release that pins and verifies dependencies or requires explicit user-managed installation.

Risk: The skill can modify a local inventory database through shell commands built from user-provided inventory fields.

Mitigation: Review write operations before execution, use safe structured command execution for user-provided fields, and keep the skill's confirmation steps for updates and deletes.

Risk: Broad natural-language triggers may activate inventory actions in unintended conversations.

Mitigation: Narrow activation triggers and require explicit confirmation before destructive or quantity-changing actions.

## Reference(s):

- [Xiwu Inventory on ClawHub](https://clawhub.ai/johnqxu/skills/xiwu-inventory)
- [johnqxu Publisher Profile](https://clawhub.ai/user/johnqxu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Natural language responses and structured JSON from xiwu CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the xiwu command-line tool and uses --json for CLI calls.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
