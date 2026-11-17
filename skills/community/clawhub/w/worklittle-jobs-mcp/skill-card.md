## Description:

Worklittle Jobs MCP lets agents search job listings, inspect job details, generate resumes and cover letters, and connect to Worklittle account and ATS workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to Worklittle for job search, job-detail review, resume and cover-letter generation, job applications, market insights, and employer ATS tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send job-search, resume, cover-letter, account, and ATS data to Worklittle.

Mitigation: Review API-key scopes, data-sharing expectations, and organizational policy before installing or using the Worklittle connection.

Risk: The skill can submit paid job applications and change company, job-listing, candidate, note, bookmark, or pipeline data.

Mitigation: Require explicit user confirmation before application submissions, per-application fees, or account and ATS changes.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/productivity/worklittle-jobs-mcp)
- [ClawHub skill page](https://clawhub.ai/johnsonbuilds/skills/worklittle-jobs-mcp)
- [Worklittle Jobs MCP GitHub repository](https://github.com/worklittle/jobs-mcp)
- [Worklittle MCP documentation](https://docs.worklittle.com/mcp)
- [Worklittle remote MCP endpoint](https://mcp.worklittle.com/)
- [Worklittle privacy policy](https://worklittle.com/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, Python, and shell command examples; MCP tool results may include job data, market summaries, and generated resume or cover-letter documents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Worklittle API key and may return or create account, application, resume, cover-letter, company, job-listing, candidate, note, bookmark, and pipeline data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
