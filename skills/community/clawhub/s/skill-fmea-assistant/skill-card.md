## Description:

Supports FMEA 2019 analysis by helping users identify failure modes, calculate RPN values, assess risk levels, and track preventive actions across DFMEA, PFMEA, and SFMEA workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality, reliability, and engineering teams use this skill to structure FMEA work, score severity, occurrence, and detection values, calculate RPN, prioritize high-risk items, and maintain project records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports may preserve spreadsheet formulas from untrusted project data.

Mitigation: Disable spreadsheet formula execution when opening exported CSVs or neutralize formula-leading values before sharing.

Risk: The export script can write outside the documented output folder when project names contain path characters.

Mitigation: Use simple project names without slashes or path characters and run the skill in a fixed sandboxed output directory.

Risk: The release evidence security verdict is suspicious despite no network or credential behavior.

Mitigation: Review the skill before installation and scan any modified scripts before deployment.

## Reference(s):

- [FMEA 2019 Format Guide](references/fmea_format.md)
- [ClawHub Skill Page](https://clawhub.ai/duding-engicool/skills/skill-fmea-assistant)
- [Server-Resolved Source Repository](https://github.com/duding-engicool/skill-fmea-assistant)
- [Publisher Profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands plus JSON or CSV files from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and exports local FMEA project records under fmea_output/ during normal use.]

## Skill Version(s):

1.1.0 (source: frontmatter); release package version 0.1.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
