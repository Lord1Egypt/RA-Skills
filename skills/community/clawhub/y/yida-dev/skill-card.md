## Description: <br>
钉钉宜搭低代码开发助手。用于创建表单和自定义页面、编写 JS 动作面板、使用 JS-API、配置数据源、设计流程自动化。适用于宜搭表单开发、JS 代码调试、API 集成等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yize](https://clawhub.ai/user/yize) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill as a DingTalk Yida low-code development reference for form design, custom pages, JS action-panel snippets, JS-API usage, data-source configuration, workflow automation, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example API or workflow snippets may affect production Yida or DingTalk data if copied without checking app IDs, form IDs, and permissions. <br>
Mitigation: Verify identifiers, use least-privilege DingTalk/Yida permissions, and test create, update, and delete flows against non-production data before deployment. <br>
Risk: Temporary debugging helpers such as vConsole may remain enabled after troubleshooting. <br>
Mitigation: Remove temporary debugging scripts and development-only diagnostics before publishing or using the app in production. <br>
Risk: Generated snippets may reference placeholder field IDs or schemas that do not match the target Yida page. <br>
Mitigation: Review every fieldId, data source, and formula against the actual Yida visual builder configuration before applying the guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yize/yida-dev) <br>
- [JS-API complete reference](references/js-api.md) <br>
- [Troubleshooting guide](references/troubleshooting.md) <br>
- [TodoMVC tutorial](references/todomvc.md) <br>
- [Formula reference](references/formulas.md) <br>
- [Integration automation reference](references/integrations.md) <br>
- [Yida Help Center](https://docs.aliwork.com/) <br>
- [Yida Developer Center](https://developers.aliwork.com/) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [Yida OpenAPI documentation](https://developers.aliwork.com/docs/api/openAPI) <br>
- [Yida updates](https://docs.aliwork.com/docs/yida_updates) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only helper content; examples should be reviewed and adapted before use in a real Yida app.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
