## Description:

Xlsx Pro helps agents create, edit, format, and validate spreadsheet files, including Excel formulas and optional LibreOffice-based recalculation for XLSX, XLSM, CSV, and TSV workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricobaboule](https://clawhub.ai/user/ricobaboule)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and spreadsheet-focused agents use this skill to generate or modify Excel-compatible workbooks with formulas, formatting, charts, and tabular data conversions. It is especially useful when the deliverable must be a spreadsheet file rather than a standalone script or document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recalculation path changes LibreOffice profile state.

Mitigation: Review before installing, use an isolated environment or VM, and avoid running it against important LibreOffice profiles until profile changes are explicit or isolated.

Risk: The LibreOffice helper can load a low-level LD_PRELOAD shim in sandboxed environments.

Mitigation: Inspect or disable the shim before use, and run recalculation only in a controlled environment where low-level helper loading is acceptable.

Risk: Spreadsheet files may be modified in place during recalculation.

Mitigation: Keep backups of important spreadsheets and test the workflow on copies before using it on production files.

Risk: Runtime dependencies are not pinned.

Mitigation: Pin Python dependencies and LibreOffice versions in deployment environments before relying on the skill for repeatable production output.

## Reference(s):

- [Xlsx Pro README](artifact/README.md)
- [Xlsx Pro skill definition](artifact/SKILL.md)
- [Xlsx Pro ClawHub page](https://clawhub.ai/ricobaboule/skills/xlsx-pro)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus generated spreadsheet files and JSON validation output from the recalculation script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports XLSX, XLSM, CSV, and TSV workflows; optional formula recalculation returns JSON with status, total errors, error summaries, and formula counts.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
