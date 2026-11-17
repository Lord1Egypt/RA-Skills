## Description:

swanlog pulls SwanLab cloud experiment metrics, config, metadata, requirements, and run information into a local directory and summarizes the run for inspection or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonwei1002](https://clawhub.ai/user/jasonwei1002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ML engineers use swanlog to fetch SwanLab experiment data from cloud runs to local files for inspection, archiving, comparison, diffing, and agent-assisted analysis without SSH access to the training machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's existing SwanLab login and saves run details locally, including files that may contain sensitive configuration, metadata, requirements, and metrics.

Mitigation: Install only when local SwanLab data export is intended, store outputs in an appropriate local directory, and review generated files before sharing them.

## Reference(s):

- [SwanLab](https://swanlab.cn)
- [ClawHub skill page](https://clawhub.ai/jasonwei1002/skills/swanlog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown summary plus local CSV, YAML, JSON, and text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a SwanLab run directory containing metrics.csv, config.yaml, metadata.json, requirements.txt, run_info.json, and brief.md.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
