## Description:

每周检索 WIPO PatentScope 上新发布的小分子药物相关专利，生成 HTML 周报并上传到 Google Drive。

This skill is ready for commercial/non-commercial use.

## Publisher:

[drtony1](https://clawhub.ai/user/drtony1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and patent analysts use this skill to run a weekly WIPO PatentScope small-molecule drug patent search, create an HTML report, and upload the report to Google Drive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on unbundled workspace scripts for WIPO scraping and report generation.

Mitigation: Verify the referenced scripts in the target workspace before running the skill and use it only in trusted, access-controlled workspaces.

Risk: Broad natural-language triggers and scheduled execution can start scraping and upload workflows when they are not intended.

Mitigation: Narrow or disable triggers and cron scheduling unless automated weekly execution is explicitly desired.

Risk: The upload step can send generated reports to an unintended Google Drive destination if rclone is misconfigured.

Mitigation: Confirm the rclone remote, destination path, and account permissions before enabling uploads.

Risk: WIPO PatentScope scraping depends on browser rendering, session setup, and page structure that may change.

Mitigation: Review failure summaries, validate generated reports, and update the workspace scraper when WIPO page behavior changes.

## Reference(s):

- [Target extraction rules](references/target-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with bash commands, file paths, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local JSON and HTML report files under wipo_reports/ and uploads the HTML report when rclone is configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
