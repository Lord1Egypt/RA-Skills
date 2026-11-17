## Description:

Use when planning vacation days for the year: turns N PTO days into the maximum number of long weekends and extended breaks by bridging public holidays, warns about holiday blackout windows, balances consumption across quarters, and exports the full year plan with ICS calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Employees and managers with a PTO budget use this skill to plan time off around supported public holidays and weekends. It identifies bridge opportunities, flags generic blackout windows, and can export planned dates to an ICS calendar file.

### Deployment Geography for Use:

United States, United Kingdom, Germany, and France (generic public-holiday calendars)

## Known Risks and Mitigations:

Risk: Holiday dates and assumptions may differ by region or employer, making a proposed plan inaccurate for the user's situation.

Mitigation: Check holidays against the relevant local calendar and confirm employer rules, especially Good Friday in French plans, before booking travel or importing events.

Risk: Exporting an ICS file can overwrite an existing file if its path is reused.

Mitigation: Choose an export filename that will not overwrite a file you need.

## Reference(s):

- [PTO Planning Reference](references/pto-strategy.md)
- [PTO Maximizer on ClawHub](https://clawhub.ai/voronindenis5/skills/pto-maximizer)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, JSON, Files]

**Output Format:** [Plain-text vacation plan; optional JSON output or ICS calendar file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans are based on the selected country, year, PTO budget, and optional planning preferences.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
