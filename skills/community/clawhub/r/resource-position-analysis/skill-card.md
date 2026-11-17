## Description:

Analyzes frontend resource-position conversion funnels from exposure, click, and business conversion data, using sequential substitution to attribute fluctuations and generate findings and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyi-ding](https://clawhub.ai/user/wuyi-ding)

### License/Terms of Use:

MIT-0

## Use Case:

Growth, product operations, and data analysts use this skill to compare resource-position funnel performance across day-over-day, week-over-week, or custom periods. It produces attribution findings and recommendations for banners, cards, popups, and similar frontend placements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The analysis script can auto-install missing Python dependencies without pinning exact versions.

Mitigation: Run it in a controlled virtual environment and preinstall reviewed, pinned versions of pandas and openpyxl.

Risk: Input workbooks may contain confidential business or user data.

Mitigation: Review Excel files for sensitive data and process them only in an approved environment.

Risk: The installation instructions include an unpinned npx command.

Mitigation: Use the command only when the installer source and registry configuration are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuyi-ding/skills/resource-position-analysis)
- [README](artifact/README.md)
- [Report template](artifact/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Excel .xlsx inputs and can write the report to stdout or a Markdown file.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
