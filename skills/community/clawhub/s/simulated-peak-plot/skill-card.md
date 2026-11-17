## Description:

Generates simulated Gaussian peak plots for chromatography, spectroscopy, and signal visualization, with support for single, clustered, merged, and negative peaks plus labels, axis customization, CSV import, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT

## Use Case:

Developers, educators, and analysts use this skill to create synthetic peak plots and sample datasets for chromatography, spectroscopy, teaching, testing, or signal-visualization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV and PNG artifacts may contain hidden deterministic markers.

Mitigation: Review generated artifacts before using them as trusted scientific data or clean public outputs, and prefer a version that removes hidden output modifications.

Risk: Very large peak configurations can exhaust local compute or produce oversized files.

Mitigation: Keep scan_rate, total points, and peak counts within the documented ranges, and reduce the time window or scan rate for large simulations.

Risk: The server security verdict is suspicious despite low declared permissions.

Mitigation: Review the skill before installation and treat generated data as synthetic until outputs are independently checked.

## Reference(s):

- [Feature Reference](references/features.md)
- [Parameter Reference](references/parameters.md)
- [Permissions Reference](references/permissions.md)
- [Test Report](references/test-report.md)
- [Changelog](references/changelog.md)
- [ClawHub Skill Page](https://clawhub.ai/ldxs001/skills/simulated-peak-plot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell and Python examples; generated PNG images and CSV data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Python dependencies for plotting; can read user-specified CSV input and write PNG or CSV outputs.]

## Skill Version(s):

2.13.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
