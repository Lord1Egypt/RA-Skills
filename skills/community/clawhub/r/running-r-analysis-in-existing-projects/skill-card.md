## Description:

Work inside an existing R project to extend analyses, modify scripts, run statistical models, update visualizations, and regenerate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Developers, data analysts, and researchers use this skill to extend, debug, and rerun analyses inside established R projects while preserving existing structure and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overwrite regenerated results, figures, or reports when rerunning an existing R analysis.

Mitigation: Use version control or backups before reruns and require the agent to identify output files before overwriting them.

Risk: The skill may install R packages while debugging or extending analyses.

Mitigation: Require the agent to show exact package installation commands before proceeding.

Risk: Changes to statistical models, plots, or reports can introduce misleading results if not reviewed.

Mitigation: Review proposed analysis changes and rerun outputs before relying on updated conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackkuo666/skills/running-r-analysis-in-existing-projects)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with R and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installs and regenerate or overwrite analysis outputs after review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
