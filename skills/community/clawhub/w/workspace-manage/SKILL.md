---
name: workspace-manager
description: |
  用于管理和维护 OpenClaw 工作区的结构。当用户提到工作区混乱、需要整理文件夹、或者希望建立标准目录结构时使用。提供自动归档、分类、清理和健康审计功能。
metadata:
  pattern: ["pipeline", "tool-wrapper"]
---

### Design Pattern
此技能使用 **Pipeline（流水线）模式** 来执行多步骤工作区管理，并通过 **Tool Wrapper（工具包装器）模式** 安全地封装文件系统操作。**优先调用配套脚本**，避免在 Prompt 中内联复杂 bash 命令，以控制 Token 成本并提升执行稳定性。

# Workspace Manager

此技能旨在保持工作区的整洁和高效，将人类文件与 Agent 文件分离，并提供一站式维护能力。

---

## 标准目录结构 (Standard Structure)

```
~/.openclaw/workspace/
├── Workspace_Human/          # ❶ 供人类使用的文件（输入、输出、备份）
│   ├── input/                # 用户提供或导入的原始文件
│   ├── output/               # 生成的产物（图片、PDF、文档）
│   │   ├── images/           # 图片文件
│   │   ├── docs/            # 文档文件 (PDF, DOCX)
│   │   └── data/            # 结构化数据 (JSON, CSV)
│   ├── backup/              # 备份文件（手动 + 自动）
│   └── temp/               # 临时文件（CDP 截图、缓存等，可安全清理）
│
├── Workspace_Agent/         # ❷ 供 Agent 之间交互的文件
│   ├── memory/             # 每日日志 (YYYY-MM-DD.md) + 长期记忆
│   ├── skills/             # 已安装的技能目录
│   ├── subagents/          # 永久子 agent 配置
│   ├── shared_context/     # 多 agent 共享上下文
│   ├── artifacts/          # 中间产物（构建产物、待整理文件）
│   ├── cache/              # 可复用的缓存数据
│   ├── logs/               # 操作日志
│   ├── skills_custom/      # 自定义编写的技能
│   ├── prompts/            # 常用提示词模板
│   └── kb/                 # Agent 知识库
│
├── archive/                  # 归档目录（按 YYYY-MM/ 组织）
├── scripts/                  # 本地脚本（workspace-manager 专用）
└── secret/                   # 敏感凭据
```

---

## 核心文件保护（永不删除）

以下文件无论任何情况都受到保护：
- `MEMORY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`, `HEARTBEAT.md`
- `.git/`, `memory/`, `skills/`, `subagents/`, `Workspace_Human/`

---

## Pipeline 工作流

**所有步骤均通过配套脚本执行**。推荐使用一键全量 Pipeline，复杂场景可单独触发某一阶段。

### 推荐：一键全量 Pipeline

```bash
# 执行完整 5 步流水线（Audit → Organize → Clean → Archive → Sync）
bash {{SKILL_DIR}}/scripts/pipeline.sh --all

# 仅预览（不实际执行任何写入操作）
bash {{SKILL_DIR}}/scripts/pipeline.sh --all --dry-run

# 执行指定步骤
bash {{SKILL_DIR}}/scripts/pipeline.sh audit organize
```

---

### Step 1 — 健康审计 (Audit)

```bash
bash {{SKILL_DIR}}/scripts/health-check.sh
```

自动检查：断链、空目录、大文件(>10MB)、畸形命名、磁盘占用、最近活动。
输出 0-100 健康评分及分级建议。

### Step 2 — 规范化 (Standardize)

```bash
bash {{SKILL_DIR}}/scripts/standardize.sh
```

确保标准目录结构完整，检测根目录散落文件并给出整理建议。

### Step 3 — 自动整理 (Organize)

```bash
bash {{SKILL_DIR}}/scripts/organize.sh
```

将 `Workspace_Agent/artifacts/` 中的散落文件按类型移动到 `Workspace_Human/output/` 对应子目录：

