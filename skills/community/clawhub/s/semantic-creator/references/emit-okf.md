# Phase 3 · Emit — Google OKF（默认目标，v0.1）

输入：Phase 2 批准的建模决策集。产出：OKF v0.1 bundle——markdown 文件目录，每文件一 concept，frontmatter 用 YAML。唯一硬要求：每个非保留 `.md` 有可解析 frontmatter 且含非空 `type`，其余皆软约定。来源：Open Knowledge Format v0.1（Google Cloud, 2026-06）。
字段语义（grain/kind/additivity 等）见 `emit-yaml.md` §2–§4，两个目标共享同一模型。生成后跑 `verify.md`。

## §1 Bundle 布局

```text
<bundle>/                         # = 域名（catalog domain）
├── index.md                      # 保留：根目录清单（唯一可带 frontmatter 的 index）
├── log.md                        # 保留（可选）：变更历史，新→旧
├── facts/
│   ├── index.md
│   └── <fact>.md                 # 每个 fact 一个 concept
├── dimensions/
│   ├── index.md
│   └── <dim>.md
├── metrics/
│   └── <measure>.md              # 可选拆
└── references/
    └── <operation>.md            # 每个 source operation 一个 API Endpoint concept
```

Concept ID = 去掉 `.md` 的 bundle 相对路径（`facts/rfq_line`）。**ID = 文件路径 = 身份**；确认后不重命名（会断链）。

**多 bundle**：≥2 个 bundle 时在共同父目录生成薄根 `index.md`——每 bundle 一行（domain / 一句 scope / 入口路径），不重复 entry_points、不内联事实维度；单 bundle 不生成。

## §2 语义对象 → OKF concept 映射

| 语义对象 | OKF `type` | 落点 | body 约定段 |
| --- | --- | --- | --- |
| catalog（路由） | `Semantic Catalog` | 根 `index.md`（带 `okf_version`） | 见 §4 |
| fact | `Semantic Fact` | `facts/<fact>.md` | `# Grain` / `# Dimensions` / `# Schema` / `# Citations` |
| dimension | `Dimension` | `dimensions/<dim>.md` | `# Schema`（attributes 表）/ `# Citations` |
| measure | `Metric` | `metrics/<measure>.md` | `# Definition`（additivity, basis, unit）/ `# Citations` |
| source operation | `API Endpoint` | `references/<op>.md` | `# Schema`（inputs/outputs）/ `# Citations` |

`time` 路由轴 → frontmatter `tags` 或 prose。OKF 链接为无类型有向边，关系语义靠 prose（「joins-with」「parent of」）。

## §3 Concept frontmatter（必填 + 推荐）

```yaml
---
type: <见 §2>                    # 必填，唯一硬要求
title: <人类可读名>
description: <一句话>
resource: <底层资产 URI；抽象概念可省>
tags: [<domain>, <axis:value>, ...]
timestamp: <ISO 8601>
---
```

扩展键：把结构化属性（`grain`/`kind`/`business_key`/`additivity`/`role`/`parent_fact`）作为额外 frontmatter 键，便于 agent 检索；body 用结构化 markdown 同步给人读。消费者须容忍未知键。

## §4 保留文件

- **根 `index.md`**：唯一允许 frontmatter 的 index，只放 `okf_version: "0.1"`。
  body 先放 `# Entry Points` 节（每场景一行：`<entry_key>（<axis>: <value>）→ [fact 链接]`，与 catalog `entry_points` 一一对应），再按类型分节列条目——`* [标题](facts/<fact>.md) - 一句描述`。
- **子目录 `index.md`**：不带 frontmatter，只列本目录条目（带描述）。
- **`log.md`**（可选）：`# Update Log` + `## YYYY-MM-DD` 分节，新→旧；条目前导加粗词（**Update**/**Creation**/**Deprecation**）是约定非强制。

## §5 交叉链接

- 用 bundle 绝对路径（`/` 开头）：`[customers](/dimensions/customers.md)`，移动子目录仍稳；关系类型由 prose 表达；消费者须容忍断链（未写知识不算错）。
- 外部来源放 `# Citations` 编号列表，可指向 `references/` 内镜像 concept。完整 concept 示例见 `examples.md` §4。
