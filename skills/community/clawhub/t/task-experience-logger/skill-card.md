## Description:

Task Experience Logger helps agents record task problems, solutions, lessons learned, tool validation notes, and long-term memory updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dawai2005](https://clawhub.ai/user/dawai2005)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to maintain structured task experience records while troubleshooting, optimizing workflows, and preserving reusable lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent task records may capture sensitive raw logs, screenshots, credentials, tokens, customer data, or private operational details.

Mitigation: Require explicit approval for persistent records and save sanitized summaries instead of raw diagnostic material.

Risk: Automatic long-term memory updates may preserve inaccurate or overly broad lessons without review.

Mitigation: Review proposed MEMORY.md updates before writing them and keep only concise, reusable lessons.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dawai2005/skills/task-experience-logger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown templates, structured notes, and memory-update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task reports, quick notes, lessons learned, tool validation records, common issue entries, and proposed MEMORY.md updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
