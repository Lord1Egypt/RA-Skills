## Description: <br>
Upload many files to S3 with automatic organization by first-character prefixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6mile-puppet](https://clawhub.ai/user/6mile-puppet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to prepare AWS CLI commands and run a bundled shell script that uploads local files into an S3 bucket organized by first-character prefixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads local files to a user-specified S3 bucket using AWS credentials. <br>
Mitigation: Use a narrowly scoped IAM role or access key limited to the intended bucket and prefix, and run with --dry-run before uploading. <br>
Risk: Files present in the selected source directory may be uploaded unintentionally. <br>
Mitigation: Review the source directory contents before execution and verify that it does not contain private or unrelated files. <br>
Risk: The documentation includes staging cleanup patterns that remove a directory tree. <br>
Mitigation: Use the bundled script's temporary staging behavior or confirm any manually configured staging directory is safe to delete before cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/6mile-puppet/s3-sort) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the AWS CLI and AWS credentials with access to the intended S3 bucket or prefix.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
