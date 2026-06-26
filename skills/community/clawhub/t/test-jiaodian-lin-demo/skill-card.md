## Description: <br>
收费技能示例模板 - 带授权验证，演示如何在 ClawHub 发布付费技能 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lintqiu](https://clawhub.ai/user/lintqiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and ClawHub publishers use this skill as a paid-skill template that checks a local license key before running a small demo function. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may reuse a password or unrelated API key as SKILL_LICENSE_KEY. <br>
Mitigation: Use a dedicated license value only for this skill and avoid storing unrelated secrets in the environment variable. <br>
Risk: Generic trigger phrases may invoke the skill during unrelated paid-content conversations. <br>
Mitigation: Review triggers before installation and invoke the skill only when paid-skill authorization behavior is intended. <br>
Risk: The artifact demonstrates simple local hash-based license validation. <br>
Mitigation: Treat it as a template and replace the demo validation scheme with a production-grade authorization flow before relying on it for paid access control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lintqiu/test-jiaodian-lin-demo) <br>
- [Publisher profile](https://clawhub.ai/user/lintqiu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with shell environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILL_LICENSE_KEY for the demo function to proceed.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
