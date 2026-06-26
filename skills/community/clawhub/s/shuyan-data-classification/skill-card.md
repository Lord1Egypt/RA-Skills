## Description: <br>
数安云智数据分类分级同步接口用于批量处理字段信息的分类分级，支持敏感数据识别、数据分类和数据分级，使用前需配置 API 地址和认证密钥。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianmo1997](https://clawhub.ai/user/jianmo1997) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, data governance teams, and security engineers use this skill to call a configured Shuyan classification service for batch classification and sensitivity-level assessment of database field metadata and sample values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Classification requests can upload field names, comments, sample values, and API tokens to the configured Shuyan endpoint. <br>
Mitigation: Use only trusted SHUYAN_API_URL endpoints, set your own SHUYAN_API_KEY, prefer HTTPS outside localhost, and send regulated or personal samples only when authorized. <br>
Risk: Batch JSON may contain sensitive or regulated sample data before it is sent to the service. <br>
Mitigation: Review batch input files before upload and minimize or remove unnecessary personal, financial, or regulated values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianmo1997/shuyan-data-classification) <br>
- [Publisher profile](https://clawhub.ai/user/jianmo1997) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python usage, JSON request examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API wrapper guidance and command output for synchronous single-field or batch data classification requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
