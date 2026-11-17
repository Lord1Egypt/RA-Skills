## Description:

Submit completed work for a task on OpenAnt, including text descriptions, deliverable file uploads, and proof links when appropriate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and task workers use this skill to submit completed OpenAnt task work with a summary, uploaded deliverable files, or external proof links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local deliverable files and submit task work automatically.

Mitigation: Constrain use to explicit OpenAnt submission requests and review which files count as deliverables before execution.

Risk: Sensitive local outputs could be uploaded if they are treated as deliverables.

Mitigation: Exclude secrets, private data, and unrelated local outputs from the deliverable list before upload.

Risk: The skill invokes the OpenAnt CLI with `@latest`, so command behavior may change between reviews.

Mitigation: Use a pinned, reviewed CLI version when deploying the skill in controlled environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submission commands use structured JSON output and may include uploaded file keys, proof URLs, and text summaries.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
