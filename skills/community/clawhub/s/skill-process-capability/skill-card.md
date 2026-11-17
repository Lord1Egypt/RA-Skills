## Description:

Analyzes manufacturing quality data by calculating CP, CPK, PP, PPK, PPM, distribution-fit results, and process visualizations for process capability assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and manufacturing analysts use this skill to evaluate whether production measurements meet specification limits, generate process capability metrics, and prepare quality analysis outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can overwrite existing files when output paths are reused.

Mitigation: Use a dedicated reports directory and choose output paths that do not replace important files.

Risk: Generated spreadsheets from untrusted data can preserve formula-like cells.

Mitigation: Review or sanitize formula-like cells before opening, sharing, or importing generated spreadsheets.

Risk: Untrusted or poorly prepared quality data can lead to misleading capability conclusions.

Mitigation: Use trusted input data, confirm specification limits, and review sample size and distribution assumptions before relying on results.

## Reference(s):

- [Process capability metrics guide](artifact/references/metrics_guide.md)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-process-capability)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-process-capability)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown or text guidance with JSON, CSV, Excel, and PNG file outputs when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include statistical summaries, capability indices, distribution-fit results, control charts, histograms, capability plots, and exported reports.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and release changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
