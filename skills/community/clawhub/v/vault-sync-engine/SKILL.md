---
slug: vault-sync-engine
name: vault-sync-engine
version: "1.0.0"
displayName: 知识库同步引擎
summary: 解决多端冲突、插件配置漂移、iCloud丢笔记痛点，让Obsidian在多设备间稳定同步
license: MIT
description: |-
  Obsidian 多端同步引擎，解决 iCloud/Dropbox 同步冲突、插件配置漂移、`.obsidian/` 目录混乱、
  移动端笔记丢失四大痛点。支持 Git 同步、选择性同步、冲突自愈与配置版本化。

  核心能力:
  - 同步方案选型：Git（推荐）/ iCloud / Dropbox / Syncthing / Obsidian Sync
  - 选择性同步：笔记同步、`.obsidian/` 不同步或分设备同步
  - 冲突检测与自愈：自动识别冲突文件、三路合并、保留冲突副本
  - 插件配置治理：按设备类型分配置、敏感配置排除同步
  - 同步健康看板：上次同步时间、冲突数、未推送提交数

  适用场景:
  - 桌面+手机+平板多端使用 Obsidian
  - 团队/家庭共享部分笔记但保留各自配置
  - 把 Obsidian 当 Git 仓库做版本化知识管理
  - iCloud/Dropbox 同步频繁出问题的用户

  差异化:
  - 同步方案决策表（含免费/付费/自建），原版未提同步
  - 选择性同步规则（`.obsidian/` 分设备），原版无此概念
  - 冲突自愈流程（三路合并 + 副本保留），原版无冲突处理
  - 同步健康看板，原版无监控

  触发关键词: obsidian, sync, 同步, 多端, icloud, dropbox, git, 冲突, conflict, 移动端
tags:
- 自动化
- 知识管理
- 同步引擎
tools:
- read
- exec
---

# 知识库同步引擎

让 Obsidian vault 在多设备间稳定同步。聚焦"不丢笔记、不乱配置、冲突可解"，把同步从黑盒变成可监控的引擎。

## 同步方案选型

| 方案 | 免费 | 冲突处理 | 选择性同步 | 移动端友好 | 推荐场景 |
|:-----|:-----|:---------|:-----------|:-----------|:---------|
| **Git** | 是 | 强（三路合并） | 强（.gitignore） | 需配合（Working Copy） | **技术用户首选** |
| iCloud | 是 | 弱（生成副本文件） | 无 | 强（iOS） | Apple 全家桶 |
| Dropbox | 限免费额度 | 中（生成副本） | 无 | 中 | 跨平台普通用户 |
| Syncthing | 是 | 中 | 弱 | 中（需后台） | 自建同步、隐私敏感 |
| Obsidian Sync | 付费 | 强 | 强 | 强 | 不想折腾、付费用户 |

选型规则：
- 技术用户 + 想要版本历史 → **Git**
- Apple 全家桶 + 不想配 Git → iCloud（接受偶发冲突）
- 跨平台 + 不想付费 → Syncthing
- 不想折腾 + 接受付费 → Obsidian Sync

## Vault 模型与同步边界

| 路径 | 内容 | 是否同步 | 说明 |
|:-----|:-----|:---------|:-----|
| `*.md` | 笔记 | **是** | 核心内容 |
| `<attachments>/` | 附件 | **是** | 笔记引用的资源 |
| `.obsidian/app.json` | 全局设置 | 按设备 | 字体/主题等可分设备 |
| `.obsidian/workspace.json` | 工作区状态 | **否** | 每设备独立 |
| `.obsidian/plugins/` | 插件配置 | 选择性 | 部分插件配置可共享 |
| `.obsidian/community-plugins.json` | 插件清单 | **是** | 保持插件一致 |
| `.trash/` | 回收站 | **否** | 每设备独立 |

## Git 同步方案（推荐）

### 初始化

```bash
cd <vault-path>
git init
cat > .gitignore <<'EOF'
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.trash/
*.tmp
.DS_Store
EOF
git add .
git commit -m "chore: init vault"
git remote add origin <repo-url>
git push -u origin main
```

### 多设备克隆

```bash
# 新设备
git clone <repo-url> <vault-path>
# 用 Obsidian 打开该文件夹
```

### 日常同步工作流

```bash
# 拉取（开始编辑前）
git pull --rebase

# 编辑笔记...

# 推送（结束编辑后）
git add .
git commit -m "docs: update <note>"
git push
```

### 自动同步脚本

```bash
# scripts/vault-sync.sh
#!/usr/bin/env bash
set -e
cd "$(obsidian-cli print-default --path-only)"
git pull --rebase --autostash || {
  echo "冲突需手动解决"
  exit 1
}
git add .
git commit -m "auto: sync $(date +%FT%T)" || echo "无变更"
git push
```

加入 cron/Task Scheduler：
- macOS/Linux：每 30 分钟跑一次
- 编辑前手动 `git pull --rebase`

## 选择性同步规则

### `.obsidian/` 分设备策略

```bash
# .gitignore 排除设备相关配置
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json
.obsidian/cache

# 保留共享配置
# .obsidian/app.json（主题/字体可共享或分设备）
# .obsidian/community-plugins.json（插件清单共享）
# .obsidian/plugins/*/data.json（按需）
```

### 插件配置治理

```bash
# 某些插件配置含设备特定路径，需排除
.obsidian/plugins/obsidian-git/data.json
.obsidian/plugins/local-rest-api/data.json

# 共享插件配置（如 Dataview 查询）
# .obsidian/plugins/dataview/data.json → 保留同步
```

## 冲突检测与自愈

### 冲突识别

```bash
# Git 同步时检测冲突
scripts/vault-sync.sh --check-conflicts
# 输出冲突文件列表
```

