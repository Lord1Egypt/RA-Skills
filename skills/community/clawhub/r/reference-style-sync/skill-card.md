## Description:

One-click synchronization and standardization of reference formats in literature management tools, intelligently fixing metadata errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and academic writers use this skill to standardize bibliographic records from Zotero, EndNote, and common interchange formats while repairing common citation metadata issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can overwrite any writable output path.

Mitigation: Review output paths before every run, use a dedicated output directory, and avoid overwriting existing files unless intended.

Risk: Processed bibliography metadata and exported CSV files may carry untrusted spreadsheet formulas.

Mitigation: Treat bibliography metadata as untrusted and be cautious opening exported CSV files in spreadsheet software until formula protections are added.

Risk: The authoritative security review marked the release suspicious and called for additional path, overwrite, extension, and CSV formula protections.

Mitigation: Apply those protections and remove the unnecessary dependency before broad use.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/reference-style-sync)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [Bibliography exports such as BibTeX, RIS, CSV, and JSON, plus markdown guidance with command and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in metadata repair, style conversion, deduplication, or quality-check-only modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
