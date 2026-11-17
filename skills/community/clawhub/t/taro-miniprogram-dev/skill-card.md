## Description:

Taro + React + TypeScript 微信小程序开发框架技能，帮助代理初始化项目、创建页面和组件、搭建 services 请求层、配置 TabBar 与页面路由，并应用配套设计系统。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and maintain Taro 3, React, and TypeScript WeChat mini-program projects. It provides project setup commands, a reusable project template, page and routing guidance, a mockable services layer, and design-system references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use npx and npm install, which can introduce supply-chain risk if package versions are not pinned and reviewed.

Mitigation: Pin the Taro CLI and dependencies, use a lockfile, and review package changes before installation.

Risk: The helper initialization script accepts a project name and performs filesystem operations.

Mitigation: Validate or avoid arbitrary project names, and run setup in a normal non-privileged workspace.

Risk: API examples include placeholder backend endpoints and token storage patterns that may not satisfy a production privacy or security model.

Mitigation: Verify backend endpoints, token handling, authentication behavior, and privacy requirements before enabling real network calls.

## Reference(s):

- [API Design Reference](references/api-design.md)
- [Design System Reference](references/design-system.md)
- [Page Development Reference](references/pages.md)
- [WeChat Mini Program Sitemap Documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/sitemap.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash, TypeScript, JavaScript, SCSS, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project template files and shell commands for Taro mini-program setup and builds.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
