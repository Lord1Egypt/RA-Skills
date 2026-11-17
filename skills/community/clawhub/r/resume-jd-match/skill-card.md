## Description:

AI-powered JD-matched resume generator with native Chinese and English support that collects structured profiles, parses target job descriptions, performs match analysis, and outputs print-optimized HTML resumes with PDF export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[26048608982lp-ai](https://clawhub.ai/user/26048608982lp-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to tailor resumes to specific job descriptions, create resumes from structured profiles, optimize ATS wording, and generate Chinese or English resume outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores resume details, contact information, and possibly birth date in plaintext workspace files.

Mitigation: Use it only in a private workspace, avoid committing generated profile or resume files, and inspect generated HTML before opening or sharing it.

Risk: The artifact security description understates where the skill writes data.

Mitigation: Review expected outputs before deployment and confirm generated files remain within the intended workspace paths.

## Reference(s):

- [HTML Resume Template Guide](references/html-template-guide.md)
- [ClawHub skill page](https://clawhub.ai/26048608982lp-ai/skills/resume-jd-match)
- [Publisher profile](https://clawhub.ai/user/26048608982lp-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus self-contained HTML resume output and optional PDF export command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates reusable resume profile content and saves tailored resume artifacts in the workspace.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
