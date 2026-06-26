## Description: <br>
TencentCloud Lighthouse helps agents manage Tencent Cloud Lighthouse instances, promotions, images, lifecycle actions, and cost-aware configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect promotion plans, choose server images, create and manage Tencent Cloud Lighthouse instances, and validate credentials for a configured Tencent Cloud account. <br>

### Deployment Geography for Use: <br>
Global, subject to Tencent Cloud regional availability and the user's configured Tencent Cloud region. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, renew, stop, reboot, and delete Tencent Cloud Lighthouse resources. <br>
Mitigation: Use a dedicated Tencent Cloud subuser with the narrowest practical permissions, restrict regions and resources where possible, and require manual approval before create, delete, reboot, or renew actions. <br>
Risk: Cloud resource creation and renewal can incur costs. <br>
Mitigation: Review plan details before execution, configure budget alerts, and release idle resources promptly. <br>
Risk: Deleting or stopping instances can interrupt services or remove data. <br>
Mitigation: Confirm target instance IDs and keep current backups before deletion or shutdown. <br>
Risk: Tencent Cloud API credentials are loaded from environment variables. <br>
Mitigation: Do not paste credentials into chat or logs, keep .env files out of source control, and rotate credentials regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ugpoor/tencentcloud-lighthouse) <br>
- [Tencent Cloud Lighthouse API](https://cloud.tencent.com/document/api/1170) <br>
- [Tencent Cloud Promotions](https://cloud.tencent.com/act) <br>
- [Tencent Cloud Lighthouse application images](https://cloud.tencent.com/document/product/1170/38176) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-style text with Python and shell snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make Tencent Cloud API calls when used with configured credentials; destructive and cost-incurring actions should require user approval.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
