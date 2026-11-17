## Description:

Automatically finds remote jobs, scores them against a resume, identifies skill gaps, generates daily reports, and can prepare or submit applications with tailored resumes and WhatsApp confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajkiranvs](https://clawhub.ai/user/rajkiranvs)

### License/Terms of Use:


## Use Case:

External job seekers use this skill to automate remote job discovery, compare postings against their resume, review skill gaps, and manage application follow-up for supported technical role profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read resume/profile data, contact job sites, and submit applications externally.

Mitigation: Keep auto-apply disabled or use dry runs until every job, destination domain, tailored resume, and application action is explicitly reviewed.

Risk: Security evidence reports weak opt-out confirmation around applications.

Mitigation: Require positive per-job approval before submission instead of relying only on a skip window or absence of a SKIP reply.

Risk: Security evidence reports conflicting privacy disclosures for WhatsApp, SMTP, LinkedIn, and data-retention behavior.

Mitigation: Review configured integrations and generated local files before use, store credentials outside profile files, and disable integrations that are not needed.

## Reference(s):

- [Remote Job Hunter ClawHub page](https://clawhub.ai/rajkiranvs/skills/remote-job-hunter)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown reports, plain-text status messages, JSON state files, and generated resume documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads profile JSON and .docx or .pdf resumes; may create daily reports, pending/applied job logs, tailored .docx resumes, and WhatsApp preview or applied message files.]

## Skill Version(s):

1.2.0 (source: server release and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
