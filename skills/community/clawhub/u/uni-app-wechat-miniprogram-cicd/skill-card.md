## Description: <br>
Supports uni-app WeChat Mini Program development, builds, miniprogram-ci publishing, and CI/CD release workflows for GitHub Actions, GitLab CI, and Jenkins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acxj](https://clawhub.ai/user/acxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to configure uni-app WeChat Mini Program projects, generate build and publishing commands, and set up automated CI/CD workflows for experience, review, or release publishing modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat Mini Program publishing requires private key and AppID credentials that could expose release authority if mishandled. <br>
Mitigation: Store private keys only in CI secrets, never commit them or upload them as artifacts, and delete generated key files after each job. <br>
Risk: Automated review or release modes can publish changes beyond an experience build if workflows are triggered too broadly. <br>
Mitigation: Restrict workflows to protected branches and require manual approval before review or release modes run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acxj/uni-app-wechat-miniprogram-cicd) <br>
- [miniprogram-ci reference](references/miniprogram-ci.md) <br>
- [CI/CD templates](references/cicd-templates.md) <br>
- [WeChat DevTools CLI reference](references/wechat-devtools.md) <br>
- [WeChat Mini Program documentation](https://developers.weixin.qq.com/miniprogram/) <br>
- [miniprogram-ci official documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html) <br>
- [uni-app documentation](https://uniapp.dcloud.io/) <br>
- [GitHub Actions documentation](https://docs.github.com/en/actions) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, YAML, JSON, and pipeline configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI environment variable names, private key handling steps, miniprogram-ci API examples, and workflow templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
