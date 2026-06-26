# skill-net

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![版本](https://img.shields.io/badge/version-3.0.0-blue)

> 诊断、映射、打分你的 OpenClaw 技能生态系统 — 发现孤儿技能、追踪依赖关系、测量健康度。

## 解决什么问题

当你管理 100+ 个技能时，会遇到这些问题：
- "`/review` 到底被哪些技能依赖？"
- "如果删除 `skill-factory`，哪些功能会坏掉？"
- "哪些技能没有触发词？"
- "整个生态系统的健康度怎么样？"

`skill-net` 扫描所有 SKILL.md，构建依赖图谱，输出可操作的诊断报告。

**触发条件：** "analyze ecosystem"、"full scan"、"ecosystem health"、"skill health"、"what depends on X"、"if I delete Y what breaks"、"find orphans"、"技能生态"

## 功能特性

- **生态健康分** — 四维度加权评分（触发词覆盖率、Metadata 完整率、跨技能引用、内聚度），满分 100
- **依赖图谱** — 映射所有技能引用（含 `skill-*` 命名引用和 `/review`、`/qa` 等协议命令）
- **孤儿检测** — 发现有 SKILL.md 但无触发词的技能
- **影响分析** — 对任意技能，精确显示删除后哪些功能会受影响，按类别分组
- **双语报告** — 通过 `--lang` 参数输出中文、英文或两者
- **结构化输出** — 保存 `ecosystem.json` + `report.md`，便于后续处理

## 快速开始

```bash
# 完整双语扫描（默认：中→英）
python3 scripts/analyze_deps.py

# 仅输出中文报告
python3 scripts/analyze_deps.py --lang=ZH

# 仅输出英文报告
python3 scripts/analyze_deps.py --lang=EN

# JSON 输出（用于自动化）
python3 scripts/analyze_deps.py --json

# 分析特定技能的影响
python3 scripts/analyze_deps.py --impact=review
```

## 输出板块

| 板块 | 说明 |
|------|------|
| 🌡️ 健康分 | 0–100 生态评分 |
| 📊 生态构成 | 核心枢纽 / 桥接节点 / 叶节点 / 孤立技能 / 孤儿技能 |
| 🗑️ 删除影响 | 删除技能 X 后哪些会坏掉 |
| 📋 生态地图 | ASCII 树状图展示技能关系 |

## 健康分公式

```
健康分 = (
  触发词覆盖率 × 30%  +
  Metadata完整率 × 20%  +
  跨技能引用 × 20%  +
  内聚度 × 30%
)
```

## 关键发现（真实数据）

**连接度最高的节点是协议命令，而非 `skill-*` 命名的技能：**

| 技能 | 类型 | 被引用次数 |
|------|------|-----------|
| `/review` | protocol | 59 个技能 |
| `/qa` | protocol | 10 个技能 |
| `/summarize` | CLI | 3 个技能 |
| `/weather` | protocol | 3 个技能 |

传统的依赖检测（只查找 `skill-X` 引用）会**严重低估**真实的生态关系。

## 目录结构

```
skill-net/
├── SKILL.md              # 技能入口 + 定义
├── LICENSE               # MIT 许可证
├── README.md             # 英文说明
├── README_zh.md          # 本文件
├── CONTRIBUTING.md       # 贡献指南
├── .gitignore
├── scripts/
│   ├── analyze_deps.py   # 主分析器（零依赖，自含）
│   └── requirements.txt   # （空 — 无外部依赖）
└── data/
    ├── ecosystem.json    # 结构化数据（运行后生成）
    └── report.md         # Markdown 报告（运行后生成）
```

## 技能分类

| 类型 | 定义 |
|------|------|
| 🔵 核心枢纽 | 被 3+ 个技能引用（高爆炸半径） |
| 🟡 桥接节点 | 既引用他人也被他人引用 |
| 🟢 叶节点 | 引用他人但无人引用它 |
| ⚪ 孤立技能 | 完全自洽，无依赖关系 |
| ⚠️ 孤儿技能 | 有 SKILL.md 但未检测到触发词 |

## 注意事项

- **孤儿 ≠ 损坏** — 许多技能使用 `/protocol` 激活而非 `use when` 短语。孤儿标记是提示，不是错误。
- **影响是单向的** — `A 引用 B` 不意味着 `B 依赖 A`。删除影响显示的是*可能*坏什么，不是*一定*坏什么。
- **不修改任何技能** — 这是只读诊断工具。

## 如何贡献

欢迎贡献！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE](LICENSE)。