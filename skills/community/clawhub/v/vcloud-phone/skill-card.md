## Description:

Helps authorized operators open the Volcengine cloud-phone admin platform, search instances by ID, inspect instance details, and download instance files such as logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjing0819](https://clawhub.ai/user/wangjing0819)

### License/Terms of Use:


## Use Case:

Employees and authorized production operators use this skill to navigate the cloud-phone administration platform, locate instances, view instance details, and retrieve requested instance files. It is intended for users who already have permission to operate on the target production resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on production cloud-phone instances and request arbitrary instance file downloads.

Mitigation: Install only for authorized production operators and require confirmation of the exact instance ID and file path before acting.

Risk: Downloaded instance files, including logs, may contain sensitive production data.

Mitigation: Treat copied downloads as sensitive data and keep them only in approved, access-controlled workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjing0819/skills/vcloud-phone)
- [Publisher profile](https://clawhub.ai/user/wangjing0819)
- [Cloud-phone admin platform](https://vcloud-admin.bytedance.net/vephone/overview)

## Skill Output:

**Output Type(s):** [Guidance, Text, Files]

**Output Format:** [Markdown or plain text operational guidance with browser-driven actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user confirmation of the target instance ID and file path before downloading production files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
