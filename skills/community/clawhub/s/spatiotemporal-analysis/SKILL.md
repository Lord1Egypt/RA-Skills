---
name: spatiotemporal-analysis
description: "时空智能分析法（v2.0 完整版）。纵向时间线 × 横向对照 × 交汇判断，必须先检索后下判断。含双交付模式（摘要→完整版）、当代实证研究不用学术库、引用覆盖率门槛、PDF 输出配方、松哥写作约定、5 子 agent 工程化流水线、数据采集脚本与模板等。触发：「时空智能分析」「时空分析」「spatiotemporal」「深度研究报告」「竞争格局分析」，或用户要求「研究一下 X 与 Y 的关系」这类带时间维度+对照维度的题目。"
version: 2.0.0
author: Hermes Agent (合并自 v1.0 local + v1.1.0 official)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Analysis, Literature, Confidence, Chinese, PDF, Methodology]
    category: research
    related_skills: [grounded-citations, arxiv, competitor-news-monitor, pdf, auto-grading]
    changelog:
      - "v2.0.3 (2026-09-08): Pitfalls 加 1 条'PDF 排版堆砌大杂烩风格'(2026-09-08 松哥反馈'排版仍不美观，变化太多，不够优雅' → 编码为字号≤4 / 颜色≤3 / 底色≤2 的硬上限自检清单)"
      - "v2.0.2 (2026-09-08): PDF 配方升级 v3（仿企鹏出版社风格：3 种字号 + 2 种颜色 + 1 处底色 + 大留白）；新增硬性约束#9 PDF 排版克制原则"
      - "v2.0.1 (2026-09-08): 新增硬性约束#8 输出术语规约（试用/test/sample/demo 等过程性术语禁用）；本次修复源于 2026-09-08 数字媒体艺术 AIGC 教育报告的章节标题错误（试用结论）"
      - "v2.0 (2026-09-08): 合并 v1.0 完整工程化骨架（5 子 agent 流水线 + fetcher + templates + 隐私清单）与 v1.1.0 实测经验（双交付模式 / 学术源判断 / 置信度校准 / PDF 配方 / 引用门槛 / 松哥写作约定）"
      - "v1.1.0 (2026-09-08): 官方版，新增双交付、学术源判断、置信度校准、Pitfalls、PDF 配方"
      - "v1.0 (2026-09-06): 本地版，5 子 agent 流水线、数据采集脚本、3 模板、隐私清单"
---

# 时空智能分析法 · Spatiotemporal Analysis · v2.0 完整版

> **本 skill 是"研究方法论 + 工程化骨架"**，定义了**怎么**做时空分析，并提供可直接调用的脚本与模板，但不替代具体业务判断。

## 触发方式

- 「时空智能分析 [研究对象]」/「时空分析 [研究对象]」
- 「spatiotemporal [研究对象]」
- 「深度研究 [研究对象]」/「竞争格局分析 [研究对象]」
- 「研究 [研究对象]」+「用时空智能分析法」

**不适用**：一句话事实查询（直接 web_search）、纯偏好之争、实时新闻监控（走 competitor-news-monitor）、代码审计（走 code-doctor）。

---

## 🚨 硬性约束（绝不妥协）

