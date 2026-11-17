## Description:

Sports Betting Analyzer helps an agent produce sports betting analysis for NBA and football matches using basic statistics, simple prediction models, risk assessment, and explanatory reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nopedijah](https://clawhub.ai/user/nopedijah)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request match analysis, recommendation-style betting reports, recent-history summaries, and command-line runs for supported NBA and football scenarios. Outputs should be treated as decision support only, not verified wagering advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present gambling recommendations based on simulated or random data rather than verified live sports data.

Mitigation: Review outputs as entertainment or decision-support text only, verify data independently, and do not rely on generated percentages or recommendations for wagering.

Risk: The bundled scripts can store betting-analysis history and reports locally.

Mitigation: Review or disable local history and report saving before use when betting interests or team names are sensitive.

Risk: The runner can auto-install an unpinned dependency.

Mitigation: Pin and review dependencies before running the installer path in managed or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nopedijah/skills/sports-betting-analyzer)
- [README](artifact/README.md)
- [Development Notes](artifact/docs/DEVELOPMENT.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text reports with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local analysis history and optional report files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
