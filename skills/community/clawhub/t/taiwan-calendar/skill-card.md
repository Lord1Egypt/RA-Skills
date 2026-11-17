## Description:

Taiwan calendar query for accurate working day/holiday information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigfoot](https://clawhub.ai/user/pigfoot)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to answer Taiwan date, working-day, holiday, make-up workday, and deadline-calculation questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar answers depend on external data endpoints, including a mutable mirror and a fallback source with weaker TLS verification.

Mitigation: For deadline-critical use, verify important dates against an official Taiwan source before acting on the result.

Risk: The skill runs a Python script through Bash, installs Python dependencies through uv, and caches calendar JSON in the system temp directory.

Mitigation: Install only in environments where this execution, dependency installation, network access, and local temp-directory caching are acceptable.

## Reference(s):

- [Taiwan Calendar skill page](https://clawhub.ai/pigfoot/skills/taiwan-calendar)
- [Taiwan government calendar data mirror](https://cdn.jsdelivr.net/gh/ruyut/TaiwanCalendar/data/{year}.json)
- [New Taipei City open data fallback](https://data.ntpc.gov.tw/api/datasets/308DCD75-6434-45BC-A95F-584DA4FED251/json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with Traditional Chinese calendar results and inline shell commands when manual execution is useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs reflect Taiwan's Asia/Taipei timezone and depend on external calendar data availability.]

## Skill Version(s):

0.0.1 (source: frontmatter, README, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
