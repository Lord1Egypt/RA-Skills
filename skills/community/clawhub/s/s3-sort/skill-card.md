## Description:

Upload many files to S3 with automatic organization by first-character prefixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6mile-puppet](https://clawhub.ai/user/6mile-puppet)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to upload local files to an S3 bucket while grouping objects into first-character prefixes for simpler browsing and management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk S3 upload behavior can move more data than intended.

Mitigation: Use a dedicated source directory, inspect its contents before execution, and run with --dry-run before uploading.

Risk: AWS credentials may allow broader S3 writes than the intended bucket or prefix.

Mitigation: Use least-privilege AWS credentials restricted to the target bucket and prefix.

Risk: Weak argument handling can make untrusted option values risky, especially for --storage-class.

Mitigation: Avoid passing untrusted values to --storage-class and review command arguments before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/6mile-puppet/skills/s3-sort)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AWS CLI credentials and an existing target S3 bucket.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
