---
name: knowledge-base-health-check
slug: knowledge-base-health-check
displayName: 知识库健康度检查
description: 对比 FAQ 知识库与金牌客服对话记录，识别口径不一致、过时内容、缺失条目，生成差异报告与优化建议。反馈与定制联系:zenobiazizi.skills@foxmail.com
version: 1.0.0
inputs:
  - name: faq_file
    type: File
    required: true
    description: "FAQ 知识库文件（.xlsx, .xls, .md, .txt, .csv），含问题与标准答案。"
  - name: dialogue_file
    type: File
    required: true
    description: "金牌客服对话记录文件（.xlsx, .xls, .md, .txt, .csv），含客户提问与客服答复。"
outputs:
  - name: inconsistency_report
    type: String
    description: "Markdown 格式的差异报告，列出每条不一致/过时/缺失的条目及具体描述。"
  - name: suggestion_list
    type: String
    description: "Markdown 格式的优化建议清单，按优先级排序。"
metadata:
  author: shibo
  category: knowledge-management
  tags: ["knowledge-base", "faq", "quality", "audit", "customer-service"]
  compatibility: Requires Python 3.10+ and pandas with openpyxl/xlrd for Excel reading.
---

# 知识库健康度检查

通过对比 FAQ 知识库与金牌客服实际对话，发现知识条目与真实服务口径的差异，帮助团队及时更新知识库。

## Quick Start

1. 准备 FAQ 知识库文件（支持 .xlsx, .xls, .md, .txt, .csv）
2. 准备金牌客服对话记录文件（同上）
3. 使用 `scripts/read_file.py` 将文件转换为文本
4. 将转换后的文本输入，执行对比分析

## 资源

- `scripts/read_file.py` - 读取多种格式文件并转换为纯文本

## When to Use

- 定期审核知识库时效性
- 新政策上线后验证知识库同步情况
- 质检发现客服口径偏离时追溯根因
- 培训新员工前确保知识库准确

## Workflow

1. **读取文件**：使用 `scripts/read_file.py` 将 FAQ 文件和对话记录转换为文本格式。
2. **解析 FAQ**：从 FAQ 文本中提取每条知识条目（问题+标准答案），建立索引。
3. **解析对话**：从对话文本中提取每轮交互（客户问题+客服答复），按话题聚类。
4. **对比分析（核心）**：
   - **口径一致性**：对比客服答复与 FAQ 标准答案，检查是否完全一致、部分偏离或矛盾。
   - **过时检测**：识别 FAQ 中提及但对话中不再使用或已废止的政策/流程。
   - **缺失检测**：发现对话中频繁出现但 FAQ 未覆盖的新问题。
   - **模糊/不完整**：判断 FAQ 答案是否过于笼统，无法指导实际对话。
5. **生成报告**：
   - 差异报告：列出每条 FAQ 条目的健康状态（正常/不一致/过时/缺失/模糊），附证据引用（对话摘录）。
   - 建议清单：按影响程度（高/中/低）排序，提出具体修改建议（如更新话术、补充新条目、删除废止内容）。

## 分析原则

- **以对话为事实基准**：金牌客服的话术代表当前最佳实践，FAQ 应与之对齐。
- **定量+定性**：统计每条 FAQ 在对话中的命中率、匹配度，同时通过语义理解判断实质差异。
- **覆盖度评估**：计算对话中涉及的话题被 FAQ 覆盖的比例，识别知识盲区。

## 输出要求

提供两份 Markdown 文档：

### 1. 📋 差异报告
- 按 FAQ 条目编号/标题列出，包含：
  - 条目原文
  - 健康状态（✅一致 / ⚠️不一致 / 🕒过时 / ❌缺失 / 🔍模糊）
  - 具体说明（引用对话证据）
  - 影响评估

### 2. 💡 优化建议清单
- 按优先级（高→中→低）排列
- 每条建议含：操作类型（更新/新增/删除/细化）、目标条目、具体修改内容、预期效果

## 安全与数据规范

- **数据脱敏**：上传前建议去除客户隐私信息（姓名、电话、订单号等）。
- **文件大小**：建议单个文件不超过 10 MB。
- **依赖**：`scripts/read_file.py` 需 pandas、openpyxl，安装命令：`pip install pandas openpyxl`

## 约束

- **文件读取**：必须使用 `scripts/read_file.py` 读取文件，保证格式统一。
- **不编写代码**：直接输出分析结果，不展示中间推理过程。
- **客观公正**：基于实际对话内容判断，不臆造差异。