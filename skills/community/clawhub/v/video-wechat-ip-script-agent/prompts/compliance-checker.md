任务：检测医美内容风险并输出安全改写版

输入内容：
- 标题：{{title}}
- 脚本：{{script}}
- 发布文案：{{caption}}
- 输出包配置：{{outputProfile}}
- 输出字段：{{outputFields}}

输出：
1. issues：风险点列表，每项包含 originalText, riskType, reason, suggestion
2. revisedVersion：对脚本或文案的安全改写版本
3. safeTitles：更安全的标题候选
4. safeCaption：更安全的发布文案

重点检查：
- 绝对化表达
- 效果承诺
- 诱导行为
- 夸大宣传
- 不适合公开传播的高风险医美话术

要求：
- 安全版本不能失去吸引力
- 修改建议必须可执行
- 输出字段优先按 `complianceOutputProfilesConfig[outputProfile]` 执行

{{outputRequirement}}
