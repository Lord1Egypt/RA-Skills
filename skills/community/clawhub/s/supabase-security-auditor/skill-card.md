## Description:

Audit Supabase projects for security - check Row Level Security policies, auth configuration, API exposure, storage rules, and edge function security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Supabase applications before launch, after configuration changes, or during security reviews. It helps identify weak Row Level Security policies, exposed API keys, unsafe auth settings, storage issues, and edge function risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project inspection can expose Supabase configuration, source files, and secret-like values in reports or transcripts.

Mitigation: Use the skill only on projects where agent inspection is acceptable, and redact service_role keys, passwords, JWTs, connection strings, and other secrets before sharing outputs.

Risk: Example discovery commands that search environment files or source code may print sensitive values.

Mitigation: Review command output locally and mask secret values before including findings in tickets, chat, or public reports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown audit report with severity-ranked findings, tables, and inline shell or SQL remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project file paths, security findings, and remediation steps; redact secrets before sharing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
