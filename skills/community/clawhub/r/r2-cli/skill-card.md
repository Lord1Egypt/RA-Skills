## Description:

Minimal Python CLI for secure upload, download, list, and delete operations on Cloudflare R2 storage using AWS Signature V4 authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zororaka00](https://clawhub.ai/user/zororaka00)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Cloudflare R2 object storage from a Python command-line workflow. It supports bucket object upload, download, listing, and deletion with credentials supplied through environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Cloudflare R2 credentials and can perform write or delete actions on remote objects.

Mitigation: Use narrowly scoped R2 keys, avoid broad delete or write permissions unless needed, and rotate or revoke credentials according to the deployment policy.

Risk: Download paths and delete commands can overwrite local files or remove remote objects immediately.

Mitigation: Review target file paths and object keys before running download or delete operations, especially in automated agent workflows.

Risk: Dependencies and CLI execution can affect the local runtime environment.

Mitigation: Install dependencies in an isolated environment and review the skill before installing or executing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zororaka00/skills/r2-cli)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and Python CLI usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Cloudflare R2 environment variables for account ID, access key, secret key, bucket, and optional region.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
