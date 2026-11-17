# 体育赛事数据可视化与观赛辅助 Skill

> 13 项球类运动全覆盖的**赛事信息整理与可视化**工具箱：把公开赛事信息结构化，生成一份带球场动画、球员聚焦卡、数据面板的结构化观赛报告。只做信息整理与可视化，**不做赛果判断、**。

---

## 一、它是什么

一个给球迷、解说、体育数据教学用的**观赛辅助**工具。你给它一场比赛（或一整天的赛程），它把能查到的公开信息——阵型站位、关键球员、主客场表现、近期状态、赛前情报、专家观点——整理成一份**看得懂、可讨论**的结构化报告，并用动画球场、球员聚焦卡、数据面板把信息"可视化"出来。

本工具**只提升你看懂比赛的信息质量**，不做赛果判断、不给出任何结论性方向。

---

## 二、核心能力

- 🏟️ **球场 / 阵型动画**：按球类自动切换场地示意图，渲染双方阵型站位（纯 SVG，无版权风险）。
- ⭐ **重点球员聚焦卡**：参数化半身插画 + 入场动画，按队伍配色与位置自动生成（零真人照片、零版权风险）。
- 🔍 **赛事信息要点面板**：把本场可讨论的信息结构化呈现，纯描述、无赛果倾向。
- 📰 **赛前情报分级**：官方 / 权威媒体 / 未证实传闻 三级标注，未证实信息明确提示"不可作为依据"。
- 🎙️ **专家观点（权威 / 非权威）**：分级呈现并标注来源可信度，对非权威/民间观点主动提示"警惕付费参照方案"。
- 🛡️ **自查自纠质量闸门**：生成报告时自动对每场做一致性自查（头像重复/破损/性别、信息完整性、新鲜度、去重），可纠正项自动归一化/剔除。
- 📅 **每日总览**：把"今天 / 这轮所有比赛"放进同一份 JSON，生成聚合总览（每张卡片标出本场看点，点击平滑跳转到该场详细单元）。
- 🎯 **重点赛事聚焦**：从全部赛事中筛出带明星球员的重点场次，单独生成精耕版报告。

---

## 三、合规红线（务必遵守）

- ⚠️ 不做赛果判断。
- ⚠️ 仅适用于**合法体育赛事**；理性观赛、量力而行、未成年人禁止。
- ⚠️ 未证实传闻仅作视野补充，**不可作为依据**。
- ⚠️ 任何"保证结果 / 无依据消息 / 收费观点"都属于诈骗话术，一律拒绝。
- 内置 `references/risk_compliance.md` 与 `audit.py` 红线扫描，上架前后均可一键复检合规性。

---

## 四、怎么用（命令）

所有命令均为纯标准库 CLI（`scripts/analytics.py`），不依赖网络与第三方库。

```bash
# 1) 生成检索清单：给定赛事信息，返回一份结构化的"该去哪采什么"清单
python scripts/analytics.py gather --match "曼城 vs 阿森纳" --league 英超 --city 曼彻斯特

# 2) 出一份单场分析报告（按 assets/report_template.md 填好 match.json）
python scripts/analytics.py report --input match.json --output report.html

# 3) 出"今日全部赛事"总览（matches 数组，每场即一份 match 数据）
python scripts/analytics.py daily --input day.json --output day.html

# 4) 出"重点赛事"聚焦版（自动筛 key=true 或含 key_players 的场次）
python scripts/analytics.py focus --input day.json --output focus.html

# 5) 刷新信息 + 时效戳（默认回写 JSON；--no-write 关闭）
python scripts/analytics.py refresh --input match.json

# 6) 一键自查（综合）：头像 + 信息完整性 + 新鲜度；--fix 自动回写修正
python scripts/audit.py <json>
python scripts/audit.py <json> --strict
```

调用本 Skill 的模型在生成报告后，须用 `present_files` 把 HTML 渲染到对话内置预览面板，并复制到桌面保底。

---

## 五、目录结构

```
sports-data-analysis/
├── SKILL.md                       # 技能入口与使用说明
├── README.md                      # 本文件
├── assets/
│   ├── report_template.md         # 单场 match.json 字段模板
│   ├── demo_match.json            # 单场演示数据（新 schema）
│   └── daily_sample.json          # 每日总览演示数据（新 schema）
├── references/
│   ├── analysis_methodology.md    # 信息整理方法（看结构/看变量/看不确定性）
│   ├── data_sources.md            # 数据源与分级采集规范
│   ├── risk_compliance.md         # 合规红线与反诈骗清单
│   ├── daily_update_workflow.md   # 每日信息更新流程
│   ├── faq.md                     # 常见问题
│   ├── marketing_copy.md          # 诚实营销文案
│   └── professional_analysis.md   # 报告专业指标说明（信息维度）
└── scripts/
    ├── analytics.py               # 核心渲染引擎（CLI）
    ├── gen_demo.py                # 生成 13 项运动演示数据（新 schema）
    └── audit.py                   # 自查体检系统（质量闸门）
```

---

## 六、发布口径

只讲真话、只做合法赛事的数据可视化与观赛辅助，**绝不承诺赛果、绝不指导任何结论性判断**。所有"亮点"必须来自「信息透明 / 战术可视化 / 看穿误导 / 理性观赛」，不涉及任何敏感表述。
