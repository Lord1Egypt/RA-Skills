## Description: <br>
Manage Tencent Cloud COS buckets and files, including bucket creation, upload and download, lifecycle policies, access control, and cost optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure and manage Tencent Cloud COS storage workflows, including storage bucket operations, object transfers, lifecycle rules, and cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad Tencent Cloud COS permissions, including wildcard object-storage access. <br>
Mitigation: Use a dedicated sub-user key and scope policies to the specific buckets and actions required for the task. <br>
Risk: Bucket and object deletion paths, forced bucket clearing, and lifecycle expiration rules can permanently remove cloud data. <br>
Mitigation: Review bucket names, object keys, force-delete settings, and lifecycle expiration rules before running destructive operations. <br>
Risk: Credentials are loaded from environment variables and local .env files. <br>
Mitigation: Keep .env files out of source control, rotate keys regularly, and avoid using primary-account credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/tencentcloud-cos-storage) <br>
- [Tencent Cloud COS API documentation](https://cloud.tencent.com/document/api/436) <br>
- [Tencent Cloud COS storage classes](https://cloud.tencent.com/document/product/436/33417) <br>
- [Tencent Cloud COS lifecycle management](https://cloud.tencent.com/document/product/436/30688) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; helper methods return dictionaries, lists, strings, or console status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud COS credentials and the cos-python-sdk-v5 and python-dotenv packages.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
