## Description: <br>
TencentCloud Manager helps agents manage Tencent Cloud CVM, Lighthouse, and COS resources, including provisioning, operations, storage lifecycle tasks, and cost-oriented guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure Tencent Cloud credentials, inspect promotions and resource status, create CVM, Lighthouse, and COS resources, and manage routine start, stop, restart, upload, lifecycle, and cost-estimation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad Tencent Cloud credentials and can create, stop, restart, and alter resources. <br>
Mitigation: Use a dedicated Tencent Cloud sub-user, avoid master-account keys, restrict permissions to required services and regions, and require explicit human approval before resource-changing operations. <br>
Risk: COS permissions and examples include object deletion, lifecycle changes, and uploads that can affect stored data. <br>
Mitigation: Remove COS DeleteObject unless required, scope bucket permissions narrowly, and review lifecycle and upload operations before running them. <br>
Risk: Credential exposure or misuse could affect cloud resources and costs. <br>
Mitigation: Keep .env files out of version control with restricted permissions, rotate keys regularly, enable audit logging, and set budget alerts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ugpoor/tencentcloud-manager) <br>
- [Tencent Cloud CVM API Documentation](https://cloud.tencent.com/document/api/213) <br>
- [Tencent Cloud Lighthouse API Documentation](https://cloud.tencent.com/document/api/1170) <br>
- [Tencent Cloud COS API Documentation](https://cloud.tencent.com/document/api/436) <br>
- [Tencent Cloud CAM User Management](https://cloud.tencent.com/document/product/598) <br>
- [Tencent Cloud Sub-User Permission Configuration](https://cloud.tencent.com/document/product/598/10603) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON policy snippets, and configuration steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe Tencent Cloud API actions that create, stop, restart, upload, or alter cloud resources and should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