1. **数据必须可溯源**——每个事实必须有 source_url + 时间戳（来自 web_search / grounded-citations）
2. **先检索，再下判断**——检索发生在写分析之前，不是之后（2026-09 AGI 报告实证教训）
3. **判断场景必须先于研究**——避免无脑对比表（详见第五章「场景判断」）
4. **推测必须标注 confidence**（高/中/低）+ 标注是「事实」还是「推测」
5. **禁止编造**——信息空白处显示「数据不足，需补充」，绝不假装知道
6. **轻量化原则**——摘要版 3,000-6,000 字；完整版 30,000-50,000 字（OPC 报告实证：14 页 / 290KB / 88% 覆盖率）
7. **隐私隔离**——上传 clawhub 时严格排除用户私密文档（详见第九章）
8. **输出术语规约**——正式交付报告**禁止**出现「试用 / test / sample / demo / v0.x / pilot / PoC」等过程性术语；使用「完整版 / 正式版 / 最终交付 / 已落档」。**章节标题、收尾落款、文档元数据全部按正式交付标准**（2026-09 数字媒体艺术报告实证教训：报告内出现「试用结论」会让读者怀疑报告完成度）
9. **PDF 排版克制原则**——PDF 输出遵循 v3 配方（仿企鹏出版社风格）：3 种字号（14/12/11pt）+ 2 种颜色（主蓝 #1548A0 + 中灰 #44545F）+ 1 处底色（引用框 4% 浅蓝底）+ 大留白（段间 12pt）+ 优雅字体（PingFang SC + Menlo）。**禁止**字号超 4 种、颜色超 3 色、emoji 多色填充（2026-09-08 松哥反馈："排版仍不美观，变化太多，不够优雅"）

---

## 一、方法论哲学根基（brief）

时空智能分析法的独特性来自**两个哲学传统**的合流：

| 维度 | 哲学根基 | 方法论对应 |
|------|---------|----------|
| **纵向（时）** | 胡塞尔现象学：意识是"滞留 + 前摄"的连续流 | 时间轴叙事，要求每个判断带时间锚点 |
| **横向（空）** | 卢曼社会系统理论：元素意义由"它与其他元素的关系"决定 | 共时性对比，要求放在生态位中评估 |

**反 4 大谬误**：
- 反"快照谬误"——不只看现在，要看过去-现在-未来
- 反"孤立谬误"——不只看单点，要看生态位
- 反"罗列谬误"——不做流水账，要讲故事弧线
- 反"二元谬误"——不评"好坏"，评"位置对不对"

---

## 二、交付模式：先摘要，看需求再展开完整版（松哥偏好）

实测有效（2026-09 OPC 中美对比报告）的两轮交付模式：

1. **第一轮：交付"摘要版"（10–20KB / 5–8 章）**——核心结论 + 5 维横向对比 + 趋势研判，足以让读者判断"这个题目值不值得继续"。
2. **如果用户说"完整分析报告" / "不用摘要" / "全部展开"**——**重做完整版（30–50KB / 8–11 章）**，而不是给摘要加附录。摘要版和完整版是两份独立报告，不是增量关系。

**为什么不是增量而是重做**：

- 摘要版的章节结构、表格密度、引用粒度都是为"快速判断"优化的；硬塞内容会变成又长又散的拼贴。
- 完整版需要独立的章节规划（如 OPC 报告完整版新增"法律实体对比"、"实证案例库"、"中国政策图谱"三章）。
- 完整版的引用密度更高（≥85% 覆盖率），需要重新走一遍 grounded-citations 流程。

**反模式**：❌ 把摘要版"展开成"完整版（保留摘要的章节顺序、表格，只往里塞内容）。结果是一份既不像摘要又不像完整版的报告。

---

## 三、源类型判断：什么时候不用学术库

`academic-workflow`（OpenAlex / S2 / arXiv / PubMed）的学术源**不是所有研究题目的有效信源**。判断标准：

| 题目类型 | 推荐源 | 学术源适用？ |
|---|---|---|
| 当代政策 / 经济实证 / 法律合规 / 商业案例 | 政府文件、咨询报告、官方媒体、IRS / 国家统计局等 | ❌ 不适用 |
| 前沿学术问题 / 模型架构 / 算法对比 | arXiv、S2、OpenAlex | ✅ 高度适用 |
| 跨学科理论（如"AI × 经济学"） | 两者结合 | ⚠️ 部分适用 |

**为什么学术源对当代实证研究常常污染**：在学术语境下，"OPC / 一人公司"可能被映射到其他概念（如 Optical Proximity Correction / Optimal Phased Catalog），污染检索结果。当代实证研究的主流文献在政策文件、咨询报告、官媒，不在期刊。

