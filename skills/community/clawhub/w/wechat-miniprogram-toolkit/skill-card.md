## Description:

Provides agent guidance and utilities for building WeChat Mini Programs, including project setup, cloud development, authentication, payments, live features, analytics, sharing, TypeScript, CI/CD, subpackage optimization, content safety, hardware APIs, and performance work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate, review, and optimize WeChat Mini Program projects and supporting configuration across app initialization, cloud services, payments, messaging, analytics, release automation, and package-size constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated payment, admin, CI, token, phone-number, and Wi-Fi code can affect sensitive credentials, privileged actions, or user data.

Mitigation: Treat these outputs as drafts and require security review, secret handling checks, and least-privilege validation before production use.

Risk: The skill under-controls persistent self-modification.

Mitigation: Do not allow automatic edits to SKILL.md or reference files without explicit human review and approval.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing and scan generated project changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moniq888/skills/wechat-miniprogram-toolkit)
- [WeChat Mini Program framework documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/)
- [WeChat Developer Tools download](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- [WeChat Cloud Development documentation](https://developers.weixin.qq.com/miniprogram/dev/wxcloud/basis/)
- [WeChat Mini Program subpackage documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages/)
- [WeChat Skyline runtime documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/skyline/)
- [WeChat Skyline Worklet animation documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/view/skyline/worklet-animation.html)
- [WeChat WXS documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxs/)
- [miniprogram-ci package](https://www.npmjs.com/package/miniprogram-ci)
- [Project initialization template](references/project-init.md)
- [Cloud development guide](references/cloud-dev.md)
- [Authentication guide](references/auth.md)
- [Payment guide](references/payment.md)
- [Subpackage strategy](references/subpackage.md)
- [CI/CD pipeline guide](references/ci-cd.md)
- [Content safety guide](references/content-safety.md)
- [Subpackage analysis script](scripts/analyze_subpackages.py)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, generated configuration, and analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated WeChat Mini Program source files, app.json snippets, CI/CD workflow drafts, and package-size analysis results.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and release changelog mention 1.6.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
