## Description: <br>
WIPO 小分子药物专利周报 searches WIPO PatentScope for newly published small-molecule drug patents, generates an HTML report, and uploads it to Google Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drtony1](https://clawhub.ai/user/drtony1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and drug-discovery teams use this skill to run weekly WIPO PatentScope searches for small-molecule patent activity, generate a summary report, and share it through Google Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local scripts that are referenced but not included in the artifact. <br>
Mitigation: Review or supply scripts/wipo_search.py and scripts/wipo_generate_report.py before installing or running the skill. <br>
Risk: Google Drive upload uses an existing rclone gdrive remote and can publish generated reports outside the local workspace. <br>
Mitigation: Use a dedicated low-privilege Google Drive destination and verify the rclone remote before enabling uploads. <br>
Risk: Weekly scheduled execution can run automatically after setup. <br>
Mitigation: Enable the cron schedule only when automatic uploads are intended, monitor initial runs, and keep an easy disable path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drtony1/wipo-patent-weekly) <br>
- [Target extraction rules](references/target-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; generated report artifacts are JSON and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files under wipo_reports/ and upload HTML output to Google Drive through rclone.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
