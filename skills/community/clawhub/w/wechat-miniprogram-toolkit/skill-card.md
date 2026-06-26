## Description: <br>
Wechat Miniprogram Toolkit helps agents support full-stack WeChat mini-program development, including project initialization, cloud development, authentication, WeChat Pay, live streaming, analytics, sharing, TypeScript, cloud hosting, messaging, content safety, mini-app handoff, hardware APIs, Skyline rendering, WXS performance, CI/CD, and subpackage optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqlskills](https://clawhub.ai/user/sqlskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to ask an agent for WeChat mini-program architecture, implementation guidance, code, configuration, release automation, and subpackage analysis. It is most useful for mini-program projects that use WeChat cloud development, payments, messaging, content review, hardware capabilities, or CI/CD workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payment, refund, release, or admin workflows could trigger financial or production-impacting actions if copied directly. <br>
Mitigation: Require server-side authorization, audit logging, secret-manager storage, and manual approval before release, refund, payment, or other financial actions. <br>
Risk: Generated authentication, analytics, messaging, media, phone-number, upload, or hardware examples could mishandle identifiers, credentials, personal data, or Wi-Fi passwords. <br>
Mitigation: Apply consent and privacy notices, data minimization, encryption for credentials, and server-side access checks before use. <br>
Risk: Reference examples may be coherent but are not production-ready secure code. <br>
Mitigation: Treat outputs as implementation guidance and perform security review, platform policy review, and testing before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sqlskills/wechat-miniprogram-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/sqlskills) <br>
- [WeChat Mini Program Framework Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/) <br>
- [WeChat Developer Tools](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) <br>
- [WeChat Cloud Development Documentation](https://developers.weixin.qq.com/miniprogram/dev/wxcloud/basis/) <br>
- [WeChat Subpackages Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/subpackages/) <br>
- [WeChat Skyline Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/runtime/skyline/) <br>
- [WeChat Worklet Animation Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/view/skyline/worklet-animation.html) <br>
- [WeChat WXS Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/view/wxs/) <br>
- [miniprogram-ci](https://www.npmjs.com/package/miniprogram-ci) <br>
- [Project Initialization Guide](references/project-init.md) <br>
- [Cloud Development Guide](references/cloud-dev.md) <br>
- [Authentication Guide](references/auth.md) <br>
- [Payment Guide](references/payment.md) <br>
- [Subpackage Guide](references/subpackage.md) <br>
- [CI/CD Guide](references/ci-cd.md) <br>
- [Subpackage Analyzer](scripts/analyze_subpackages.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and generated source files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose WeChat mini-program project files, cloud functions, CI/CD workflows, payment flows, analytics instrumentation, messaging templates, content-review flows, and subpackage analysis output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