| 文件类型 | 目标位置 |
|----------|----------|
| `*.png`, `*.jpg`, `*.webp`, `*.gif` | `Workspace_Human/output/images/` |
| `*.pdf`, `*.docx`, `*.doc` | `Workspace_Human/output/docs/` |
| `*.json`, `*.csv`, `*.xml` | `Workspace_Human/output/data/` |
| `*screenshot*`, `cdp_tmp_*`, `*.tmp` | `Workspace_Human/temp/` |

### Step 4 — 安全清理 (Clean)

```bash
# 预览（默认，永远先预览）
python3 {{SKILL_DIR}}/scripts/cleanup.py

# 执行清理（移动到系统 trash，可恢复）
python3 {{SKILL_DIR}}/scripts/cleanup.py --execute

# 按条件清理
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-age 30 --execute   # 30天以上
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-size 50            # >50MB
```

**保护规则**：永不删除 `.git/`、`memory/`、`skills/`、`Workspace_Human/`、最近 24h 文件及所有核心配置文件。

### Step 5 — 归档 (Archive)

```bash
# 交互式归档（7天以上文件，按月组织）
bash {{SKILL_DIR}}/scripts/archive.sh

# 自定义天数
DAYS=30 bash {{SKILL_DIR}}/scripts/archive.sh
```

归档结构：`archive/YYYY-MM/`。仅处理 `Workspace_Agent/artifacts/`。

### Step 5 — 云端同步 (Sync) ⭐ 可选扩展

```bash
bash {{SKILL_DIR}}/scripts/sync.sh
```

**此步骤为可选扩展**，需要 `gog` CLI 已安装并认证。未安装或未认证时自动跳过，不阻断其他 Pipeline 步骤。

**同步范围**（可通过 `config/sync-config.json` 配置开关）：
- ✅ `Workspace_Human/` 全部内容 → Google Drive `AI_Workspace/Workspace_Human/`
- ✅ `Workspace_Agent/` 全部内容 → Google Drive `AI_Workspace/Workspace_Agent/`（默认关闭）
- ✅ 核心配置文件（MEMORY.md 等） → Google Drive `AI_Workspace_Backup/`

**启用同步**：安装 `gog` CLI 并运行 `gog auth login` 即可自动启用。

**关闭同步**：删除 `gog` 或不运行 `gog auth login`，Pipeline 自动跳过此步骤。

---

## 常用命令速查

| 任务 | 命令 |
|------|------|
| **一键全量** | `bash {{SKILL_DIR}}/scripts/pipeline.sh --all` |
| 健康审计 | `bash {{SKILL_DIR}}/scripts/health-check.sh` |
| 规范化 | `bash {{SKILL_DIR}}/scripts/standardize.sh` |
| 整理文件 | `bash {{SKILL_DIR}}/scripts/organize.sh` |
| 预览清理 | `python3 {{SKILL_DIR}}/scripts/cleanup.py` |
| 执行清理 | `python3 {{SKILL_DIR}}/scripts/cleanup.py --execute` |
| 归档旧文件 | `bash {{SKILL_DIR}}/scripts/archive.sh` |
| 云端同步 | `bash {{SKILL_DIR}}/scripts/sync.sh` ⭐可选 |

---

## 目录命名规则

- **所有目录名**：kebab-case，无空格，无特殊字符
- 示例：`Workspace_Human`, `Workspace_Agent`, `shared_context`, `skills_custom`
- **文件扩展名**：全部小写

## 最佳实践

- **每次会话结束前**：`bash {{SKILL_DIR}}/scripts/pipeline.sh audit organize`
- **每周定期维护**：`bash {{SKILL_DIR}}/scripts/pipeline.sh --all`（完整流水线）
- **永远先预览再执行**：特别是 `cleanup.py`（默认就是预览模式）
- **永远用 `trash` 代替 `rm`**：所有脚本均使用 `trash-put`，误删可从系统回收站恢复
- 引导用户将临时文件生成在 `Workspace_Agent/artifacts/`，会话结束后由 Pipeline 自动整理
