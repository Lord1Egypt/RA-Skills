## Description:

Records purchase commands in the form "\u91c7\u8d2d <date> <item name> <price>" into a desktop Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbei2007](https://clawhub.ai/user/linbei2007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators can use this skill to parse structured purchase messages and append date, item-name, and price fields to an Excel purchase log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports that crafted purchase text may cause unintended operating-system command execution through the command handler.

Mitigation: Review or patch the launcher to use argument-based process execution before installing or running the skill.

Risk: The skill writes user-provided item names and prices into an Excel workbook.

Mitigation: Sanitize item names before writing to Excel and confirm the workbook path before allowing writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbei2007/skills/purchase-record)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Markdown status message plus an Excel workbook row update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends purchase date, item name, and numeric price to purchase_record.xlsx.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
