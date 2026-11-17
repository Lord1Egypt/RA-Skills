<div align="center">

# 🛡️ 安全生产标准顾问

**safety-standards-advisor**

一个 WorkBuddy（AI）技能：以**国家法律法规为依据、以行业标准（GB / AQ / TSG / JGJ 等）为细则**，帮你解决工作中遇到的安全生产的合规与技术问题。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-orange.svg)](https://www.workbuddy.cn/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple.svg)](#安装跨平台)
[![Hermes](https://img.shields.io/badge/Hermes%20Agent-compatible-teal.svg)](#安装跨平台)
[![Codex](https://img.shields.io/badge/Codex%20CLI-compatible-green.svg)](#安装跨平台)
[![Standards](https://img.shields.io/badge/standards-7074-green.svg)](#数据资产)
[![Laws](https://img.shields.io/badge/laws-108-red.svg)](#数据资产)

</div>

---

> 💡 **设计原则：法律层级优先** —— 法律 > 行政法规 > 部门规章 > 规范性文件 > 强制性国标 > 行业标准。
> 回答任何安全生产问题时，先给出**适用的法定义务来源**，再补**对应的技术标准条款**。

## ✨ 能做什么

- 🎯 **合规答疑**：按主题回答安全生产合规要求 —— 用电安全、高处作业、有限空间、特种设备、粉尘防爆、机械安全、危化品、职业健康、建筑施工、消防、应急管理
- 📚 **法规检索**：按四级法律渊源排序，检索适用的法律法规；覆盖 **108 部**（法律 20 / 行政法规 27 / 部门规章 57 / 规范性文件 4）
- 🔧 **标准检索**：按标准号 / 关键词检索 **7074 条**国家标准与行业标准
- 📖 **正文要点**：读取具体标准的正文要点（标准库文字版可直接引用；扫描件无文字层会提示查找文字版）
- 🛠️ **可执行建议**：给出「法定义务 → 标准条款 → 落实建议」的结构化回答

## 📌 适用场景

- ✅ 隐患排查与合规义务判定
- ✅ 特殊作业管理（动火、高处、有限空间、临时用电等）
- ✅ 设备验收与特种设备合规
- ✅ 个体防护用品选型
- ✅ 事故处置与应急管理
- ✅ 安全生产标准化建设

## 🚀 安装（跨平台）

本技能兼容主流 AI 编码助手与 Agent 框架。先 clone，再按你用的工具放到对应目录即可：

```bash
git clone https://github.com/fengeail/safety-standards-advisor.git
```

### 各平台安装位置

| 平台 | 安装目录 | 加载方式 | 兼容文件 |
| --- | --- | --- | --- |
| **WorkBuddy** | `~/.workbuddy/skills/safety-standards-advisor/` | 自动识别 `SKILL.md` | `SKILL.md` |
| **Claude Code** | `.claude/skills/safety-standards-advisor/` | 自动识别 `SKILL.md` + `allowed-tools` | `SKILL.md` |
| **Hermes Agent** | `~/.hermes/skills/safety-standards-advisor/` | 自动识别 `SKILL.md`（兼容 agentskills.io） | `SKILL.md` |
| **OpenClaw** | 技能目录 | 兼容 agentskills.io 开放标准 | `SKILL.md` |
| **Codex CLI** | 项目根目录 | 自动读取 `AGENTS.md` | `AGENTS.md` |
| **Cursor** | 项目根 或 `.cursor/skills/` | 读取 `.cursorrules` | `.cursorrules` |

一键复制命令：

```bash
# WorkBuddy
cp -r safety-standards-advisor ~/.workbuddy/skills/

# Claude Code（项目级）
mkdir -p .claude/skills && cp -r safety-standards-advisor .claude/skills/

# Hermes Agent
cp -r safety-standards-advisor ~/.hermes/skills/

# Codex CLI / Cursor —— 直接在项目根使用，无需复制
cd safety-standards-advisor && codex   # Codex 自动读 AGENTS.md
# Cursor 自动读 .cursorrules
```

安装后直接对话即可触发，例如：

> 我们车间粉尘比较大，除尘系统有哪些法定要求？

> 登高作业 2 米以上需要办理哪些手续？

> GB 30871 动火作业有什么要求？

### 兼容性说明

- 本技能的脚本仅用 **Python 标准库**（csv/json/os/argparse），无第三方依赖，任何平台都能跑。
- 各平台的加载入口文件已全部内置（`SKILL.md` / `AGENTS.md` / `.cursorrules`），互不冲突。
- 正文件索需要你自行配置标准库（见下文「用自己的标准库重建索引」）；仅做法规/标准号检索则开箱即用。

## 📦 数据资产

随技能附带的索引文件（**不含标准全文，仅做索引与要点归纳**）：

| 文件 | 说明 |
| --- | --- |
| `references/标准目录.csv` | 全量标准索引（标准号 / 标题 / 主题 / 格式 / 相对路径），共 **7074 条** |
| `references/stdno_index.json` | 标准号 → 文件路径 的去重映射 |
| `references/law_index.json` | **108 部**国家法律法规四级分层索引（法律 20 / 行政法规 27 / 部门规章 57 / 规范性文件 4） |
| `references/topics/*.md` | **11 篇**主题手册（含「核心适用法律法规」章节）+ 法律层级速查 |
| `scripts/lookup.py` | 检索引擎：法律法规 / 标准号 / 关键词 / 正文 |
| `scripts/read_std.py` | 读取标准正文（自动适配 .docx 副本、跳过加密件） |
| `scripts/extract_text.py` | 把标准库抽取成可检索的文本语料 |
| `scripts/setup.py` | 用你自己的标准库重建索引 |

## 🔄 用自己的标准库重建索引（可选）

本技能自带的索引是从作者整理的标准库蒸馏而来。如果你想**用自己的标准库**重建：

```bash
python scripts/setup.py --root "D:/你的标准库"
```

它会遍历目录、用正则识别标准号、按文件夹推断主题，生成 `references/标准目录.csv` 和 `references/stdno_index.json`。

如需正文级检索，再把你的标准库抽取成文本并生成 `index.jsonl`：

```bash
python scripts/extract_text.py --root "D:/你的标准库" --out "D:/你的语料库"

export SAFETY_STANDARDS_ROOT="D:/你的标准库"
export SAFETY_CORPUS="D:/你的语料库"   # 含 index.jsonl
```

## 📐 法律层级速查

```
法律（全国人大）          《安全生产法》《消防法》《职业病防治法》…
   ↓
行政法规（国务院）        《生产安全事故报告和调查处理条例》…
   ↓
部门规章（应急管理部等）   《安全生产违法行为行政处罚办法》…
   ↓
规范性文件                各类通知、实施意见
   ↓
强制性国标（GB）          GB 28526、GB 50016…
   ↓
行业标准                  AQ / TSG / JGJ / DL / SH …
```

## ⚖️ 合规与版权声明

- 📜 国家 / 行业标准**受版权保护**，本技能**只做索引与要点归纳，不随附、不重新分发标准全文**。
- 🔍 标准正文请通过正规渠道获取（国家标准全文公开系统、行业标准出版机构等）。
- ⚠️ 本技能输出**仅供参考**，不能替代具有资质的安全评价、法律意见或现场专业判断。涉及重大安全决策，请依规委托有资质的机构。

## 📁 目录结构

```
safety-standards-advisor/
├── SKILL.md                     # 技能定义（WorkBuddy / Claude Code / Hermes / OpenClaw）
├── AGENTS.md                    # Codex CLI 项目指令
├── .cursorrules                 # Cursor 规则
├── README.md
├── LICENSE
├── references/
│   ├── 标准目录.csv             # 7074 条标准索引
│   ├── stdno_index.json         # 标准号 → 路径映射（2070 个）
│   ├── law_index.json           # 108 部法律法规四级索引
│   └── topics/                  # 11 篇主题手册
│       ├── 用电安全.md
│       ├── 高处作业.md
│       ├── 有限空间.md
│       ├── 特种设备.md
│       ├── 粉尘防爆.md
│       ├── 机械安全.md
│       ├── 危险化学品.md
│       ├── 职业健康与个体防护.md
│       ├── 消防.md
│       ├── 应急管理.md
│       └── 法律层级速查.md
└── scripts/
    ├── lookup.py                # 检索引擎
    ├── read_std.py              # 正文读取
    ├── extract_text.py          # 语料抽取
    └── setup.py                 # 重建索引
```

## 🙏 致谢

- 标准全文来源：国家标准全文公开系统、各行业标准发布机构
- 技能运行环境：[WorkBuddy](https://www.workbuddy.cn/)

---

<div align="center">

**⭐ 如果这个技能帮到了你，欢迎 Star 支持一下！**

</div>
