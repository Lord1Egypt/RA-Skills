## Description:

Waimai Merchant helps agents manage local food-delivery merchant and product records, including merchant registration, product creation, price updates, and delivery-time settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and developers use this skill to manage local food-delivery merchant onboarding, menu, pricing, stock, and delivery-promise records through a Node.js CLI. It is suited for local operations workflows where data is stored in SQLite rather than synchronized with live delivery platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive and customer-facing commands such as delete, reject, suspend, product visibility, price, stock, and delivery-time changes can execute immediately.

Mitigation: Require explicit user confirmation in the current turn, verify target record IDs and current values, show a before/after diff, and keep backups before running high-impact commands.

Risk: Merchant and product data is stored in a local SQLite database under the user's home directory.

Mitigation: Install only where local storage of merchant, contact, address, pricing, and product data is acceptable, and restrict access to the local data directory.

Risk: The skill manages local records and is not synchronized to Meituan, Ele.me, or another live delivery platform.

Mitigation: State the local-only scope in completion reports and avoid representing local CLI changes as live platform updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/waimai-merchant)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and CLI status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command suggestions, changed IDs, before/after summaries, and rollback guidance.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
