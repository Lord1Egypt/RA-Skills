## Description:

Automates B2B cold email outreach by processing Apollo lead exports, verifying email addresses with Hunter.io, and uploading verified leads to Instantly campaigns with personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Growth teams and sales operators use this skill to configure and run a B2B cold email pipeline that turns Apollo lead data into verified Instantly campaign uploads. It is intended for users who are authorized to process prospect contact data and operate outbound email campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes and uploads prospect contact data to external services.

Mitigation: Use it only with authorized lead data, review applicable privacy and anti-spam obligations, and test with a small CSV before uploading at scale.

Risk: API keys are required for Hunter.io and Instantly, and the artifact uses a local configuration file pattern.

Mitigation: Keep API keys out of the repository, add a strong ignore rule for local config files, and prefer an environment or secret-management workflow for shared use.

Risk: Email verification failures may allow leads through if Hunter.io returns a non-200 response.

Mitigation: Change the verification step to fail closed on Hunter errors and require explicit confirmation before uploading verified leads to Instantly.

## Reference(s):

- [Cold Email Outreach ClawHub Skill Page](https://clawhub.ai/zero2ai-hub/skills/skill-cold-email-outreach)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript configuration and shell commands, plus CLI status output from the provided scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, campaign configuration guidance, customizable email sequence code, and command-line upload summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
