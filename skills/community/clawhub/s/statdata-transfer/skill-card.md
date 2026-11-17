## Description:

Reads and converts 50+ statistical and clinical-trial data formats while preserving variable labels, value labels, and missing-value metadata where supported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Developers, data analysts, and clinical-data teams use this skill to inspect, convert, and round-trip statistical data files such as SPSS, Stata, SAS, R, Excel, Parquet, HDF5, JSON, and CSV while understanding metadata preservation limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and writes local statistical data files, and some discovery behavior may touch broader file sets than expected.

Mitigation: Use explicit input and output paths and run it from directories that do not contain unrelated sensitive files.

Risk: Some R, Minitab, and EpiData paths can invoke a local R interpreter when explicitly enabled.

Mitigation: Keep allow_r_exec disabled for untrusted files and enable it only for files from trusted sources.

Risk: Optional dependency installation can fetch packages when the user asks for installation.

Mitigation: Install dependencies in an isolated environment with reviewed package versions.

Risk: Conversions may create sidecar metadata files or backup files alongside requested outputs.

Mitigation: Choose output directories deliberately and review generated metadata and backup files after conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/medstatstar/skills/statdata-transfer)
- [Project homepage](https://github.com/medstatstar/statdata-transfer)
- [README](https://github.com/medstatstar/statdata-transfer/blob/main/README.md)
- [Chinese README](https://github.com/medstatstar/statdata-transfer/blob/main/README_zh-CN.md)
- [Usage examples](references/usage_examples.py)
- [New formats architecture analysis](references/new_formats_architecture_analysis.json)
- [v1.4 implementation summary](references/v1.4_implementation_summary.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown responses with Python snippets, shell commands, conversion guidance, and optional converted data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write requested output files, sidecar metadata files, and backup files for some overwrite paths.]

## Skill Version(s):

2.2.1 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
