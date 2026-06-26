## Description: <br>
云之家(YunZhijia)表单数据解析与构建技能，用于解析云之家表单JSON结构并支持推送数据解析和审批发起数据构建。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlifeng](https://clawhub.ai/user/jlifeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand YunZhijia form payloads, parse approval callback data from widgetMap and detailMap structures, and build form data for approval initiation APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discusses YunZhijia attachment and image file IDs, which could refer to sensitive business files. <br>
Mitigation: Process only YunZhijia form data and attachments the user is authorized to handle, and confirm before downloading attachments. <br>
Risk: Examples involving YunZhijia API access can encourage users to expose real access tokens in prompts or skill files. <br>
Mitigation: Use placeholders in shared prompts and files, and keep real YunZhijia access tokens out of skill documentation and conversation history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jlifeng/yzj-form-parser) <br>
- [控件类型详解](references/widget-types.md) <br>
- [明细表控件详解](references/detail-widget.md) <br>
- [附件控件详解](references/file-widget.md) <br>
- [YunZhijia file download endpoint](https://www.yunzhijia.com/docrest/doc/user/downloadfile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and Java code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no executable code or hidden behavior found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
