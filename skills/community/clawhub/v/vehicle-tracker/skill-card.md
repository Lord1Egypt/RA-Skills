## Description:

Track vehicle expenses (gas, maintenance, parts) in Google Sheets and save related photos. Handles mileage, cost, category, and photo organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huchengtw](https://clawhub.ai/user/huchengtw)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to record vehicle fuel, maintenance, parts, and purchase expenses in Google Sheets or local Excel files, with optional photo organization for receipts or service records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local file handling and photo or Excel path configuration can write files into unintended locations.

Mitigation: Review configured photo and Excel directories before use and avoid pointing them at sensitive locations.

Risk: Formula-like vehicle, category, or description values may be written into spreadsheet fields.

Mitigation: Use trusted values for vehicle names, categories, and free-text fields, and review spreadsheet-bound data before execution.

Risk: Dry-run behavior may still update configuration before the dry-run output is returned.

Mitigation: Do not rely on dry-run as side-effect free until the config-write ordering is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huchengtw/skills/vehicle-tracker)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with JSON configuration examples and Python command-line invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write expense rows to Google Sheets or local Excel files and copy related photos when executed.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
