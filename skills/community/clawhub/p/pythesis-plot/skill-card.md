## Description:

Python scientific plotting tool for thesis and dissertation workflows that analyzes uploaded CSV, Excel, or text data, recommends chart plans, waits for confirmation, and generates publication-oriented figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlzc](https://clawhub.ai/user/stephenlzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and students use this skill to turn tabular research data into chart recommendations, analysis reports, reproducible Python plotting code, and 300 DPI scientific figures for academic writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads uploaded datasets and stores local copies, generated reports, plot configuration, code, and figures on disk.

Mitigation: Use a dedicated output folder, avoid sensitive datasets unless local storage is acceptable, and clean generated files according to the user's data retention needs.

Risk: The security summary says the config-based plot generator can write files outside the intended output folder.

Mitigation: Review generated plot_config.json before running generation and use a constrained working directory or sandbox for untrusted configs.

Risk: The workflow installs and runs local Python dependencies for data processing and plotting.

Mitigation: Use a virtual environment with pinned dependencies before running the scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stephenlzc/skills/pythesis-plot)
- [Installation Guide](artifact/docs/installation.md)
- [Workflow Guide](artifact/references/workflow_guide.md)
- [Chart Types](artifact/references/chart_types.md)
- [Style Guide](artifact/references/style_guide.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown analysis and recommendations, JSON plot configuration, Python code, and generated PNG/PDF figure files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs are organized in timestamped local directories and include copied input data, analysis reports, plot configuration, plotting code, and figures.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
