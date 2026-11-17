## Description:

Manage shared expenses, balances, and settlements through the Splitwise CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barronlroth](https://clawhub.ai/user/barronlroth)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Splitwise balances and groups, list expenses, create shared expenses, record settlements, and delete records through the local Splitwise CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive Splitwise balances, friends, groups, and expense history to the agent.

Mitigation: Use only when the user is comfortable granting the agent access to local Splitwise CLI data and OAuth-backed account context.

Risk: Expense creation, settlement recording, and expense deletion can change financial records.

Mitigation: Require explicit user confirmation before creating expenses, recording settlements, or deleting records.

Risk: Duplicate or incorrect expense entries can affect shared balances.

Mitigation: List recent matching expenses before logging recurring or similar charges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barronlroth/skills/splitwise-cli)
- [Splitwise CLI homepage](https://github.com/example/splitwise-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports JSON, quiet, and no-color CLI output modes when the underlying splitwise command is run.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
