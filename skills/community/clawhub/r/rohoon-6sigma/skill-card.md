## Description:

Rohoon Six Sigma professional support for DMAIC/DMADV, SPC control charts, process capability, MSA analysis, DOE, FMEA, 5S/VSM, automotive quality management, process optimization, and supplier assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamhyzhu](https://clawhub.ai/user/williamhyzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, manufacturing teams, and agent developers use this skill to analyze process capability, control charts, measurement systems, designed experiments, and AIAG-VDA style quality reports for automotive and industrial quality workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance guidance may lead an agent to perform broad backups or stage many files at once.

Mitigation: Review maintenance steps before execution and scope any backup or git operation to the intended files.

Risk: The batch PDF generator may automatically open generated files.

Mitigation: Run batch report generation only in an environment where automatic file opening is acceptable.

Risk: Dependencies and statistical outputs may affect production quality decisions.

Mitigation: Use a virtual environment with pinned dependencies and independently validate report conclusions before audits or production use.

## Reference(s):

- [README](README.md)
- [Excel Import and Report Features](EXCEL_IMPORT_REPORT_FEATURES.md)
- [Process Capability Indices](references/capability-indices.md)
- [Control Charts Reference](references/control-charts.md)
- [Design of Experiments Guide](references/doe-guide.md)
- [Lean Six Sigma Tools Reference](references/lean-six-sigma-tools.md)
- [MSA Reference Guide](references/msa-reference.md)
- [ClawHub Skill Listing](https://clawhub.ai/williamhyzhu/rohoon-6sigma)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus optional JSON, PDF, Excel, and CSV artifacts when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include statistical analysis, report-generation commands, quality report files, and configuration guidance.]

## Skill Version(s):

1.8.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
