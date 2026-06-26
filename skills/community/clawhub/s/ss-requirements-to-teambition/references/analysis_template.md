# AI 分析 + 任务创建模板

## 分析流程

1. 读取 `scripts/data/` 下最新的 JSON 文件
2. 对每个会话，按 `config.json` 中 `analysis.dimensions` 提取信息
3. 汇总后，用 `teambition-mcp__createTaskV3` 创建任务

## 任务创建规则

### 标题格式
按 `config.json` 中 `analysis.taskTitleFormat` 生成，默认 `[{ss_project_id}] {summary}`

### 必填字段（从 config.json 读取映射）
- `projectId`: `config.tb.projectId`
- `scenariofieldconfigId`: `config.tb.sfcId`
- `stageId`: `config.tb.stageId`
- `content`: 按 taskTitleFormat 生成

### 自定义字段
遍历 `config.tb.customfields`，按类型填充：

- **需求类型**（单选）：填 `cfId` + `valueId`
- **会话ID**（文本）：填 `cfId` + 会话 ID 字符串
- **项目ID**（文本）：填 `cfId` + SS 项目 ID

### 备注（note）
Markdown 格式，包含：
- 客户名称
- 问题描述
- 期望方案
- 最终结论
- 原始会话链接（如有）

## 去重

创建前先调用 `teambition-mcp__searchProjectTasksV3` 搜索是否已有相同会话 ID 的任务，避免重复创建。

## 示例调用

```json
{
  "projectId": "从config读取",
  "content": "[26485] 客户反馈AI回复不准确",
  "scenariofieldconfigId": "从config读取",
  "stageId": "从config读取",
  "customfields": [
    {
      "cfId": "69df253e95d7ece67f2d6e94",
      "value": [{"id": "69df253e95d7ece67f2d6e95", "title": "需求"}]
    },
    {
      "cfId": "69df25e800b8437a49b4840e",
      "value": [{"title": "session_abc123"}]
    }
  ],
  "note": "## 客户反馈\n\n**客户**: xxx公司\n**问题**: AI回复不准确\n**期望**: 提高准确率\n**结论**: 待跟进"
}
```