## Description:

Fetches today's Wakapi coding statistics and appends or updates local CSV summaries for totals, top projects, and top languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosformula](https://clawhub.ai/user/cosformula)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to automate daily exports of Wakapi or WakaTime-compatible activity data into local CSV files for personal analytics, reporting, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Wakapi API key to fetch activity data from the configured server.

Mitigation: Set WAKAPI_URL to a trusted HTTPS Wakapi server and prefer a read-only or least-privileged API key if available.

Risk: The skill writes CSV files to the configured output directory, and generated CSVs may be opened by spreadsheet applications that evaluate formulas.

Mitigation: Use a trusted WAKAPI_OUT_DIR and be cautious when opening generated CSV files in spreadsheet applications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosformula/skills/wakapi-sync-skill)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Text]

**Output Format:** [CSV files and plain-text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WAKAPI_URL, WAKAPI_API_KEY, and WAKAPI_OUT_DIR; writes daily-total.csv, daily-top-projects.csv, and daily-top-languages.csv.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
