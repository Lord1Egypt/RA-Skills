## Description:

Manage Tencent Cloud COS buckets and objects, including bucket creation, file upload and download, lifecycle policies, access control, and cost optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Tencent Cloud COS storage workflows from an agent, including bucket administration, object transfers, lifecycle rules, and storage cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents broad Tencent Cloud COS permissions that can affect all buckets and objects.

Mitigation: Use a dedicated Tencent Cloud sub-user limited to the specific buckets and prefixes required for the task.

Risk: Credential handling guidance includes .env-based setup and troubleshooting that could expose secrets if copied into logs or shared outputs.

Mitigation: Keep credential files out of source control and logs, avoid printing .env contents, and rotate Tencent Cloud keys regularly.

Risk: Delete bucket, delete object, and lifecycle expiration operations can permanently remove COS data.

Mitigation: Review target bucket names, object prefixes, and lifecycle expiration rules before execution, and rely on separate Tencent Cloud recovery controls for important data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/tencentcloud-cos-storage)
- [Tencent Cloud COS API documentation](https://cloud.tencent.com/document/api/436)
- [Tencent Cloud COS storage classes](https://cloud.tencent.com/document/product/436/33417)
- [Tencent Cloud COS lifecycle management](https://cloud.tencent.com/document/product/436/30688)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud COS credentials and the COS Python SDK before cloud operations can run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