**操作规则**：如果是 OPC 这类**当代政策 + 经济实证**题目，跳过学术库，直接走政府文件（IRS / 国家统计局 / 国务院 / 深圳市政府）+ 头部咨询（Carta / Menlo / McKinsey）+ 权威媒体（人民网 / 央视 / BBC 中文 / 36氪）。

**学术源实测缺陷**（见 `references/output-conventions-and-source-quirks.md`）：
- arXiv 连续调用会 429（sleep ≥ 5秒）
- arXiv citation_count 恒为 None，跨源按引用数排序会把预印本静默排到末尾
- Crossref 批量 DOI 补全遇一个非法 DOI 整批 400

---

## 四、5 子 agent 流水线（工程化骨架）

```
[触发 / 入口]
    │
    ▼
① spatiotemporal-scenario-judge      # 场景判断：A 无竞品 / B 少量 / C 充分
    │
    ▼
② spatiotemporal-longitudinal        # 纵向：时间轴 + 关键节点 + 决策逻辑（时空之"时"）
    │
    ▼
③ spatiotemporal-cross-sectional     # 横向：竞品 / 替代方案 + 生态位（时空之"空"）
    │
    ▼
④ spatiotemporal-convergence         # 交汇：纵向惯性 × 横向位置 → 概率分布
    │
    ▼
⑤ spatiotemporal-renderer            # 输出：Markdown → PDF → 落档
```

每个 agent 标识清晰（如 `我是 spatiotemporal-longitudinal...`），输入范围严格。

**5 个子 agent 不是项目代号**，是**方法论组件**——可用于研究 OPC、Cursor、AGI × 设计思维或任何其他对象。

---

## 五、场景判断：3 种竞品场景

| 场景 | 判断标准 | 横向处理 |
|------|---------|---------|
| **A 无竞品** | 输入研究对象后搜索"X 竞品/alternatives"，无显著结果 | 跳过逐一对比；改为分析"为什么没竞品"+"潜在竞争者从哪冒"+"间接替代方案" |
| **B 少量竞品（1-2）** | 搜索结果 ≤ 2 个显著竞品 | 逐一深入对比，每个竞品至少 1500 字 |
| **C 充分竞品（≥3）** | 搜索结果 ≥ 3 个显著竞品 | 选 3-5 个最具代表性对比，其余简要提及 |

**自动检测脚本**：`scripts/spatiotemporal_fetcher.py --mode scenario`

---

## 六、纵向分析规范（时空之"时"）

每个时间节点必须包含：

```
- date: YYYY-MM-DD（必须）
- event_type: funding/release/team/pricing/partnership/incident
- title: 一句话标题
- description: 详细描述
- source_url: 一手来源
- source_type: official/sec/news/blog/social/forum
- confidence: confirmed/reported/speculated
```

**叙事弧线要求**：
- 不写成"YYYY 年 X，YYYY 年 Y"的流水账
- 要有"起承转合"：铺垫 → 转折 → 爆发 → 沉淀
- 每个关键节点要回答"为什么选 A 不选 B"

**检索设计**（来自 `references/output-conventions-and-source-quirks.md`）：
- 拆成 4+ 条窄查询，4 条 × 12-15 条结果 ≈ 57 篇命中，其中约 15 篇承重
- 覆盖源 + 前沿源配对（OpenAlex/S2 + arXiv）
- **检索「失败模式」词**（fixation / deskilling / premature convergence / homogenization）——只搜主题词回来的是一片叫好，搜怀疑中的代价才能捞到让分析不平庸的对照实验
- 覆盖源加日期过滤（如 2024-01-01 起），否则一篇高引的 2019 综述会把当期发现挤掉

---

## 七、横向分析规范（时空之"空"）

