## Description:

Syncs WeRead highlights and notes into flomo with incremental deduplication, configurable today/date/all sync scopes, tag templates, local state tracking, and Markdown-based intermediate storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericxie777](https://clawhub.ai/user/ericxie777)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to move exported WeRead annotations into flomo while limiting sync scope and avoiding duplicate pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected WeRead highlights and notes are sent to the configured flomo webhook during non-dry-run syncs.

Mitigation: Use --dry-run first, verify the webhook is the user's own HTTPS flomo endpoint, and prefer today or date mode before all.

Risk: A leaked flomo webhook could allow unintended writes to the user's flomo account.

Mitigation: Keep the webhook outside the skill package and rotate it if it appears in shell history, logs, or process captures.

## Reference(s):

- [Formatting](artifact/references/formatting.md)
- [Publishing notes](artifact/references/publishing.md)
- [ClawHub skill page](https://clawhub.ai/ericxie777/skills/weread-to-flomo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated flomo note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run output, local deduplication state, and optional webhook posting.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
