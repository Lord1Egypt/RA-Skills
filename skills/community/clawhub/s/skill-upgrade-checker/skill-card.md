## Description:

Check installed skills for available upgrades, interpret version changes and risk, and execute upgrades with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaowh3613](https://clawhub.ai/user/zhaowh3613)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to audit installed ClawHub skills, compare local and registry versions, review changelogs and upgrade risk, and execute confirmed updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update installed skills through the ClawHub CLI after approval.

Mitigation: Review the proposed version changes, risk rating, and exact `clawhub update` commands before confirming; choose `none` or specific skill names to avoid bulk changes.

Risk: Major upgrades can introduce breaking behavior.

Mitigation: Require individual confirmation for each major upgrade and review changelog or description changes before execution.

Risk: Registry or changelog data may be incomplete for some skills.

Mitigation: Mark unknown versions as skipped and recommend manual review when no changelog is available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaowh3613/skills/skill-upgrade-checker)
- [Publisher profile](https://clawhub.ai/user/zhaowh3613)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables, concise recommendations, confirmation prompts, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawhub CLI and explicit user confirmation before updates are executed.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
