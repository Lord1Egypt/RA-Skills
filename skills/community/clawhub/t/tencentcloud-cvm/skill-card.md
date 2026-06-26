## Description: <br>
Creates and manages Tencent Cloud CVM instances, including lifecycle operations, promotion lookup, cost guidance, and security group setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure Tencent Cloud credentials, compare CVM purchasing options, and manage CVM instances across create, list, start, stop, restart, security group, and delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, stop, restart, configure, and delete Tencent Cloud infrastructure. <br>
Mitigation: Require manual review before create, stop, restart, security-group, disk, or delete operations. <br>
Risk: The documented permission policy is broad and grants wildcard access to CVM, VPC, and CBS resources. <br>
Mitigation: Use a dedicated sub-user and replace wildcard permissions with the narrowest required actions and resources. <br>
Risk: Cloud credentials are required for operation and could be exposed if mishandled. <br>
Mitigation: Keep credentials out of source control, use environment configuration, rotate credentials, and isolate dependencies in a virtual environment. <br>


## Reference(s): <br>
- [Tencent Cloud CVM API documentation](https://cloud.tencent.com/document/api/213) <br>
- [Tencent Cloud CVM product documentation](https://cloud.tencent.com/document/product/213) <br>
- [Tencent Cloud promotions center](https://cloud.tencent.com/act) <br>
- [Tencent Cloud CAM user management](https://cloud.tencent.com/document/product/598) <br>
- [Tencent Cloud API 3.0 Explorer](https://console.cloud.tencent.com/api/explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python, Bash, YAML, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
