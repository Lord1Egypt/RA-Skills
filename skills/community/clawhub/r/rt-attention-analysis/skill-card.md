## Description:

Processes reaction-time and accuracy data from continuous-performance and sustained-attention tasks, computes adaptive fast/slow trigger thresholds, lapse metrics, RT variability, bootstrap/effect-size statistics, and optional RT time-series plots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guigui855](https://clawhub.ai/user/guigui855)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use this skill to process trial-level reaction-time datasets, identify fast or slow attentional states, detect lapses, and summarize sustained-attention performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python scripts over user-provided reaction-time datasets.

Mitigation: Install and run it only in environments where local script execution on those datasets is acceptable.

Risk: Generated CSV reports may preserve untrusted input values that spreadsheet software could interpret as formulas.

Mitigation: Treat exported CSV files as untrusted when source data is not fully trusted, and avoid opening them with spreadsheet formula execution enabled.

## Reference(s):

- [Methods Background - RT-Based Lapse Detection and Real-Time Triggering](references/methods.md)
- [ClawHub skill page](https://clawhub.ai/guigui855/skills/rt-attention-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus generated text, CSV, and optional PNG report files from the bundled scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The trigger script writes an annotated CSV; the analysis script writes summary text, metrics CSV, triggered CSV for single-subject data, and an optional RT time-series PNG.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
