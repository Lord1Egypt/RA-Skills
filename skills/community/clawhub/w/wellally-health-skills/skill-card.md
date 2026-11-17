## Description:

Wellally Health Skills provides a modular personal health management suite for recording health data, analyzing trends and risks, generating reports, and supporting health-related tracking workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huifer](https://clawhub.ai/user/huifer)

### License/Terms of Use:


## Use Case:

External users and developers use this skill suite to add Claude Code health-management commands for personal health records, chronic disease tracking, women's and children's health, mental-health screening, medication safety checks, and health report generation. It is for health data management and reference guidance, not professional diagnosis, treatment, emergency triage, or medication decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and stores sensitive medical data in local files.

Mitigation: Use it only where local medical files are expected, obtain explicit user consent, and prefer no-history mode and deletion controls before broader use.

Risk: The skill can produce high-stakes health guidance across medication, pregnancy, pediatric, emergency, and mental-health contexts.

Mitigation: Do not rely on outputs for diagnosis, medication changes, dosing, emergency triage, pregnancy decisions, or crisis handling; require professional review for those cases.

Risk: Generated HTML reports may load third-party scripts.

Mitigation: Avoid opening generated reports while online unless remote scripts are removed or pinned with integrity checks; prefer local-only bundled report assets.

## Reference(s):

- [Wellally Health Skills ClawHub listing](https://clawhub.ai/huifer/skills/wellally-health-skills)
- [WellallyHealth product feature list](artifact/docs/feature-list-for-partners.md)
- [Claude Code skills documentation index](https://code.claude.com/docs/llms.txt)
- [Agent Skills open standard](https://agentskills.io)
- [WHO International Travel and Health](https://www.who.int/ith)
- [CDC Travelers' Health](https://www.cdc.gov/travel)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, Guidance, Configuration]

**Output Format:** [Markdown and text responses with structured JSON records and optional HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local health data files; generated reports may include third-party web assets.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
