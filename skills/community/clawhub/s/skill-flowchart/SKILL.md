---
name: skill-flowchart
slug: skill-flowchart
displayName: SkillFlowChart
version: 1.0.0
description: "生成技能流程图、决策树、工作流图。读取 SKILL.md 或技能定义文件，提取决策节点与执行步骤，输出自包含 HTML 流程图（SVG，零依赖）。适用于可视化 Skill 执行流程、画决策树、生成 agent skill 的 decision flow diagram、流程可视化。Reads a SKILL.md and generates a decision flowchart HTML."
license: MIT
---

# Skill 决策流程图生成器

读取一份 `SKILL.md`，提取结构化数据 `nodes.json`，脚本确定性生成流程图 HTML。

## 分工

| 阶段 | 谁干 | 为什么 |
|------|------|--------|
| SKILL.md → nodes.json | **AI** | SKILL.md 是自然语言，语义不稳定，靠 AI 理解上下文 |
| nodes.json → HTML | **脚本** | 坐标计算要确定性、可复现、对齐像素 |

AI 只输出结构化数据，**绝不**输出坐标或 SVG；脚本只做几何，**绝不**猜语义。

## 执行步骤

### 1. 读取 SKILL.md

读取用户指定的 `SKILL.md`。若未找到，询问用户输入路径。

### 2. AI 提取 nodes.json

按以下 schema 输出 JSON。每条出边**必须**显式标注 `side` 字段——这是 AI 的语义判断，脚本不会猜。

#### 顶层结构

```json
{
  "title": "技能名称",
  "subtitle": "可选描述",
  "nodes": [ ... ],
  "edges": [ ... ],
  "loops": [ ... ],
  "legend": [ ... ]
}
```

- `nodes`：必填，节点数组
- `edges`：必填，有向边数组
- `loops`：可选，回环虚线（见下文）
- `legend`：通常留空 `[]`，使用默认图例

#### 节点 type

| type | 含义 | 形状 |
|------|------|------|
| `entry` | 流程起点 | 圆角矩形 |
| `decision` | 决策点（是/否、有/无） | 菱形 |
| `process` | 处理步骤 | 圆角矩形 |
| `output` | 报告/文件输出 | 圆角矩形 |
| `terminal` | 终止/报错退出 | 圆角矩形 |

#### 节点 role（配色）

| role | 含义 | fill / stroke |
|------|------|---------------|
| `ai` | AI 推理 / LLM 调用 | #E6F1FB / #185FA5 |
| `output` | 报告 / 文件输出 | #EEEDFE / #534AB7 |
| `decision` | 决策点 | #FAEEDA / #854F0B |
| `script` | 脚本执行 | #E1F5EE / #0F6E56 |
| `terminal` | 终止 / 报错 | #FCEBEB / #A32D2D |

> **一个节点只能有一个 role。** 如果一个步骤涉及多种不同性质的工作（对应不同 role），必须拆成多个节点串联。例如「脚本取基线 + AI 补充分析」不能合并为一个 role=ai 的节点，必须拆成 role=script 和 role=ai 两个节点。

#### 边 side（关键！）

| side | 含义 | 布局行为 |
|------|------|----------|
| `bottom` | 主流程向下 | target 在 from 下一层，cx 继承 from |
| `left` | 决策左分支 / 分叉左 | 决策→同层水平连；普通→下一层正交折线 |
| `right` | 决策右分支 / 分叉右 | 同上，方向相反 |

**side 的语义判断由 AI 完成**：
- 决策菱形（type=decision）的 `left`/`right` → 与决策**同层**，水平连线
- 普通矩形（type=process/output）的 `left`/`right` → **下一层**，正交折线（垂直→水平→垂直，无斜线）

#### loops（回环，可选，虚线）

当流程中存在「回到先前步骤」的逻辑时使用，例如：
- 修复后重新审查（`apply_fix → entry`）
- 重试（`retry → checkpoint`）
- 循环直到满足条件（`recheck → validate`）

```json
{ "from": "apply_fix", "to": "entry", "label": "修复后重新审查", "path": "left_edge" }
```

字段说明：
- `from`：回环起点节点 id（通常是最后一步）
- `to`：回环终点节点 id（通常是流程起点或某个检查点）
- `label`：回环标签，显示在虚线旁
- `path`：固定为 `"left_edge"`（沿图左边缘路由）

**注意**：
- 回环起点到终点之间**不要**在 edges 里重复画边，否则会重复渲染
- loops 里的 from/to 节点**不参与** depth 计算

#### legend

通常留空 `[]`，脚本会使用默认 5 色图例。如需自定义：

```json
[
  { "label": "AI 执行",   "fill": "#E6F1FB", "stroke": "#185FA5" },
  { "label": "输出/报告", "fill": "#EEEDFE", "stroke": "#534AB7" },
  { "label": "决策点",    "fill": "#FAEEDA", "stroke": "#854F0B" },
  { "label": "脚本",      "fill": "#E1F5EE", "stroke": "#0F6E56" },
  { "label": "终止",      "fill": "#FCEBEB", "stroke": "#A32D2D" }
]
```

### 3. 调用脚本生成 HTML

```bash
python3 <skill_dir>/scripts/flowchart.py <nodes.json> --out docs/decision-flowchart.html
```

脚本会：
- 校验 id 唯一性、side/type/role 合法性、from/to 引用合法性
- 自动计算层级（决策侧支同层 / 普通分叉下层 / 汇合点 = max(入边)+1）
- 自动计算 x（side 决定）和 y（按层级 + 节点高度）
- 渲染连线（水平侧支 / 正交折线 / 垂直主流程 / 汇合三段 / 回环虚线）
- 自动 viewBox + 底部图例
- 输出自包含 HTML

## nodes.json 示例

- `docs/halucatch-v2-nodes.json` — 完整示例（含 loop 回环、三叉分支、汇合点）
- `docs/halucatch-nodes.json` — 基础示例
- `docs/security-review-nodes.json` — 多决策点示例
- `docs/self-nodes.json` — 最小示例（9 节点）

## 自检清单

- [ ] 入口节点 type=entry 在最顶部
- [ ] 每条边都有 side 字段（bottom/left/right）
- [ ] 决策菱形的 side=left/right 是侧支（同层水平连线）
- [ ] 普通矩形的 side=left/right 是分叉（下层正交折线）
- [ ] 一节点一 role，混合步骤已拆分
- [ ] 汇合点（多条入边到同一节点）不需要特殊处理，脚本自动识别
- [ ] 回环用 loops 字段，不在 edges 里重复
- [ ] 所有节点 id 在 edges 的 from/to 中都被引用（无孤立节点）
- [ ] 图例留空 `[]`
