## Description:

钉钉宜搭开发助手用于创建表单和自定义页面、编写 JS 动作面板、使用 JS-API、配置数据源并设计流程自动化。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yize](https://clawhub.ai/user/yize)

### License/Terms of Use:


## Use Case:

Developers and Yida builders use this skill to implement DingTalk Yida low-code forms, custom pages, JavaScript action-panel logic, data sources, OpenAPI integrations, formulas, and workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote script loading and debugging helpers may introduce untrusted code or expose production behavior.

Mitigation: Only load JavaScript from fully trusted, controlled origins and remove debugger or vConsole snippets before production release.

Risk: OpenAPI and automation examples can create, update, delete, or synchronize business data.

Mitigation: Test flows in a sandbox, scope credentials and operations narrowly, and require review before applying update or delete behavior to production data.

Risk: Webhook and AI integration patterns may share business or personal data with third-party services.

Mitigation: Perform privacy and data-sharing review before enabling webhook, OpenAPI, or AI workflow integrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yize/skills/yida-dev)
- [JS-API complete reference](references/js-api.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [TodoMVC tutorial](references/todomvc.md)
- [Formula functions](references/formulas.md)
- [Integration automation guide](references/integrations.md)
- [Yida help center](https://docs.aliwork.com/)
- [Yida developer center](https://developers.aliwork.com/)
- [DingTalk open platform](https://open.dingtalk.com/)
- [Yida OpenAPI documentation](https://developers.aliwork.com/docs/api/openAPI)
- [Yida updates](https://docs.aliwork.com/docs/yida_updates)
- [Yida example center](https://www.aliwork.com/o/coc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript, JSON, formula, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Yida field IDs, component schemas, OpenAPI paths, automation patterns, and debugging steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
