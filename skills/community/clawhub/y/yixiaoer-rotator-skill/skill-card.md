## Description: <br>
Yixiaoer Rotator Skill helps agents rotate Yixiaoer publishing accounts by platform, synchronize available accounts, and persist local rotation state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lsx1205](https://clawhub.ai/user/lsx1205) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and publishing operators use this skill to select the next Yixiaoer account for each content platform, reducing repeated use of the same account during multi-account publishing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate yixiaoer-skill package for API calls. <br>
Mitigation: Install it only from a trusted source and inspect or pin the dependency before use. <br>
Risk: The skill requires a Yixiaoer API key and member ID. <br>
Mitigation: Use scoped, revocable credentials through environment variables and avoid storing them in skill files or logs. <br>
Risk: Automated account rotation can publish from an unintended account or platform if state is stale or misconfigured. <br>
Mitigation: Review the local rotation state and selected account before unattended publishing, especially after syncing or resetting accounts. <br>


## Reference(s): <br>
- [Yixiaoer Rotator Skill on ClawHub](https://clawhub.ai/lsx1205/yixiaoer-rotator-skill) <br>
- [Yixiaoer account rotation configuration](references/config.md) <br>
- [yixiaoer-skill dependency](https://clawhub.ai/yixiaoer-skill) <br>
- [Yixiaoer service](https://www.yixiaoer.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Configuration instructions] <br>
**Output Format:** [Markdown guidance with bash commands, CLI text output, account identifiers, and JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YIXIAOER_API_KEY and YIXIAOER_MEMBER_ID environment variables and a local yixiaoer-skill dependency.] <br>

## Skill Version(s): <br>
1.0.5 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
