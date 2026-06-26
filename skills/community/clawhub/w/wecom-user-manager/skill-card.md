## Description: <br>
Enterprise WeCom user-management skill for adding user permissions, automatically activating first-time users, and managing the user lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
WeCom administrators and operations teams use this skill to add users, assign roles and store or regional access, and activate users when they first log in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change account access and role assignments in a WeCom environment. <br>
Mitigation: Use it only in a controlled WeCom deployment, require auditable administrator approval, and verify role, store, region, province, and city enforcement before production use. <br>
Risk: The security review notes missing external helper modules, so the full account-management behavior could not be reviewed from this artifact alone. <br>
Mitigation: Inspect or supply the missing helper modules before installing, and limit the WeCom MCP permissions available to the skill. <br>
Risk: User records and activation state may be stored in users.json or synchronized configuration files. <br>
Mitigation: Protect those files with appropriate access controls, review synchronization paths, and remove real test user details from public documentation or shared deployments. <br>


## Reference(s): <br>
- [API user manager reference](references/api-user-manager.md) <br>
- [WeCom developer documentation](https://developer.work.weixin.qq.com) <br>
- [ClawHub skill page](https://clawhub.ai/gwyang7/wecom-user-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with command examples and JSON-like response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and controlled access to the WeCom MCP user-management tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and .clawhub/manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
