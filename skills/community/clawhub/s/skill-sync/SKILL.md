---
name: skill-sync
version: 1.0.0
description: Automatically sync local skills to ClawHub and GitHub. Detects new/modified skills, publishes to ClawHub, commits to GitHub, and maintains sync status.
author: sunnyhot
license: MIT
keywords:
  - skill-sync
  - clawhub
  - github
  - auto-publish
  - auto-sync
  - skill-manager
---

# Skill Sync - 自动同步 Skills 到 ClawHub & GitHub

**一键同步你的所有 skills**

---

## ✨ 核心功能

### 🔄 **自动同步**
- ✅ 检测新增的 skills
- ✅ 检测修改的 skills
- ✅ 自动发布到 ClawHub
- ✅ 自动提交到 GitHub
- ✅ 记录同步状态

### 📊 **状态管理**
- ✅ 跟踪每个 skill 的同步状态
- ✅ 记录 ClawHub 发布 ID
- ✅ 记录 GitHub commit hash
- ✅ 提供同步报告

### 🔍 **智能检测**
- ✅ 检测 SKILL.md 文件变化
- ✅ 检测 scripts 文件变化
- ✅ 检测 package.json 变化
- ✅ 忽略临时文件和缓存

---

## 🚀 使用方法

### 1. **手动触发同步**

```bash
node /Users/xufan65/.openclaw/workspace/skills/skill-sync/scripts/sync.cjs
```

**功能**:
- 扫描所有 skills
- 检测需要同步的 skills
- 发布到 ClawHub
- 提交到 GitHub
- 推送同步报告

---

### 2. **自动监控模式**（推荐）

创建定时任务，每小时自动检查并同步：

```bash
openclaw cron add \
  --name "skill-sync" \
  --cron "0 * * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --wake now \
  --deliver \
  --message "运行 skill-sync: 检查所有 skills 的变化，自动同步到 ClawHub 和 GitHub。报告格式用中文。"
```

**运行频率**:
- 每小时检查一次（`0 * * * *`）
- 或每 30 分钟检查一次（`*/30 * * * *`）

---

### 3. **查看同步状态**

```bash
cat /Users/xufan65/.openclaw/workspace/memory/skill-sync-status.json
```

**包含内容**:
- 每个 skill 的同步状态
- ClawHub 发布 ID
- GitHub commit hash
- 最后同步时间
- 版本信息

---

## 📋 工作流程

```
┌─────────────────┐
│  扫描 Skills    │
│  - 检测新增     │
│  - 检测修改     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  生成同步列表   │
│  - 新 skills    │
│  - 修改的 skills│
└────────┬────────┘
         │
         ▼
     有需要同步的？
         │
    ┌────┴────┐
   Yes       No
    │          │
    ▼          ▼
┌───────┐  ┌──────────┐
│同步流程│  │推送报告  │
└───┬───┘  │无需同步  │
    │      └──────────┘
    ▼
┌─────────────────┐
│  1. Git Commit  │
│  2. ClawHub Pub │
│  3. Git Push    │
│  4. 更新状态    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  推送同步报告   │
│  - 成功列表     │
│  - 失败列表     │
│  - 状态更新     │
└─────────────────┘
```

---

## 🔧 配置选项

### `config/settings.json`

```json
{
  "skillsDir": "/Users/xufan65/.openclaw/workspace/skills",
  "statusFile": "/Users/xufan65/.openclaw/workspace/memory/skill-sync-status.json",
  "gitRepo": "/Users/xufan65/.openclaw/workspace",
  "clawhubConfig": {
    "autoPublish": true,
    "requireConfirmation": false
  },
  "gitConfig": {
    "autoCommit": true,
    "autoPush": true,
    "commitMessage": "Auto-sync skills to ClawHub"
  },
  "ignorePatterns": [
    "node_modules",
    ".git",
    "*.log",
    "*.tmp"
  ]
}
```

---

## 📊 同步状态文件

### `memory/skill-sync-status.json`

```json
{
  "lastSync": "2026-03-12T14:30:00+08:00",
  "skills": {
    "deals-hunter": {
      "version": "3.0.0",
      "clawhubId": "k97c0kee4b0t8rmf4490m9r9bn82s082",
      "clawhubPublished": "2026-03-12T10:00:00+08:00",
      "gitCommit": "7779310",
      "gitPushed": "2026-03-12T14:30:00+08:00",
      "status": "synced"
    },
    "failure-monitor": {
      "version": "1.0.0",
      "clawhubId": "k973cr1p4k5g3mh36yjp24agg182rcsa",
      "clawhubPublished": "2026-03-12T14:30:00+08:00",
      "gitCommit": "22b355d",
      "gitPushed": "2026-03-12T14:35:00+08:00",
      "status": "synced"
    }
  }
}
```

---

## 🎯 同步条件

### **需要同步的情况**:

1. **新增 Skill**
   - `skills/` 目录下出现新的 skill 文件夹
   - 包含 `SKILL.md` 文件

2. **版本更新**
   - `SKILL.md` 中的 `version` 字段变化
   - `package.json` 中的 `version` 字段变化

