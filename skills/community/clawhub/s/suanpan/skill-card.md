## Description:

Converts Chinese natural-language transaction descriptions into suanpan CLI commands for bookkeeping, expense and income recording, transfers, queries, and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinguobing](https://clawhub.ai/user/yinguobing)

### License/Terms of Use:

MIT-0

## Use Case:

People using the suanpan personal finance CLI use this skill to turn Chinese bookkeeping requests into reviewable shell commands for adding, querying, analyzing, and managing local financial records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references a one-line remote installer.

Mitigation: Inspect or verify the install script and upstream repository before running it; prefer a reviewed source build or pinned release when possible.

Risk: Generated commands can add, update, remove, import, or export financial records.

Mitigation: Require explicit user confirmation before executing mutating or export commands, review command arguments, and use dry-run mode for imports before committing changes.

## Reference(s):

- [Transaction command reference](references/commands.md)
- [Analytics command reference](references/analytics.md)
- [Management command reference](references/management.md)
- [Suanpan source repository referenced by the skill](https://github.com/yinguobing/suanpan.git)
- [Suanpan install script referenced by the skill](https://raw.githubusercontent.com/yinguobing/suanpan/main/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are proposals for user review and may affect local financial records if executed.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
