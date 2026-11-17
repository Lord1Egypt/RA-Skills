## Description:

ZT Digital I18n 国际化组件,提供接口国际化、异常信息国际化、参数校验国际化及动态参数支持。支持 Properties 配置文件和数据库两种资源加载方式。适用于需要多语言支持的 Java Spring Boot 项目。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengzhi5](https://clawhub.ai/user/dengzhi5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add internationalization to Java Spring Boot services, including localized API responses, exception messages, validation errors, and dynamic message parameters from properties files or database resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding an unpinned Maven dependency can introduce supply-chain or compatibility risk.

Mitigation: Verify the Maven artifact source, pin an approved version, and resolve dependencies through a trusted repository or dependency-management policy.

Risk: Incorrect locale header formats, resource encoding, or missing keys can produce wrong or untranslated user-facing messages.

Mitigation: Use the documented locale-language header format, UTF-8 resource files, and deployment tests that cover key locales, fallback behavior, and dynamic parameter ordering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dengzhi5/skills/zt-i18n)
- [Java I18n Usage Example](artifact/templates/i18n_usage_example.java)
- [Chinese Properties Resource Example](artifact/templates/messages_zh_CN.properties)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with Java, XML, YAML, and properties examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference sample Java controller and properties resource templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