iCloud/Dropbox 同步会生成"冲突副本"文件（如 `note (1).md`、`note (conflicted copy).md`）：

```bash
# 扫描冲突副本
scripts/conflict-scan --vault "<vault-path>"
# 识别模式：* (1).md、* (conflicted copy).md、*. conflicted
```

### 三路合并自愈

```bash
# Git 冲突 → 用 merge tool 解决
scripts/conflict-resolve --strategy merge --vault "<vault-path>"

# iCloud/Dropbox 冲突副本 → 三路合并
scripts/conflict-resolve --strategy three-way \
  --base "<vault-path>/note.md" \
  --mine "<vault-path>/note (1).md" \
  --strategy keep-both-on-fail
```

**保留策略**：
- 合并成功：删除冲突副本，保留合并结果
- 合并失败：保留双方，生成 `note (merged-failed).md`，等用户手动处理
- 永不静默丢弃任何一方

## 同步健康看板

```bash
scripts/vault-health
```

输出示例：

```text
=== Vault 同步健康看板 ===
上次同步：2026-07-18 14:30 (8 分钟前)
未推送提交：2
未拉取提交：0
冲突文件：0
游离附件：12
插件配置漂移：1（obsidian-git/data.json）
同步方案：Git (origin: github.com/me/vault)
分支：main

建议：
- 推送 2 个未推送提交
- 检查 obsidian-git 插件配置是否需要排除
```

## 真实场景示例

### 场景1：桌面+手机 Git 同步

```
用户：在手机上用 Working Copy 改了笔记，桌面要拉
执行：
1. 桌面 git pull --rebase --autostash
2. 健康看板确认无冲突
3. 继续编辑
```

### 场景2：iCloud 冲突副本清理

```
用户：iCloud 同步生成了 5 个冲突副本
执行：
1. conflict-scan → 列出 5 个冲突文件
2. conflict-resolve --strategy three-way 逐个合并
3. 3 个合并成功，2 个保留双方等手动处理
4. 报告：清理 3 个冲突，2 个待处理
```

### 场景3：插件配置漂移

```
用户：桌面装了新插件，手机没装
执行：
1. vault-health → 检测到 community-plugins.json 漂移
2. 提示：桌面有 dataview，手机无
3. 用户选择：手机也装（同步配置）或桌面禁用（保持一致）
```

### 场景4：选择性同步附件

```
用户：附件太多，手机不想全同步
执行：
1. 配置 .gitignore 排除大附件目录
2. 用 Git LFS 管理大文件
3. 或切到 Obsidian Sync（支持选择性同步）
```

## FAQ

**Q1: Git 同步在手机上怎么搞？**
A: iOS 用 Working Copy（付费）或 Obsidian Git 插件；Android 用 Termux + git 或 Obsidian Git 插件。Obsidian Git 插件可在 Obsidian 内自动同步。

**Q2: iCloud 经常生成冲突副本怎么办？**
A: 三步：① 用 `conflict-scan` 定期扫描；② 用 `conflict-resolve` 三路合并；③ 考虑切到 Git 或 Obsidian Sync 彻底解决。

**Q3: `.obsidian/workspace.json` 要同步吗？**
A: 不要。每设备的工作区状态独立。同步会导致打开 Obsidian 时窗口布局乱跳。已在 .gitignore 排除。

**Q4: 插件配置要不要同步？**
A: 分情况。`community-plugins.json`（插件清单）同步；插件 `data.json` 看是否含设备特定路径。`obsidian-git` 等含路径的配置建议排除。

**Q5: 冲突合并丢内容了怎么办？**
A: 不会。冲突解决脚本永远保留双方副本。若合并成功也会在 `.trash/` 留一份原文件。Git 还有 `git reflog` 可找回。

## 故障排查

| 现象 | 排查路径 |
|:-----|:---------|
| Git push 被拒 | `git pull --rebase` 先拉 → 解决冲突 → 重试 |
| iCloud 不同步 | 检查 iCloud Drive 是否启用 → 检查网络 → 重启 iCloud 进程 |
| 手机看不到新笔记 | 检查 Git 是否 push → 手机端 pull → 检查 .gitignore 是否误排除 |
| 插件配置丢失 | 检查是否被 .gitignore 排除 → 从 Git 历史恢复 `git checkout HEAD -- path` |
| 冲突副本爆炸 | 用 conflict-resolve 批量处理 → 评估是否换同步方案 |
| 同步慢 | 检查附件大小 → 用 Git LFS → 或排除大附件目录 |

## 依赖说明

### 运行环境
- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent
- **操作系统**: Windows / macOS / Linux（移动端需配合同步工具）
- **Obsidian**: 桌面版 + 移动版（多端场景）

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| `git` | 版本控制 | 必需（Git 方案） | 系统自带或 git-scm.com |
| Git 远程仓库 | 托管 | 必需（Git 方案） | GitHub/GitLab/Gitea |
| `obsidian-cli` | 命令行工具 | 推荐 | npm / 官方仓库 |
| iCloud Drive | 同步服务 | 可选（iCloud 方案） | Apple 内置 |
| Dropbox | 同步服务 | 可选（Dropbox 方案） | dropbox.com |
| Syncthing | 同步服务 | 可选（自建方案） | syncthing.net |
| Obsidian Sync | 同步服务 | 可选（付费方案） | obsidian.md 订阅 |
| Working Copy（iOS） | Git 客户端 | 可选（iOS Git） | App Store |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- Git 远程仓库认证（SSH key 或 Personal Access Token）
- Obsidian Sync 订阅账号（若使用付费方案）
- 无需第三方 API Key

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 必须通过 exec 执行 git 与同步脚本）
- **说明**: 基于自然语言指令驱动 Agent 配置并运维多端同步，含冲突自愈与健康监控
