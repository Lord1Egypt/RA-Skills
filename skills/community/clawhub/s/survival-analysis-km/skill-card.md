## Description:

Generates Kaplan-Meier survival curves, calculates survival statistics, and estimates hazard ratios for clinical and biological survival data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers, clinical researchers, and biomedical analysts use this skill to run Kaplan-Meier survival analysis on time-to-event CSV data, generate survival plots, compare groups, and summarize hazard-ratio and log-rank results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependencies are declared without pinned versions, which can change behavior across installs.

Mitigation: Install in an isolated environment and pin or lock dependencies before use.

Risk: The script writes fixed output filenames into the caller-supplied output directory and may overwrite existing files with those names.

Mitigation: Direct output to a fresh project-local directory and check for existing files before running.

Risk: Clinical or biomedical input data may be sensitive and statistical conclusions may affect downstream decisions.

Mitigation: Use least-privileged local execution, handle input data as sensitive, and have results reviewed by appropriate domain or biostatistical expertise.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/survival-analysis-km)
- [References and Resources for Survival Analysis](references/README.md)
- [Sample Survival Dataset](references/sample_data.csv)
- [lifelines Documentation](https://lifelines.readthedocs.io/)
- [scikit-survival Documentation](https://scikit-survival.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with command examples; generated analysis artifacts include PNG, PDF, CSV, and TXT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads caller-provided CSV survival data and writes Kaplan-Meier plots, survival statistics, log-rank results, hazard-ratio results, and a human-readable report.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
