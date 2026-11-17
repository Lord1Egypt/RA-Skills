## Description:

xlsx helps agents create, edit, analyze, clean, convert, and verify spreadsheet files such as .xlsx, .xlsm, .csv, and .tsv.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a spreadsheet file is the primary input or deliverable, including creating workbooks, editing existing spreadsheets, cleaning tabular data, converting formats, adding formulas, formatting sheets, and validating formula results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run LibreOffice and modify the user's LibreOffice macro profile.

Mitigation: Install and run it only in environments where LibreOffice profile changes are acceptable, and avoid using it on systems with important existing LibreOffice macros unless isolated.

Risk: In some Linux sandboxed environments, the skill can compile and use a native LD_PRELOAD shim for LibreOffice.

Mitigation: Review the bundled LibreOffice helper before installation and run the skill in a sandbox where native compilation and LD_PRELOAD use are acceptable.

Risk: Bundled Office tooling includes non-spreadsheet document helpers beyond the core spreadsheet workflow.

Mitigation: Limit use to spreadsheet tasks unless the bundled document tooling has been reviewed for the deployment environment.

Risk: Processing untrusted Office files can expose users to document parsing and macro-profile risks.

Mitigation: Avoid untrusted Office files, or process them in an isolated workspace with no sensitive LibreOffice profile state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fslong520/skills/sheetpro)

## Skill Output:

**Output Type(s):** [files, code, shell commands, configuration, guidance]

**Output Format:** [Spreadsheet files with concise Markdown guidance and JSON validation output when recalculation checks are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces spreadsheet deliverables and may use LibreOffice-based formula recalculation to report formula errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
