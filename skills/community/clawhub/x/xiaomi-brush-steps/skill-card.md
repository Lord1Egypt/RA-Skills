## Description: <br>
华米运动(Zepp/小米运动)自动刷步数技能，支持多账号管理。当用户提到刷步数、修改运动步数、华米运动、小米运动、手环步数时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckxgzxa](https://clawhub.ai/user/ckxgzxa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to configure Zepp Life/Xiaomi fitness accounts and ask an agent to submit a chosen step-count range or schedule recurring step updates. It is intended for users who deliberately want automation that alters Zepp/Xiaomi step records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store Zepp/Xiaomi passwords in local configuration. <br>
Mitigation: Use a dedicated low-value account, do not reuse the password, keep config.json protected or deleted when not needed, and avoid publishing the configuration file. <br>
Risk: The skill alters Zepp/Xiaomi fitness step records and can automate recurring changes. <br>
Mitigation: Install and run it only when the user intentionally wants step-record modification, and create scheduled jobs only when the user knows how to remove them. <br>
Risk: The skill includes optional fake-IP behavior. <br>
Mitigation: Leave fake-IP behavior disabled unless the user has reviewed and accepted that behavior. <br>
Risk: The skill documentation mentions third-party credential-testing sites. <br>
Mitigation: Avoid third-party credential-testing sites unless the user has separately evaluated their trustworthiness. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckxgzxa/xiaomi-brush-steps) <br>
- [Publisher profile](https://clawhub.ai/user/ckxgzxa) <br>
- [Zepp token endpoint](https://api-user.zepp.com/v2/registrations/tokens) <br>
- [Huami login endpoint](https://account.huami.com/v2/client/login) <br>
- [Huami band-data endpoint](https://api-mifit-cn.huami.com/v1/data/band_data.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus shell commands and plain-text Brush Step Report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports per-account success or failure and the submitted step count range.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
