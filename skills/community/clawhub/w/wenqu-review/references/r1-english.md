# R1：英文术语检查

调用工具：**Bash grep**、`language/glossary.md`、豁免列表

## 执行步骤

1. `grep -n "[A-Za-z]{4,}" 文章路径`，找正文中的英文词（排除代码块行、img 标签行、画图提示行）
2. 逐条对照豁免列表：在列表里的跳过
3. 不在豁免列表的词：
   - **首次出现**：是否给了「中文名（英文）」格式？没给的报问题
   - **后续出现**：是否还在用英文？是的报问题
4. 对照 `language/glossary.md`：文章里的中文译名是否和词汇表一致？不一致的报问题

## 豁免词汇（不翻译，也不加括号解释）

| 词汇 | 说明 |
|------|------|
| Token | 不写"词元" |
| LLM | 不展开翻译 |
| MCP | 不写"模型上下文协议" |
| API、SDK | 不展开翻译 |
| Agent | 可用，也可写"智能体"，视语境 |
| ReAct | 不展开翻译 |
| hook | 不写"钩子"——中文技术社区直接说 hook |
| prompt | 不写"提示词" |
| System Prompt | 专有名词，直接用 |
| embedding | 不写"嵌入向量" |
| JWT、OAuth、SSO | 认证协议名 |
| Redis、gRPC、Kafka、PostgreSQL | 广泛使用的技术产品名 |
| DM | Direct Message 缩写，行业通用，用"私信" |

判断标准：中文技术社区习惯直接用英文表述的词，不翻译，也不加括号解释。

## 常见需要处理的类型

| 类型 | 反例（不允许） | 正例 |
|------|------------|------|
| 组件名 | Derivative、IngestionService | 派生节点（Derivative）、摄取服务（IngestionService） |
| 人名 | Tulving | 图尔文（Endel Tulving） |
| 操作命令 | ADD、DELETE | 新增（ADD）、删除（DELETE） |
| 技术术语 | Cross-Encoder | 交叉编码器（Cross-Encoder） |

## 报告格式

`行号 | 当前写法 | 候选改法`，每条给 1-2 个候选，让用户选。

特别检查：搜索"钩子"，确认豁免词汇没有被误译。
