## Description:

Provides guidance, scripts, and CI/CD templates for developing, building, and publishing uni-app projects as WeChat Mini Programs with miniprogram-ci.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acxj](https://clawhub.ai/user/acxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to configure uni-app WeChat Mini Program builds, automate uploads or experience-version publishing, and troubleshoot miniprogram-ci and WeChat DevTools workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CI/CD workflow can upload, submit, or release WeChat Mini Program builds.

Mitigation: Use protected branches, manual approvals, and least-privilege release roles before enabling review or release modes.

Risk: WeChat private keys may be written to CI workspaces or passed through weakly scoped paths.

Mitigation: Keep keys only in CI secret stores, write them to temporary confined paths, delete them after use, and avoid arbitrary WEAPP_PRIVATE_KEY_PATH values.

Risk: The publishing flow installs and runs project dependencies during release automation.

Mitigation: Pin dependencies and use npm ci in controlled CI environments before running upload or release commands.

## Reference(s):

- [miniprogram-ci reference](references/miniprogram-ci.md)
- [CI/CD templates](references/cicd-templates.md)
- [WeChat DevTools CLI reference](references/wechat-devtools.md)
- [WeChat Mini Program documentation](https://developers.weixin.qq.com/miniprogram/)
- [miniprogram-ci official documentation](https://developers.weixin.qq.com/miniprogram/dev/devtools/ci.html)
- [uni-app documentation](https://uniapp.dcloud.io/)
- [GitHub Actions documentation](https://docs.github.com/en/actions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript, shell, JSON, YAML, and CI configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow steps that upload, submit, or release WeChat Mini Program builds.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
