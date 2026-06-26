## Description: <br>
TencentCloud OPS helps agents manage Tencent Cloud CVM instances and COS object storage, including resource creation, deletion, status checks, credential validation, and configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure Tencent Cloud credentials, manage CVM compute resources, manage COS buckets and files, estimate operating cost, and generate operational commands or Python examples for Tencent Cloud workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live Tencent Cloud operations, including creating, stopping, deleting, and configuring CVM and COS resources. <br>
Mitigation: Use a dedicated Tencent Cloud sub-user, restrict permissions to required regions and resources, and manually review every stop, delete, or release operation before execution. <br>
Risk: The documented setup uses Tencent Cloud API credentials and environment variables. <br>
Mitigation: Keep secrets out of Git, avoid main-account keys, rotate credentials regularly, and store credentials only in local environment configuration. <br>
Risk: The security evidence reports broad cloud-control permissions and destructive actions without built-in safeguards. <br>
Mitigation: Apply least-privilege CAM policies, avoid finance and billing permissions, set budget alerts, and monitor created resources for idle spend. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/tencentcloud-ops) <br>
- [Tencent Cloud API documentation](https://cloud.tencent.com/document/api) <br>
- [Tencent Cloud CVM API](https://cloud.tencent.com/document/api/213) <br>
- [Tencent Cloud COS API](https://cloud.tencent.com/document/api/436) <br>
- [Tencent Cloud CAM user management](https://cloud.tencent.com/document/product/598) <br>
- [Tencent Cloud API 3.0 Explorer](https://console.cloud.tencent.com/api/explorer) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Tencent Cloud CLI commands, Python SDK examples, environment variable guidance, cost estimates, and review notes for destructive operations.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
