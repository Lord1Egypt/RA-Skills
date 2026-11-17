## Description:

Enterprise WeChat user management skill for adding user permissions, automatically activating first-time users, and managing the user lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Administrators and WeCom workspace operators use this skill to add users, assign role and store permissions, and activate first-time users in an Enterprise WeChat deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the release as suspicious because account state can be granted or changed through under-scoped, partially missing code paths.

Mitigation: Deploy only in a controlled WeCom environment after confirming missing dependency modules, import paths, activation authentication, and audit logging.

Risk: The skill behavior depends on synchronizing users.json between workspace and plugin locations, which can create stale or inconsistent permissions if unmanaged.

Mitigation: Define and test an approved users.json synchronization process before enabling user activation or permission changes.

## Reference(s):

- [API User Manager Reference](artifact/references/api-user-manager.md)
- [ClawHub Skill Page](https://clawhub.ai/gwyang7/skills/wecom-user-manager)
- [Enterprise WeChat Developer Documentation](https://developer.work.weixin.qq.com)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Configuration]

**Output Format:** [Natural-language responses, confirmation-card content, and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update Enterprise WeChat user and permission configuration state.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
