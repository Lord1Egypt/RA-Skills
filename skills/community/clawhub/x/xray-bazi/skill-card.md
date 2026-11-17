## Description:

Bazi guides an agent through Chinese Four Pillars birth-chart collection, calendar verification, chart construction, and traditional Bazi interpretation using bundled reference tables and classical summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to guide an agent through collecting birth details, verifying calendar pillars when possible, producing a Four Pillars chart, and returning a traditional Bazi analysis with caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects sensitive birth and profile details, including name, former name, birth date, birth time, gender, birthplace, and living or deceased status.

Mitigation: Use the skill only when the user intentionally requests Bazi analysis, ask only for details needed for that analysis, and avoid retaining or sharing the collected profile information.

Risk: The skill can send birth-date data to the apihz calendar API and may use apihz credentials in a URL, which can be exposed through logs or command history.

Mitigation: Prefer non-private or scoped credentials, avoid providing sensitive apihz credentials unless necessary, and redact API URLs or logs that contain credential parameters.

Risk: Global installation from a mutable branch can make future behavior depend on remote repository changes.

Mitigation: Install project-scoped copies and pin the source version or commit before using the skill in sensitive workflows.

Risk: Traditional Bazi analysis can produce misleading guidance if treated as medical, financial, or life-decision advice.

Mitigation: Present outputs as cultural or entertainment reference only and defer health, finance, and other consequential decisions to qualified professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/xray-bazi)
- [Wuxing tables](references/wuxing-tables.md)
- [Shichen table](references/shichen-table.md)
- [Dayun rules](references/dayun-rules.md)
- [Classical texts](references/classical-texts.md)
- [apihz specified-date calendar API](https://cn.apihz.cn/api/time/getzdday.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown conversation with tables and occasional shell command or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request birth and profile details; date-pillar results should be marked for review when calendar API validation is unavailable.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
