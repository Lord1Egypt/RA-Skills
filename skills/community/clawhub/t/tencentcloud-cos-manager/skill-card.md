## Description: <br>
Helps an agent manage Tencent Cloud COS buckets and objects, including uploads, downloads, lifecycle rules, storage class choices, permissions, encryption options, and cost estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure and operate Tencent Cloud COS storage for application data, static assets, backups, and archive workflows. It is most useful when an agent needs to generate commands or code for bucket management, object transfer, lifecycle policy, access control, and cost planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request broad Tencent COS permissions and operate across storage buckets and objects. <br>
Mitigation: Use a dedicated Tencent Cloud sub-user with permissions limited to required buckets, prefixes, and actions instead of name/cos:* on all resources. <br>
Risk: Delete, force-delete, lifecycle expiration, ACL, public-access, and download-destination operations can cause data loss or unintended exposure. <br>
Mitigation: Manually review these operations before execution, keep credentials private, and prefer reversible or scoped changes where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ugpoor/tencentcloud-cos-manager) <br>
- [COS API documentation](https://cloud.tencent.com/document/api/436) <br>
- [Tencent Cloud COS storage class documentation](https://cloud.tencent.com/document/product/436/33417) <br>
- [Tencent Cloud COS lifecycle documentation](https://cloud.tencent.com/document/product/436/30688) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, JSON, YAML, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Tencent Cloud COS operations that create, delete, upload, download, or reconfigure storage resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
