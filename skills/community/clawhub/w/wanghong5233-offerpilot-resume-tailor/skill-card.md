## Description:

Generate, review, and export tailored application materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate tailored resume bullets, cover letters, and greeting messages for a job, review or regenerate drafts, and export approved materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-based curl templates can create unintended command execution risk if job_id or thread_id values are not safely validated or encoded.

Mitigation: Install only when the local service on 127.0.0.1:8010 is trusted, strictly validate identifiers, prefer structured HTTP calls or non-shell argument arrays, and confirm approve/export actions before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, files]

**Output Format:** [Markdown responses with JSON request bodies, curl command templates, and returned file path or download URL when export succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before approve/reject actions and surfaces API errors or invalid JSON for retry decisions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
