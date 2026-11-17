## Description:

Checks and fixes English abbreviations in briefing_package files so player-facing TRPG terms include Chinese full terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

TRPG content authors and game system maintainers use this skill to audit briefing_package and related rule or scenario files so player-facing abbreviations are expanded with Chinese full terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk abbreviation edits may affect multiple TRPG content files beyond the named briefing_package without a preview.

Mitigation: Use an explicit file list or request a dry-run diff before writeback, then review proposed changes before accepting them.

Risk: Loosely scoped edits could unintentionally change canonical rules, scenarios, or character sheets.

Mitigation: Limit runs to current formal files and exclude old, backup, draft, or superseded files from the edit set.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ice26985850/skills/trpg-abbr-check-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and proposed edits for TRPG briefing files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce proposed changes across .md and .yaml content files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
