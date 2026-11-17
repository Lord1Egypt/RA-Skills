## Description:

Skywork Excel helps agents create and analyze spreadsheets, tables, reports, charts, dashboards, and file conversions through the Skywork Excel backend service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route spreadsheet, table, report-generation, data-analysis, and file-conversion requests to Skywork Excel, including uploads of Excel, CSV, PDF, and image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User spreadsheets, PDFs, images, CSVs, and prompts are sent to Skywork's backend service.

Mitigation: Install only when this data transfer is acceptable and avoid submitting sensitive files without appropriate approval.

Risk: The skill depends on SKYWORK_API_KEY and evidence security guidance calls out credential handling concerns.

Mitigation: Use a scoped, rotatable key; store it in approved configuration; do not paste or print it in logs or chats.

Risk: Downloaded files and logs are written to the local workspace or temporary directories.

Mitigation: Run the skill in a workspace where generated outputs and logs cannot overwrite important files, and review downloads before use.

Risk: Evidence security marks the release suspicious because of remote file transfer and credential and file-write handling flaws.

Mitigation: Review the skill and scan results before deployment, avoid overriding --base-url, and limit installation to trusted environments.

## Reference(s):

- [Skywork API Key Setup Guide](references/apikey-fetch.md)
- [Skywork website](https://skywork.ai)
- [Skywork Excel ClawHub listing](https://clawhub.ai/gxcun17/skills/skywork-excel)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown status updates with shell commands, file paths, and downloadable spreadsheet or report outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files and OSS download URLs after remote processing; tasks can run for several minutes.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
