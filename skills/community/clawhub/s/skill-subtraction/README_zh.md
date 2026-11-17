# skill-subtraction (技能减法)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](scripts/audit_skills.py)
[![Agents](https://img.shields.io/badge/Compatible%20Agents-7-green)](#安装)

> AI 技能管理的核心是「精而专」，而非「多而全」。

对已安装的 AI 技能进行系统性审计，践行**定期做减法**的理念。扫描全部已安装技能，按类别评估使用价值，生成结构化的**保留 / 归档 / 卸载**建议报告，帮助用户保持技能集精简高效。

灵感来源：Swyx（Latent Space 主播 / smol.ai 创始人）关于 AI 技能管理的观点——大多数人用 AI 的习惯是不断做加法，看到一个技能就装一个，结果堆了几十个，真正用的没几个。

## Demo

![示例审计报告](assets/demo-report.svg)

真实生成的示例：[英文报告](examples/audit_report_en.md) · [中文报告](examples/audit_report_zh.md)

## 为什么需要做减法？

| 问题 | 说明 |
|------|------|
| **认知负荷过重** | 技能越多，选择成本越高，违背提效初衷 |
| **干扰判断** | 过时技能像噪音，干扰面对新问题时的判断 |
| **维护成本高** | 技能需要更新调试，过多意味着无谓的精力消耗 |

## 功能

- **遵循 Agent Skills 规范**：YAML frontmatter 仅包含标准 `name` 与 `description` 字段，非标字段（`version`、`agent_created` 等）统一移入 `metadata:` 或正文，配合英文为主、尾部兼顾中文的触发词描述，保证跨平台 100% 兼容
- **自动扫描**：一键扫描当前 Agent 平台下的所有已安装技能。脚本通过自身路径自动检测所属平台——装在 `~/.workbuddy/skills/` 下就扫 WorkBuddy，装在 `~/.codex/skills/` 下就扫 Codex，以此类推；同时支持扫描当前工作区 `.workbuddy/skills/` 下的项目级技能，以及单独盘点归档库
- **双语输出**：支持中文和英文报告输出，通过 `--lang zh`（默认）或 `--lang en` 控制；stderr 消息、问题描述、审计报告模板均完整双语化
- **多平台兼容**：兼容 WorkBuddy、Codex、Claude Code、Cursor、Cline、Continue、LobsterAI 等采用 `~/.<agent>/skills/` 目录约定的平台；`--all` 可一键扫描机器上所有已安装的平台
- **分类评估**：按开发工程 / 数据集成 / 内容创作 / 专业业务 / 通用生产力 / 元技能 6 大业界功能分类及细分领域评估，六指标打分（使用频率、必要性、当前相关性、启用状态、维护状态、独特价值）
- **智能建议**：自动生成保留 / 归档 / 卸载三类建议，含去重、禁用检测、项目结束检测、批量安装检测等特殊规则
- **安全清理**：归档操作会先保存技能配置，确认后才执行卸载，不擅自删除

## 安装

需要 Python 3.10+ 和遵循 `~/.<agent>/skills/` 目录约定的 AI 助手平台。

| 平台 | 命令 |
|------|------|
| **Codex**（会话内安装器） | `/skill-installer install https://github.com/helloyxs/skill-subtraction` |
| **Claude Code** | `cp -r skill-subtraction ~/.claude/skills/` |
| **Cursor** | `cp -r skill-subtraction ~/.cursor/skills/` |
| **WorkBuddy** | `cp -r skill-subtraction ~/.workbuddy/skills/` |
| 任意平台（克隆） | `git clone https://github.com/helloyxs/skill-subtraction ~/.<agent>/skills/skill-subtraction` |

> Cursor 也会自动加载 `~/.claude/skills/` 和 `~/.codex/skills/`，一份拷贝可同时服务多个平台。

## 使用方法

在对话中直接说：

- "帮我检查一下装了哪些技能"
- "做一次技能减法"
- "哪些技能该留、哪些该删"
- "审计我的技能" / "Audit my installed skills"

技能会自动触发，执行五步工作流：

1. **扫描** — 运行 `python3 scripts/audit_skills.py --lang <zh|en>`，获取所有已安装技能的元数据（含批量安装检测、安装来源统计）
2. **分类** — 按 6 大业界功能分类（开发工程 / 数据集成 / 内容创作 / 专业业务 / 通用生产力 / 元技能）与细分领域归类，独立标识安装来源（用户安装 / 平台预装 / Agent 创建）
3. **评估** — 六指标加权打分，综合评分 24–100 分
4. **建议** — 生成保留 / 归档 / 卸载报告（语言跟随对话语言）
5. **清理** — 用户确认后执行（归档会先保存配置）

### 直接运行扫描脚本

```bash
python3 scripts/audit_skills.py              # 扫描用户级技能（默认中文输出）
python3 scripts/audit_skills.py --lang en    # 指定输出语言为英文
python3 scripts/audit_skills.py --agent codex
python3 scripts/audit_skills.py --all        # 扫描所有已安装的 Agent 平台
python3 scripts/audit_skills.py --workspace /path/to/workspace
python3 scripts/audit_skills.py --skills-dir "C:\Users\admin\AppData\Roaming\LobsterAI\SKILLs"
python3 scripts/audit_skills.py --archives              # 扫描默认归档库
python3 scripts/audit_skills.py --archive-dir /path/to/skill-archive
```

输出同时包含已安装的 `skills` 与独立的 `archived_skills` 归档清单。归档条目包括归档时间、原因、重新激活条件、来源路径，以及是否包含原始 `SKILL.md`。`--archives` 检查每个已检测 Agent 的 `~/.<agent>/skill-archive/`；`--archive-dir` 可指定任意归档目录。归档记录不计入已安装技能数量，也不会参与保留/归档/卸载评分。退出码：0 = 完全正常，2 = 扫描完成但有 error 级问题（方便 CI 接入）。

## 评估框架

| 综合评分 | 建议 | 说明 |
|---------|------|------|
| 80–100 | 保留 | 高价值技能，深度掌握 |
| 50–79 | 归档 | 保存配置后卸载，需要时重新激活 |
| 24–49 | 卸载 | 低价值，直接清理 |

特殊规则（覆盖评分）：零使用 + 不相关 → 直接卸载 · 完全重叠 → 保留最优的一个（去重）· 已禁用且从未手动调用 → 卸载 · 项目结束 → 卸载 · 平台预装 + 从未触发 → 归档。

完整评估框架（分类体系、六指标评分细则、去重优先级、归档规范）见 [`references/evaluation_framework.md`](references/evaluation_framework.md)。

## 审计周期建议

| 频率 | 适用场景 |
|------|---------|
| 每季度 | 技能数量超过 10 个时 |
| 每个项目结束时 | 清理项目级技能 |
| 业务方向调整时 | 评估业务型技能的相关性 |
| 感觉"技能太多"时 | 随时触发 |

## 目录结构

```
skill-subtraction/
├── SKILL.md                          # 技能主定义（工作流 + 触发规则）
├── LICENSE                           # MIT 协议
├── README.md                         # English README
├── README_zh.md                      # 中文说明
├── agents/
│   └── openai.yaml                   # Codex 市场清单
├── assets/
│   └── demo-report.svg               # 示例报告图
├── examples/
│   ├── audit_report_en.md            # 英文示例报告
│   └── audit_report_zh.md            # 中文示例报告
├── scripts/
│   └── audit_skills.py               # 技能扫描脚本，输出结构化 JSON
└── references/
    └── evaluation_framework.md       # 完整评估框架
```

## License

[MIT](LICENSE)
