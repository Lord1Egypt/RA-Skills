## Description:

Use BatchJob HTTP APIs for strict upload validation, precheck, submit, polling, and cancellation with automatic file source resolution from file IDs, local paths, public URLs, or channel attachment paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocovs](https://clawhub.ai/user/cocovs)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to upload BatchJob input files, run prechecks, submit asynchronous jobs, poll job status, cancel jobs, and produce concise job summaries. It is intended for workflows where a BatchJob endpoint and bearer token are already configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically upload local files or URL-fetched content to a configured external BatchJob service with limited user confirmation or destination validation.

Mitigation: Use explicit file IDs or clearly selected workspace files, avoid sensitive local paths and private datasets, verify the BatchJob endpoint and token configuration, and require operator review before use in broadly privileged agent runtimes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cocovs/skills/ssy-batchjob-async-job)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include job IDs, status, progress, output summary URLs, validation guidance, and local template file paths when relevant.]

## Skill Version(s):

0.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
