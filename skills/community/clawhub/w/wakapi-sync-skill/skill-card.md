## Description: <br>
Daily Wakapi (WakaTime-compatible) summary to local CSV files; fetches today's stats and appends or updates CSVs for totals, top projects, and top languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosformula](https://clawhub.ai/user/cosformula) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and personal analytics users use this skill to export daily Wakapi coding activity into local CSV datasets for reporting, dashboards, or archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Wakapi API key. <br>
Mitigation: Use a trusted Wakapi instance, prefer HTTPS for WAKAPI_URL, and provide only the API key needed for this export workflow. <br>
Risk: The script creates or replaces its named CSV files in the configured output folder. <br>
Mitigation: Set WAKAPI_OUT_DIR to a dedicated directory for this skill and review or back up existing CSV files before first use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cosformula/wakapi-sync-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/cosformula) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, API calls, Text] <br>
**Output Format:** [CSV files plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily-total.csv, daily-top-projects.csv, and daily-top-languages.csv in WAKAPI_OUT_DIR.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
