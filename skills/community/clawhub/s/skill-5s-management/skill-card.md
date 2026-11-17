## Description:

Provides 5S management standards, visual management design support, on-site issue diagnosis, and report-generation guidance across Seiri, Seiton, Seiso, Seiketsu, and Shitsuke workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, quality, and site-management teams use this skill to query 5S standards, design visual management practices, diagnose workplace 5S issues, and prepare improvement reports. Developers or analysts may also use the included script guidance to turn trusted inspection JSON into an HTML 5S report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may execute browser content if untrusted inspection JSON is inserted into report fields.

Mitigation: Use only trusted inspection JSON, or update the report generator to HTML-escape every data field before generating reports.

Risk: Report output paths can overwrite existing files.

Mitigation: Choose output locations deliberately and review the destination path before running the report generator.

Risk: The documented ad hoc dependency installation command does not pin reviewed package versions.

Mitigation: Install Python dependencies from a reviewed, pinned dependency file before using the script in a managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-5s-management)
- [Server-resolved source repository](https://github.com/duding-engicool/skill-5s-management)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables, JSON examples, shell command examples, and optional generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report generator reads inspection JSON and writes an HTML file with embedded charts.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
