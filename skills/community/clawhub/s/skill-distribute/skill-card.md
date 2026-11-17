## Description:

多平台内容自动分发工具。在小红书发布后，自动将内容同步到抖音、视频号、快手。支持自动处理图片尺寸、填写标题标签、处理验证码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and developers use this skill to configure Python-based workflows for adapting Xiaohongshu content, images, tags, and posting schedules for distribution to Douyin, WeChat Channels, and Kuaishou. Review in a sandbox or dry-run workflow before using real social accounts because the security evidence flags incomplete publishing behavior and account-safety risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package may report successful publishing even when real platform publishing is not implemented.

Mitigation: Require code review and a dry-run or sandbox validation before treating logs or status summaries as evidence of a completed post.

Risk: Real social account sessions, cookies, phone numbers, and CAPTCHA flows may be exposed or mishandled during browser automation.

Mitigation: Use test accounts first, restrict file permissions for account and cookie files, avoid storing credentials in shared environments, and clear session artifacts after testing.

Risk: Batch and scheduled workflows can repeatedly invoke posting logic without a final human review step.

Mitigation: Keep scheduled tasks disabled until publishing behavior is verified, and add explicit confirmation or dry-run review before any live batch execution.

Risk: CAPTCHA automation and high-frequency cross-posting can create account, compliance, and platform-policy risk.

Mitigation: Use manual CAPTCHA handling where appropriate, respect platform rules, lower posting frequency, and monitor accounts for rate-limit or verification challenges.

Risk: Dependencies are range-pinned and browser automation launches Chromium with reduced sandboxing.

Mitigation: Pin and review dependency versions, run in an isolated environment, and restore browser sandboxing unless the deployment environment explicitly requires otherwise.

## Reference(s):

- [API 文档](artifact/references/API.md)
- [平台适配指南](artifact/references/PLATFORM_GUIDE.md)
- [选择器配置](artifact/references/SELECTORS.md)
- [更新日志](artifact/references/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python commands, code snippets, YAML configuration, and operational warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces single-stream agent guidance for configuring and running local browser-automation scripts, batch distribution, and scheduled posting workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
