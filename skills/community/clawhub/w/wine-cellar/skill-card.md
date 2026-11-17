## Description:

Comprehensive wine cellar management skill for tracking inventory, providing meal-based recommendations, acting as a virtual sommelier, tracking consumption/purchases, and supporting barcode lookup to retrieve bottle details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzysb](https://clawhub.ai/user/fuzzysb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage a personal wine collection, look up bottle details by barcode, recommend wines for meals, and maintain local inventory records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wine inventory, purchase, and consumption notes are stored as local JSON files inside the skill directory.

Mitigation: Review the stored JSON before sharing the skill directory, avoid entering sensitive personal notes, and keep backups of inventory data.

Risk: The security evidence describes the release as an incomplete prototype with missing advertised helpers and import fixes needed before included scripts run reliably.

Mitigation: Test barcode lookup and pairing scripts locally before relying on them, and fix missing imports or helper scripts before operational use.

Risk: Barcode details, prices, scores, and pairing recommendations come from a small local database and rule-based matching.

Mitigation: Verify bottle metadata, market values, critic scores, and pairing advice against trusted sources when accuracy matters.

## Reference(s):

- [Wine database reference](references/wine_database.json)
- [ClawHub skill page](https://clawhub.ai/fuzzysb/skills/wine-cellar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional JSON file edits and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local JSON inventory and barcode cache files when the user asks for cellar operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