**对比维度**（根据研究对象类型灵活调整）：
1. 核心差异（技术路线 / 商业模式 / 目标用户 / 优劣势 / 定价）
2. 用户视角（真实口碑 / 社区评价 / 使用体验偏差）
3. 生态位分析（在赛道中的位置 / 填补了什么空白）
4. 趋势判断（机会 + 风险）

**禁止**：参数对照表的文字版。要讲每个竞品"活成了什么样"，用户选它的真实理由。

**横向表所有行共用同一条比较轴**——否则那是清单，不是对比。

**对象是研究主题（而非具体产品）时**，横向轴往往**不是竞品**，而是竞争性机制——"谁承担认知负荷"、"代价由谁支付"。四种机制的对比表 >> 四家厂商的对比表。

---

## 八、交汇分析规范（最关键）

交汇段不是"前面内容的缩写版"，要给出**新的综合性判断**：

**结构**：
1. **纵向惯性**：过去 5-10 年的演化路径揭示的"惯性"（如：技术债务、组织惯性、用户习惯）
2. **横向位置**：当前在生态位中的相对位置
3. **未来概率分布**：列出 3-5 个可能场景 + 各自概率 + 关键证据
4. **关键转折点**：哪些信号出现，概率分布会变化

**probability 标注规则**（实测好用的校准标准）：
- **高** — 对照实验 / 大样本盲评 / 多来源可复现
- **中** — 访谈、单案例、小样本原型研究、专家问卷
- **低** — 由邻近发现外推；必须写明"什么数据能定案"
- 概率 ≥ 70% = high confidence
- 30%-70% = medium confidence
- < 30% = low confidence
- **必须**有 2 个以上独立证据来源

**结尾必须补一节「本次检索推翻的流行说法」**——往往是整份报告最值钱的部分，而且是纯凭记忆的分析在结构上产不出来的。

---

## 九、隐私隔离（上 clawhub 前必查 7 项）

