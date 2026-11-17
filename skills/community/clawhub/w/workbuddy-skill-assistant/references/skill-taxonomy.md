# Skill 基础分类标准（taxonomy）

> **采纳来源**：阿里 SkillsHub（[skills.alibaba.org.cn](https://skills.alibaba.org.cn/)）的七大领域划分。
> **采纳日期**：2026-09-16，经教授确认。
> **原则**：**基础七类固定不变**（代码、名称、语义都不改），需要新领域时**积木式追加扩展类**，不动七类。

## 一、基础七类（固定）

| 代码 | 中文名 | 英文 | 覆盖范围 | 典型积木举例 |
|------|--------|------|----------|--------------|
| `coding` | 编程开发 | Coding & Dev | 写代码、调试、重构、代码评审、部署、技术栈最佳实践 | code-review-and-quality、diagnosing-bugs |
| `agent` | 智能体 | Agent | Agent 能力扩展、技能发现、子代理编排、提示工程 | find-skills、skill-designer、agent-browser |
| `writing` | 写作创作 | Writing | 文章、报告、文案、公文、内容策略、润色 | deep-report-forge、any2html、gzh-design |
| `analysis` | 数据分析 | Data Analysis | 数据处理、统计分析、可视化、报表、金融数据分析 | xlsx、data-visualization、stock-volume-12step-analysis |
| `design` | 设计创意 | Design | UI/视觉设计、海报、配色、排版、图像处理 | canvas-design、ardot-design-assistant、impeccable |
| `productivity` | 效率工具 | Productivity | 办公自动化、文档批处理、日程任务、流程提效 | Work_ppt_master、Work_document_pipeline、wecom-unified |
| `education` | 教育学习 | Education | 教学、辅导、知识内化、学习评测 | card-generator、brick-workshop |

> 七类的代码沿用来源站的路径 slug（`/categories/<code>/`），便于与外部来源做检索映射。

## 二、扩展类（积木式追加）

基础七类覆盖通用领域，但专业场景（尤其投资研究）需要追加。扩展类**按需增加，不预设上限**，但每次追加须经教授确认并登记在此表。

| 代码 | 中文名 | 追加理由 | 典型积木举例 |
|------|--------|----------|--------------|
| `finance` | 金融投资 | 七类未覆盖投研/持仓/交易决策，而这是教授的主业场景 | Ob-portfolio-V5-strategy、westockdata、Work_build_dashboard |
| `knowledge` | 知识管理 | 七类未覆盖个人知识库/图谱/笔记沉淀 | ontology、obsidian、Work_work_diary、Work_investment_archiver |
| `meta` | 元技能 | 七类未覆盖「管理 skill 本身的 skill」（设计/体检/发布/路由） | skill-designer、skill-check-pro、skill-publish-audit、Work_skill_router |
| `workbuddy` | WorkBuddy 平台 | 七类未覆盖 WorkBuddy 生态自身（助手/工坊/注册表/工作流） | workbuddy-assistant、jimu-assistant、Work_skill_suite |

## 三、判定规则

1. **一 skill 一主分类**：按「最主要的产出物」定，不按使用工具定。示例：用 Python 画投资图表 → 归 `finance`（产出是投研结论），不归 `analysis`。
2. **无法归类 → `productivity`**：效率工具是兜底类（与来源站一致）。
3. **`agent` 与 `meta` 的分界**：面向**任意**任务的 Agent 能力（技能发现、浏览器自动化）归 `agent`；只面向 **skill 自身治理**的归 `meta`。
4. **`analysis` 与 `finance` 的分界**：通用数据方法（表格、统计、可视化）归 `analysis`；投研/持仓/交易语义归 `finance`。
5. **扩展类不吞基础类**：`finance` 出现后，通用金融**数据工具**（如 xlsx）仍归 `analysis`——分类看语义，不看数据源。

## 四、使用方式

1. **注册表标注**：`skill-registry.md` 每条积木标注 `分类`（七类代码或扩展类代码）；
2. **推荐对齐**：向教授推荐 skill 时，先把任务域映射到分类，再在同分类内挑候选，避免跨类乱推；
3. **外部检索映射**：检索阿里 SkillsHub 时直接用七类代码作为 `category` 过滤；检索本机积木时用同一套代码，两侧口径一致；
4. **工作流卡片**：卡片步骤表里的每块积木，建议标注分类，便于一眼看出接力是否跨域过大。

## 五、与外部来源的映射

| 本 skill 分类 | 阿里 SkillsHub | 说明 |
|---------------|----------------|------|
| `coding` | `/categories/coding/` | 名称与语义一致 |
| `agent` | `/categories/agent/` | 一致 |
| `writing` | `/categories/writing/` | 一致 |
| `analysis` | `/categories/analysis/` | 一致 |
| `design` | `/categories/design/` | 一致 |
| `productivity` | `/categories/productivity/` | 一致 |
| `education` | `/categories/education/` | 一致 |
| 扩展四类 | — | 来源站无对应分类，为本 skill 自建；从来源站检索时映射到最接近的基础类（如 `finance` → `analysis` + 关键词"股票/金融"） |

> 检索与安装的具体操作见 [skill-sources.md](skill-sources.md)。
