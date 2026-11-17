## Description:

Batch-parses resumes and job descriptions, uses AI to assess candidate-to-role fit, and produces structured Excel matching reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxffly](https://clawhub.ai/user/sxffly)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams, recruiters, and operators use this skill to compare batches of PDF or Word resumes against role requirements from JD documents and produce detailed and summary Excel reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive applicant data and can send full resume text to OpenClaw subagents or configured external model APIs.

Mitigation: Use only with candidate consent, disclose model providers, minimize resume data before processing, and define retention controls for generated reports, logs, and parsed JSON files.

Risk: Security evidence reports an unsafe entry point that loads code from outside the reviewed package.

Mitigation: Remove the external workspace import and require execution only from reviewed package files before using the skill with real candidate resumes.

Risk: Security evidence and artifact configuration indicate exposed API keys in bundled configuration.

Mitigation: Revoke the exposed credentials and replace them with user-provided secrets loaded from a secure configuration source before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxffly/skills/resume-jd-matcher)
- [config_resume_match.yaml](references/config_resume_match.yaml)
- [config_template.yaml](references/config_template.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus generated Excel workbooks and log files when the skill is executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Excel output includes detailed candidate requirement matches and a candidate summary sheet.]

## Skill Version(s):

2.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
