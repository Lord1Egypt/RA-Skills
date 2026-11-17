## Description:

Convert JSON, YAML, or TSV files to standardized CSV format with automatic header detection and consistent output for easy data analysis and processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Data analysts, researchers, and engineers use Quickcsv to convert JSON, YAML, or TSV inputs into standardized CSV for analysis, processing, or transfer between tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using -o writes to a selected path and may replace an existing file.

Mitigation: Choose output paths deliberately and avoid overwriting important files without a backup or review.

Risk: CSV generated from untrusted input may contain formula-like cells that spreadsheet software could evaluate.

Mitigation: Review or sanitize untrusted data before opening generated CSV files in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/skills/quickcsv)
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with bash command examples and CSV output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tool can write CSV to a selected output path or stream CSV to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
