## Description: <br>
微信小程序云开发完整指南。包含项目结构、云函数开发、miniprogram-ci 部署命令、常见问题处理。适用于需要开发、部署微信小程序的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasondu](https://clawhub.ai/user/jasondu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to structure, configure, preview, upload, and deploy WeChat Mini Program cloud functions and front-end releases with miniprogram-ci. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private key paths and deployment identifiers appear in the skill guidance, so careless use could expose signing material or deploy to the wrong WeChat environment. <br>
Mitigation: Replace sample project identifiers, keep private keys out of source control, restrict key file permissions, prefer secret storage or protected CI variables, and manually confirm AppID, cloud environment, function name, version, and upload description before deployment. <br>


## Reference(s): <br>
- [WeChat Mini Program development environment information](artifact/references/config.md) <br>
- [ClawHub package page](https://clawhub.ai/jasondu/wechat-miniprogram-dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes WeChat Mini Program project structure, miniprogram-ci commands, cloud function snippets, configuration examples, and deployment script guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
