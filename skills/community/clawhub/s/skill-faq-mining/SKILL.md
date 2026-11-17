---
name: faq-knowledge-mining
slug: faq-knowledge-mining
displayName: FAQ知识库挖掘
description: 从历史人工客服会话日志中提炼高频问题与最佳答案，生成标准FAQ格式的Markdown文档。支持Excel文件读取。适用于：更新知识库、提取高频问题、总结客服标准话术、优化客服响应质量。
version: 1.2.0
inputs:
  - name: log_file
    type: File
    required: true
    description: "脱敏后的客服会话日志，支持 .txt、.json、.md、.xlsx、.xls 等格式；必须包含发言角色（客户/客服）及时间顺序。"
  - name: options
    type: Object
    required: false
    description: "可选参数：top_n（提取高频问题的数量上限，默认20）、min_freq（最低频次阈值）、lang（输出语言，默认中文）。"
outputs:
  - name: faq_markdown
    type: File
    description: "生成的FAQ标准格式Markdown文件，按问题频次从高到低排序，每个条目为【问】+【答】结构。"
  - name: faq_summary
    type: String
    description: "FAQ统计摘要，包含提取的问题总数、高频问题Top10列表及数据覆盖说明。"
metadata:
  author: shibo
  category: content-generation
  tags: ["faq", "knowledge-base", "customer-service", "content-generation"]
  compatibility: Requires Python 3.10+ and pandas with openpyxl/xlrd for Excel reading.
---

# FAQ 知识库挖掘

从历史人工客服会话日志中提取高频问题与最佳答案，生成标准FAQ格式的Markdown文档。

## Quick Start

1. 准备脱敏后的客服会话日志文件（支持 `.txt`、`.json`、`.md`、`.xlsx`、`.xls` 格式），确保包含会话上下文、发言角色及时间顺序。
2. 如果是Excel文件，使用 `scripts/read_file.py` 脚本转换为文本格式。
3. 将数据内容输入进行FAQ提取和分析。

## 资源

- `scripts/read_file.py` - 读取Excel、Markdown、文本、JSON、CSV文件并转换为文本格式

## When to Use

- 从客服聊天记录中提取常见客户问题
- 总结标准客服响应话术
- 优化客服响应质量

## Workflow

1. **读取文件数据**：如果是Excel文件，使用 `scripts/read_file.py` 转换为文本格式；其他格式可直接使用。
2. **理解与分析输入数据**：读取脱敏后的客服会话日志，明确时间跨度与数据规模，提取客户首轮提问及后续问答交互。
3. **意图提取与最佳答案筛选**：
   - 将语义相同但表述不同的问题进行聚类，归一化为标准问并统计频次
   - 通过客户的下一句回复作为反馈指标评估解答质量
   - 选择通俗易懂、简洁明了的回复作为最佳答案
4. **生成标准FAQ文档**：按频次从高到低排序，输出为标准FAQ格式的Markdown文件。

## Input Requirements

- **数据源**：脱敏后的客服会话日志，必须包含会话上下文、发言角色（客户/客服）及时间顺序
- **数据范围**：明确时间跨度与数据规模，确保样本具有代表性
- **数据质量**：会话记录完整，包含客户首轮提问及后续问答交互

## Output Specifications

### 格式要求
- **文件格式**：`.md` 格式的Markdown文件
- **排序规则**：严格按照问题出现频次从高到低排序
- **结构规范**：每个FAQ条目遵循"第一行为问，第二行为答"的标准结构

### 风格要求
- **整体**：专业、客观、条理清晰
- **最佳答案**：保持优秀客服话术风格，专业且富有亲和力，通俗易懂

## Output Example

### 如何申请退款？
您好！请您在手机 APP 中点击【我的】-【全部订单】，找到需要退款的商品，点击【售后/退款】按钮，选择退款原因并提交即可。资金将在 1-3 个工作日内原路退回。

### 发票抬头填错了可以修改吗？
您好！如果发票已经开具，您可以在当月内联系我们作废原发票并重新开具。请您直接将正确的【发票抬头】和【税号】发送在这条对话中，我为您处理。

## Exception Handling

- **数据不足**：若会话日志数据量过小或时间跨度过短，提示用户补充数据
- **聚类失败**：若语义聚类效果不佳，提供人工校验接口或调整聚类阈值
- **反馈缺失**：若大量会话缺少客户下文反馈，降低反馈评估权重或提示补充完整记录

## Usage Notes

- 仅处理脱敏数据，严禁处理包含客户隐私信息的原始会话记录
- 生成的FAQ文档需经业务专家审核后方可导入知识库
- 建议定期运行本技能，持续更新FAQ文档以适应业务变化

## 安全与数据规范

- **数据脱敏**：上传数据前建议去除真实姓名/工号等敏感信息，或使用示例数据测试。
- **文件大小**：建议单个文件不超过 10MB，避免内存溢出。
- **Python 依赖**：scripts/read_file.py 依赖 pandas、openpyxl，安装命令：`pip install pandas openpyxl`