3. **文件修改**
   - `SKILL.md` 被修改
   - `scripts/` 目录下的文件被修改
   - `config/` 目录下的文件被修改

4. **未同步状态**
   - 状态文件中没有该 skill 的记录
   - 状态为 `pending` 或 `failed`

---

## 🔒 安全考虑

- ✅ **只同步 skills 目录**：不会修改其他文件
- ✅ **保留 Git 历史**：使用 `git add` + `git commit`
- ✅ **ClawHub 验证**：发布前检查 skill 格式
- ✅ **错误处理**：发布失败不会中断整个流程
- ✅ **回滚支持**：可以通过 Git 回滚到之前的状态

---

## 📝 Discord 推送格式

### **同步成功**

```markdown
# ✅ Skills 同步完成

**同步时间**: 2026-03-12 14:30:00
**总计**: 3 个 skills

## 📦 成功同步

### 1. **failure-monitor** v1.0.0
- ✅ ClawHub: k973cr1p4k5g3mh36yjp24agg182rcsa
- ✅ GitHub: commit 22b355d
- 📅 发布时间: 2026-03-12 14:30:00

### 2. **deals-hunter** v3.0.0
- ✅ ClawHub: k97c0kee4b0t8rmf4490m9r9bn82s082
- ✅ GitHub: commit 7779310
- 📅 发布时间: 2026-03-12 10:00:00

---

**🔗 快速链接**:
- ClawHub: https://clawhub.com/skill/failure-monitor
- GitHub: https://github.com/sunnyhot/deals-hunter
```

### **无需同步**

```markdown
# ℹ️ Skills 检查完成

**检查时间**: 2026-03-12 15:00:00
**总计**: 10 个 skills

✅ 所有 skills 已是最新状态，无需同步
```

### **部分失败**

```markdown
# ⚠️ Skills 同步完成（部分失败）

**同步时间**: 2026-03-12 14:30:00
**成功**: 2 个 | **失败**: 1 个

## ✅ 成功同步
- failure-monitor v1.0.0
- deals-hunter v3.0.0

## ❌ 失败列表
### skill-name v1.0.0
- **错误**: ClawHub API rate limit exceeded
- **建议**: 稍后重试或手动发布

---

**建议**: 检查失败的 skills 并手动修复
```

---

## 📁 文件结构

```
skills/skill-sync/
├── SKILL.md                      # 技能说明
├── scripts/
│   ├── sync.cjs                  # 主同步脚本
│   ├── scan-skills.cjs           # 扫描 skills
│   ├── publish-clawhub.cjs       # 发布到 ClawHub
│   └── git-sync.cjs              # Git 同步
├── config/
│   └── settings.json             # 配置选项
└── package.json                  # 依赖管理
```

---

## 🔧 命令行选项

### **完整同步**

```bash
node scripts/sync.cjs --all
```

同步所有需要同步的 skills

### **指定 Skill**

```bash
node scripts/sync.cjs --skill failure-monitor
```

只同步指定的 skill

### **仅 ClawHub**

```bash
node scripts/sync.cjs --clawhub-only
```

只发布到 ClawHub，不提交到 GitHub

### **仅 GitHub**

```bash
node scripts/sync.cjs --git-only
```

只提交到 GitHub，不发布到 ClawHub

### **Dry Run**

```bash
node scripts/sync.cjs --dry-run
```

只检查需要同步的 skills，不实际执行

---

## 🎯 最佳实践

### 1. **运行频率**
- ✅ 推荐：每小时检查一次
- ✅ 可接受：每 30 分钟检查一次
- ❌ 不推荐：超过 2 小时（可能错过更新）

### 2. **版本管理**
- ✅ 每次修改后更新 `version` 字段
- ✅ 使用语义化版本（SemVer）
- ✅ 在 SKILL.md 中记录更新日志

### 3. **提交信息**
- ✅ 使用清晰的 commit message
- ✅ 包含 skill 名称和版本
- ✅ 描述主要修改内容

---

## 🚨 故障排除

### **Q: ClawHub 发布失败怎么办？**

A: 检查以下几点：
1. ClawHub CLI 是否已登录（`clawhub login`）
2. SKILL.md 格式是否正确
3. 是否有网络问题
4. 可以稍后重试或手动发布

### **Q: Git 推送失败怎么办？**

A: 检查以下几点：
1. Git 仓库是否正确配置
2. 是否有网络问题
3. 是否有冲突需要解决
4. 可以手动 `git push` 解决

### **Q: 如何查看详细日志？**

A: 查看日志文件：
```bash
cat /Users/xufan65/.openclaw/workspace/memory/skill-sync-log.json
```

---

## 📝 更新日志

### v1.0.0 (2026-03-12)
- ✅ 初始版本
- ✅ 支持自动检测 skills 变化
- ✅ 支持自动发布到 ClawHub
- ✅ 支持自动提交到 GitHub
- ✅ 支持同步状态跟踪
- ✅ 支持 Discord 推送通知

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/sunnyhot/skill-sync

---

**🎉 让你的 skills 管理更加自动化！**
