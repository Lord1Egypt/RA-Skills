# ThinkTank Skill Finder 维护说明

更新时间：2026-04-14

本文档用于说明这份 Skill 清单的研究场景划分、技能包定义、主数据表字段，以及质量检查与维护规则。

## 智库研究场景

### 信息获取

对应研究任务中的资料入口阶段，重点覆盖：

- 网页抓取
- 学术检索
- 新闻与行业动态获取
- 外部证据和来源发现

### 调研执行

对应问卷、访谈、开放题整理和调研材料回收分析，重点覆盖：

- 问卷设计与发布
- 访谈提纲设计
- 访谈纪要与洞察整理
- 调研回收材料分析

### 文档处理

对应 PDF、Word、Excel、PPT 等材料的读取、编辑、转换和抽取，重点覆盖：

- PDF 处理与 OCR
- Word 文稿处理
- Excel 表格处理
- PPT 材料处理
- 多类型文档转 Markdown

### 知识整理

对应跨资料的中间整理层，重点覆盖：

- 多文档总结
- 结构化摘要
- 资料清洗
- 中间知识沉淀

### 分析建模

对应从信息走向洞察的研究阶段，重点覆盖：

- 市场分析
- 竞品分析
- 趋势分析
- SWOT 等分析框架
- 数据分析

### 报告输出

对应最终成果交付阶段，重点覆盖：

- Word 报告成稿
- PPT 汇报材料
- 结论提炼
- 政策建议或咨询式表达

### 可视化

对应研究框架图、流程图、架构图和信息图表达，重点覆盖：

- draw.io 图表
- Mermaid 图表
- Excalidraw 草图
- 信息图

## Bundle 定义

### `thinktank-core`

智库研究核心包。覆盖信息获取、文档处理、分析和基础交付，是默认主力技能包。

### `academic-research-plus`

学术研究增强包。用于补强 arXiv、Google Scholar、论文精读和论文对比等学术研究场景。

### `monitoring-and-insight`

动态监测增强包。用于新闻跟踪、趋势观察，以及补充搜索与网页抓取等持续监测类任务。

### `analysis-modeling-plus`

分析建模增强包。用于市场分析、商业分析框架、SWOT 和数据分析等研究建模任务。

### `delivery-plus`

材料转换与展示增强包。用于处理非常规输入材料和展示化输出，比如扫描版 PDF 转 Word、文章转信息图。

## `skills.csv` 字段说明

- `bundle_id`：所属技能包；不保留在正式清单中的条目留空
- `slug`：Skill slug
- `title`：Skill 标题
- `keep`：是否保留在当前正式清单中，取值为 `yes` 或 `no`
- `restricted_keep`：是否可进入默认的 `restricted` 安装模式，取值为 `yes` 或 `no`
- `primary_stage`：主流程阶段
- `dependencies`：主要使用前提、外部依赖或平台绑定情况
- `downloads`：下载量
- `stars`：收藏或点赞量
- `installs_current`：当前安装量
- `checked_at`：最近检查日期
- `reason`：当前保留或不保留的简要原因
- `review_note`：质量检查摘要

## 质量检查逻辑

质量检查不只看 ClawdHub 排名和下载量，更看下面 4 个维度：

1. 包内容是否完整
   - 是否只有 `SKILL.md`
   - 是否带 `scripts/`、`README.md`、`references/`、`package.json` 等真实落地内容
2. 使用门槛是否可接受
   - 是否依赖 API Key、登录、桌面 CLI、浏览器网页或外部服务
   - 是否存在明确价格、免费次数限制、调用计费
   - 是否强绑定某个平台、某个机构系统或特定账号体系
   - 是否依赖中国以外网络或平台才能发挥核心能力
3. 名称与实际能力是否一致
   - 名称是否容易让人误判
   - 实际上是工具能力、方法模板，还是外部服务包装
4. 平台验证度是否足够
   - `downloads`、`stars`、`installs_current` 作为辅助判断
   - 只作为加减分项，不单独决定去留

## 维护规则

- 新增 skill 时，直接在 `skills.csv` 追加一行
- 复查 skill 时，更新同一行，不新增重复记录
- bundle 调整时，只改 `bundle_id`
- 质量结论调整时，只改 `keep`、`restricted_keep`、`reason`、`review_note`
- 如果某个 skill `keep=no`，原则上 `bundle_id` 也应清空，避免和正式技能包混淆
- `restricted` 模式的含义是：默认不安装需要 API Key 或依赖中国以外网络的 skill
- `dependencies` 继续保留给人阅读；脚本过滤只读取 `keep` 和 `restricted_keep`
