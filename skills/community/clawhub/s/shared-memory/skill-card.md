## Description: <br>
Share memories and state with other users by creating users and groups, granting permissions, managing access control, and subscribing to changes through Ensue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christinetyip](https://clawhub.ai/user/christinetyip) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to manage shared Ensue memory spaces, users, groups, access grants, revocations, and memory-change subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse local Ensue credentials and make high-impact permission or deletion changes. <br>
Mitigation: Set ENSUE_API_KEY explicitly where possible and require clear user confirmation before deletes, org-wide grants, broad namespace patterns, or write/delete permissions. <br>
Risk: Credential values may be exposed during troubleshooting. <br>
Mitigation: Avoid printing or sharing raw API keys when diagnosing configuration issues. <br>


## Reference(s): <br>
- [Ensue](https://ensue-network.ai) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ENSUE_API_KEY and can call the Ensue API to change sharing permissions, users, groups, and subscriptions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