**绝不上传**：
- 用户 ~/Documents/*、~/Downloads/*
- 用户 ~/Desktop/* 中的课程 / 论文 / 毕设 / UXPA* / OPENCLAW* / viflow* / AISDDS*
- ~/.hermes/sessions/* 对话历史
- ~/.openclaw/* 用户项目
- 任何 *.docx/*.pdf 包含用户原创内容
- 任何 API key / token / 邮箱 / 电话

**可以上传**：
- 学术论文检索脚本（已开源 MIT 协议）
- 时空智能分析法 SKILL.md + references/ + scripts/ + templates/
- 通用方法论和模板

---

## 十、核心参考资料（按需加载）

| 文件 | 触发场景 |
|------|---------|
| **references/methodology.md** | 任何场景——哲学根基 + 5 段叙事弧线模板 |
| **references/data_sources.md** | 数据采集——4 大源（academic-workflow + DuckDuckGo + GitHub + 本地缓存）+ 9.1-9.6 中文源 / 院校官方源 / CNKI / RISD-Parsons 附录（2026-09-08 实证教训） |
| **references/writing_baseline.md** | 写作风格——4 种叙事节奏 + 严禁事项 |
| **references/output-conventions-and-source-quirks.md** | 松哥写作约定 + 学术源实测缺陷 + 检索词模板 |
| **references/markdown-to-pdf-zh.md** | 中文 PDF 输出配方（pandoc + xelatex + PingFang SC） |
| **templates/convergence_table.md** | 交汇分析的概率分布表模板 |
| **templates/report_short.json** | 短报告（3000 字）模板 |
| **templates/report_medium.json** | 中等报告（5000 字）模板 |
| **scripts/spatiotemporal_fetcher.py** | 数据采集主入口 |
| **scripts/spatiotemporal_auditor.py** | 报告一致性审计器 |

---

## 十一、与其他 skill 的协作

| skill | 何时调用 | 调用方式 |
|------|---------|---------|
| **grounded-citations** | 引用溯源（必备） | 每个事实必须能溯源；用 `add`/`render`/`verify` 流程 |
| **academic-workflow** | 学术文献检索 | `academic-workflow/scripts/research.py` 模块 |
| **arxiv** | arXiv 单源检索 | `skill_view(name='arxiv')` + 调用 |
| **competitor-news-monitor** | 实时新闻监控 | 第②子 agent 调用 |
| **pdf** | 像素级控制 PDF | 用 `pdf_create.py` + reportlab JSON spec |
| **auto-grading** | 论文/毕设审查 | 学术评审时复用 |

---

## 十二、引用覆盖率门槛（grounded-citations 硬约束）

研究报告必须跑完 grounded-citations 的完整四步（reset → add → render → verify），且满足：

| 交付物 | 引用覆盖率门槛 | 解释 |
|---|---|---|
| **完整版报告** | ≥ 85% | 通过 `verify --min-coverage 0.85`；低于此值视为未达标，必须补源或加 `[unverified]` 标记 |
| **摘要版** | ≥ 75% | 摘要可以接受更多 `[unverified]` 总结句，因为重点是快速判断不是溯源 |
| **法规 / 政策类报告** | ≥ 90% | 这类报告判断句少、事实句多，覆盖率应自然偏高；达不到说明检索不到位 |

**实操流程**：

```bash
S=~/.hermes/skills/research/grounded-citations/scripts/sources.py
python "$S" reset                                # 起新 ledger
python "$S" add <url1> --title "..."             # 每个一手源必加
python "$S" add <url2> --title "..."
# ... 写正文，每个事实句挂 [n]，总结句挂 [unverified]
python "$S" render --replace-in report.md        # 把 ledger id→URL 写到 Sources 块
python "$S" verify report.md --min-coverage 0.85 # 不通过就补
```

**反模式**：
- ❌ 直接在 Markdown 里手写 `[1] http://...` 而不跑 ledger → URL 与 id 会跑偏，verify 不通过
- ❌ 不补源就硬把 75% 的报告标"高引用覆盖率" → 等于隐瞒溯源漏洞

---

## 十三、PDF 输出（macOS 实测）

完整版 / 摘要版交付时如果用户要 PDF，不要用 markdown 转 HTML 截图或 weasyprint（中文易出坑）。**pandoc + xelatex + PingFang SC 是实测最稳的中文配方**（2026-09 OPC 报告输出 14 页 / 290KB）。

完整一行命令 + 已知瑕疵 → `references/markdown-to-pdf-zh.md`。

---

## 十四、Pitfalls

- **先凭记忆写时间线，再去「核对」** —— 这是确认偏误的形状：来源只要大致沾边，错的行就被留下了。顺序必须是先检索。
- **横向表每行的比较维度不一致** —— 那是清单，不是对比，支撑不了任何判断。
- **交汇段的判断不标置信度** —— 没有日期、没有标签的推测，半年后整份报告就废了。
- **跳过「推翻了什么」那一节**，理由是"查到的都同意我" —— 若真什么都没推翻，这件事本身值得写一句，并且值得回头检查是不是所有查询都被措辞成了同意自己。
- **把上一次同题分析的结论当既定事实复用** —— 复用前重跑检索。
- **只报喜不报缺陷** —— 检索过程中的报错、限流、字段缺失要写进报告的"实测缺陷"一节，那是下一次改良工具的输入。
- **学术库硬塞当代政策/经济类题目** —— OPC 这类题目在 OpenAlex/arXiv 里没有有效信源，跳过学术库直接走政府文件+头部咨询+权威媒体。
- **删/合 skill 之前不做覆盖度审计** —— 见第十七章。松哥原话："如果内容变少了，那也是有问题的"。**禁止**"新版看着更精简"就直接合并，**必须**先证明 v2.0 完全覆盖 v1.0 的所有内容（不仅是 SKILL.md，还有 references / scripts / templates）。
- **猜 skill 名字 / 触发词 / 路径而不上 ls 检查目录**（2026-09-08 教训）—— 用户说"改名了"或"触发词是什么"时，第一反应应该是 `ls ~/.hermes/skills/<category>/` + `grep "name:" <skill>/SKILL.md`，**而不是凭印象猜**。猜错 → 用户打断 → 反复试错 → 浪费 5+ 轮对话。**正确流程**：先查实际状态（`ls` + `skill_view`），再回应。**技能名 / 触发词 / 描述都从 SKILL.md frontmatter 直接读，不要靠"印象"。**
- **凭印象说"新开发"或"新建"**（2026-09-08 教训）—— 用户说"改名了"或"触发词是什么"，可能是：(a) 真的新开发；(b) 旧 skill 已存在但目录名/触发词曾被改动；(c) 是用户的命名习惯与你记的不一致。**正确流程**：先 `ls` 检查整个分类目录 → 找到实际的 SKILL.md → 直接读 frontmatter。如果 skill 已存在且完整，**不要从零开发**。
- **PDF 排版堆砌"大杂烩"风格**（2026-09-08 教训）—— 用户原话："排版仍不美观，变化太多，不够优雅"。PDF 一旦字号超过 4 种、颜色超过 3 色、底色超过 2 处，读者会感到"信息超载"。**3 种字号 + 2 种颜色 + 1 处底色**是优雅的硬上限（参见 `references/markdown-to-pdf-zh.md` v3 配方）。**自检清单**：① 字号 ≤ 4 ② 颜色 ≤ 3 ③ 底色 ≤ 2 ④ emoji 不用多色填充 ⑤ 留白段间 ≥ 12pt。任何一项超标 → 强制精简。

---

## 十五、Verification Checklist

- [ ] 纵向表每行有年份 + 来源
- [ ] 横向表所有行共用同一条比较轴
- [ ] 交汇段每条判断都有置信度标签，事实与推测分列
- [ ] 有「本次推翻的流行说法」一节（或明确说明无）
- [ ] 有「可复现检索命令」一节
- [ ] 有「实测缺陷 / 工具报错」一节
- [ ] `verify --min-coverage 0.85` 通过（完整版）/ `0.75` 通过（摘要版）/ `0.90` 通过（法规政策类）
- [ ] 所有内联引用 [n] 都在 ledger 里且 Sources 块由 render 命令写入
- [ ] 双交付模式：第一轮给摘要，第二轮重做完整版（除非用户明确拒绝）
- [ ] 上传 clawhub 前已剔除 7 项隐私清单内容
- [ ] **skill 合并/清理**：做过覆盖度审计（17 章），删除前已备份到 `~/.hermes/.<name>-merge-backup-YYYYMMDD/`

---

## 十六、3 个已验证场景

| # | 研究对象 | 场景 | 关键经验 |
|---|---------|------|---------|
| 1 | AGI × 设计思维 | A（无直接竞品） | 4 个思维结构变化是核心产出；第一遍凭模型知识的判断被 N=60 对照实验推翻 |
| 2 | OPC 一人公司 | C（充分竞品） | 当代实证研究跳过学术库，走 IRS + 国家统计局 + 国务院 + 头部咨询；43 信源 / 88% 覆盖率 / 14 页 PDF |
| 3 | 国内数字媒体艺术 × AIGC 教育（2026-09-08 实证） | A（无直接竞品 · 跨学科研究领域） | 4 大院校路径对比；中文 arxiv 命中率 < 30%，必须加院校官网 + 中文媒体源；skill 评分 93/100 |

**v2.0.1 验证结论**：
- AGI × 设计思维 + 数字媒体艺术教育 = 两个场景 A 的实证，证明 v2.0 对"无直接竞品·跨学科"类研究稳定
- 下一次验证场景 C（充分竞品，例如"Cursor vs Copilot vs Windsurf"）可以补足实证类型覆盖

---

## 十七、Skill Lifecycle：合并/清理前的覆盖度审计（**强约束**）

这一章**不是研究方法论**，而是本 skill 在 2026-09 v2.0 合并过程中用血的教训换来的 **skill 生命周期规则**。适用于**任何** skill 的合并 / 重写 / 删除，不限于本 skill。

### 铁律

松哥原话："纵横或者横纵分析法都是老的版本，有了时空智能以后，保持时空智能那个最新的、最完整的版本。**老的、过渡的，你按照时间顺序看一下，就都删掉。** 别到时候这些都差不多的东西，触发词互相干扰，然后也占空间。"

松哥原话（确认版）："**不对吧。你要检查一下这个时空智能这个最新版本是不是基本上完全涵盖了之前横纵的最新版本。涵盖了嘛就是对的，如果内容变少了，那也是有问题的。**"

→ 翻译为可执行规则：**禁止**"新版看着更精简"就直接删旧版。**必须**先证明新版完全覆盖旧版的所有内容。

### 触发条件

满足以下任意一条时，**必须**先做覆盖度审计，再做删除 / 合并：

1. 同一个方法论 / 同一个工作流出现 ≥ 2 个 skill（重复风险）
2. 准备把一个 skill 改名 / 移动目录 / 重写 SKILL.md
3. 用户说"清理一下"、"合并"、"删掉老的"、"保持最新"
4. 新版与旧版名字不同但内容描述相似

### 覆盖度审计流程（5 步，强制）

```bash
# Step 1: 文件级对比 —— 不要只看 SKILL.md，要把整个目录摊开
find <旧版目录> -type f -exec wc -l {} \; > /tmp/old_files.txt
find <新版目录> -type f -exec wc -l {} \; > /tmp/new_files.txt
diff /tmp/old_files.txt /tmp/new_files.txt

# Step 2: 内容级对比 —— 把旧版每一项独有内容列出来，逐一确认新版是否覆盖
# 用 execute_code 或 read_file 读出旧版 SKILL.md + 所有 references
# 用同样的方法读新版
# 输出对比表：旧版独有 / 新版独有 / 两者都有

# Step 3: 触发词去重 —— 两个 skill 触发词重复会导致路由冲突
grep -E "^description:" <旧版 SKILL.md> | head -1
grep -E "^description:" <新版 SKILL.md> | head -1
# 重复度 ≥ 80% 的两个 skill 必须合并

# Step 4: 工程化骨架不能丢 —— scripts/ + templates/ + 隐私清单这些"非方法论"内容
# 容易被精简主义误删，必须逐一确认
ls <旧版>/scripts/ <旧版>/templates/ 2>/dev/null
ls <新版>/scripts/ <新版>/templates/ 2>/dev/null
# 旧版有而新版缺的每个文件，必须在新版里有等价物

# Step 5: 删除前必须先备份（保护性，不是依赖）
mkdir -p ~/.hermes/.<skill-name>-merge-backup-YYYYMMDD/
cp -r <旧版> ~/.hermes/.<skill-name>-merge-backup-YYYYMMDD/v<旧版号>
cp -r <第二旧版> ~/.hermes/.<skill-name>-merge-backup-YYYYMMDD/v<第二旧版号>
```

### 决策表

| 覆盖度审计结果 | 决策 |
|---|---|
| 新版**完全覆盖**旧版（含工程化骨架）| ✅ 可以删除旧版 |
| 新版**部分覆盖**（新版有删减）| ❌ **不能删**，把旧版独有内容补进新版后再删 |
| 新版**精简但等价**（同样的规则换种说法）| ✅ 可以删，但要在 SKILL.md 修订日志里写"等价重写" |
| 触发词**冲突 ≥ 80%**| ⚠️ 必须合并（重复触发会让 router 随机派发）|
| 旧版有 scripts/templates，新版没有 | ❌ **不能删**，scripts/templates 是工程化骨架不是方法论 |

### 2026-09 OPC / spatiotemporal-analysis 实测

合并 v1.0（openclaw-imports/spatiotemporal-analysis） + v1.1.0（research/vertical-horizontal-analysis） → v2.0（research/spatiotemporal-analysis）的过程里：

- 第一次准备直接删 v1.0 → 用户拦下："不对吧"
- 做了覆盖度审计 → 发现 v1.0 独有 20 项（5 子 agent 流水线 / fetcher.py / auditor.py / 3 个模板 / 7 项隐私清单 等），v1.1.0 独有 13 项（双交付模式 / PDF 配方 / 引用门槛 等）
- 合并后 v2.0 = 1560 行，**两项独有内容全部保留**
- 删除前先备份到 `~/.hermes/.spatiotemporal-merge-backup-20260908/`（30 天后清理）

### 反模式（绝对不要做）

- ❌ "新版更精简 = 旧版过时了" → 删 → 用户发现丢了工程化骨架 → "如果内容变少了，那也是有问题的"
- ❌ 只比 SKILL.md 行数，不比 references/scripts/templates 清单
- ❌ 触发词相似就合并、不做内容比对
- ❌ 不备份就删（user-owned skill 的删除是不可逆操作）

---

## 修订日志

### v2.0.1 (2026-09-08 · 增量补丁)
- 🆕 **Pitfalls 增 2 条**（基于本次会话命名反复纠正教训）：
  - "猜 skill 名字/触发词/路径而不上 ls 检查目录"——先 `ls ~/.hermes/skills/<category>/` 再回应
  - "凭印象说'新开发'或'新建'"——用户说"改名了"可能是 (a) 真的新开发 / (b) 旧 skill 已存在但目录名/触发词曾被改动 / (c) 命名习惯不一致。先查实际状态再判断
- 🆕 **本会话实证**：研究对象"国内数字媒体艺术 × AIGC 教育" → 场景 A（无直接竞品·跨学科研究领域）→ 4 大院校路径对比 → skill v2.0 评分 93/100

### v2.0 (2026-09-08)
- 🔀 **合并**：v1.0 完整工程化骨架（5 子 agent 流水线 + fetcher + templates + 隐私清单 + 协作表）+ v1.1.0 实测经验（双交付模式 / 学术源判断 / 置信度校准 / PDF 配方 / 引用门槛 / 松哥写作约定 / Pitfalls / Verification）
- 📁 **位置变更**：从 `openclaw-imports/spatiotemporal-analysis/` + `research/vertical-horizontal-analysis/` 合并到 `research/spatiotemporal-analysis/`
- 🗑️ **删除**：旧的 spatiotemporal-analysis 与 vertical-horizontal-analysis 两个目录（v2.0 是它们的唯一后续版本）
- 📊 **内容规模**：SKILL.md ~250 行 + 5 个 references (~1100 行) + 2 个 scripts (~460 行) + 3 个 templates (~160 行) ≈ 1970 行
- 🆕 **新增 Skill Lifecycle 章节（17）**：松哥原话"如果内容变少了，那也是有问题的"→ 编码为 skill 合并/清理前的覆盖度审计强约束（2026-09-08 当日补加）

### v1.1.0 (2026-09-08)
- ✨ 双交付模式（OPC 报告实证）
- ✨ 学术源适用判断表
- ✨ 先检索再下判断铁律
- ✨ 置信度实操校准
- ✨ 引用覆盖率门槛（≥85/75/90%）
- ✨ Pitfalls + Verification
- ✨ PDF 输出配方

### v1.0 (2026-09-06)
- ✨ 5 子 agent 流水线（scenario → longitudinal → cross-sectional → convergence → renderer）
- ✨ 数据采集脚本（fetcher.py 294 行 + auditor.py 165 行）
- ✨ 3 模板（convergence_table / report_short / report_medium）
- ✨ 4 大数据源（academic-workflow + DuckDuckGo + GitHub + 本地缓存）
- ✨ 7 项隐私清单
- ✨ 与其他 skill 的协作表