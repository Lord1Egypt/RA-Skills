# Skill-Updater

> 本地修改保护式 clawhub skill 更新器。

---

## 中文说明

### 解决问题

你修改了某个从 clawhub 安装的 skill，后来 clawhub 发布了新版本。直接执行 `clawhub update` 会**覆盖**你的本地修改。

Skill-Updater 在更新时**尝试保留你的修改**。如果无法自动合并，会报告冲突，由你决定如何处理。

### 核心功能

| 特性 | 说明 |
|------|------|
| **本地修改保护** | 修改被保存为 unified diff patch，不被 clawhub update 覆盖 |
| **Patch 合并** | clawhub 更新后，尝试将 patch 应用到新版文件 |
| **冲突可见** | 无法自动合并时，显示清晰的 diff 对比 |
| **无强制覆盖** | 任何时候都可以选择接受新版、丢弃修改 |

### 工作流程

```
Step 1: 修改 skill 文件
Step 2: 首次运行自动保存 patch
        (.skill-updater/originals/ + mod.patch)
Step 3: clawhub 发布新版
Step 4: python3 git_update.py --apply
        → clawhub update 下载新版
        → patch --dry-run 试探合并
        → 成功：写入新版 ✅
        → 失败：显示 diff，用户手动处理
```

### 冲突处理

| 情况 | 行为 |
|------|------|
| patch 成功应用 | 新版 + 修改均保留 ✅ |
| patch 失败（同一区域被双方修改） | 显示 diff，用户手动决策 |
| 无本地修改 | 直接 clawhub update ✅ |
| 选择丢弃修改 | 删除 patch，接受新版 |

### 文件结构

```
skill-dir/
├── .skill-updater/
│   ├── mod.patch       # 本地修改的 unified diff（增量，极小）
│   └── originals/       # 安装时的原始文件快照（用于 diff 对比）
└── [skill 文件]
```

### CLI 命令

```bash
# 预览（dry-run）
python3 git_update.py

# 实际更新
python3 git_update.py --apply

# 仅更新指定 skill
python3 git_update.py --apply --skill <slug>

# 查看已保存的修改
python3 git_update.py --show-patch

# 丢弃修改（接受新版）
python3 git_update.py --discard --skill <slug>

```


## English

### Problem Solved

You modified a clawhub-installed skill. Later, the author publishes a new version on clawhub. Running `clawhub update` directly **overwrites your local changes**.

Skill-Updater **tries to preserve your changes** during the update. If auto-merge fails, it reports the conflict for you to decide.

### Features

| Feature | Description |
|---------|-------------|
| **Local Mod Protection** | Changes saved as unified diff, not overwritten by clawhub update |
| **Patch Merge** | After clawhub update, applies saved patch to new version |
| **Conflict Visibility** | Shows clear diff when auto-merge fails |
| **No Forced Overwrite** | Always choose whether to keep or discard changes |

### Workflow

```
Step 1: You modify skill files
Step 2: First run saves patch automatically
        (.skill-updater/originals/ + mod.patch)
Step 3: New version released on clawhub
Step 4: python3 git_update.py --apply
        → clawhub update downloads new version
        → patch --dry-run attempts to merge
        → Success: written ✅
        → Fail: show diff, user decides
```

### Conflict Handling

| Scenario | Result |
|----------|--------|
| Patch applies cleanly | New version + modifications preserved ✅ |
| Same area modified by both | Show diff, manual decision |
| No local modifications | Direct clawhub update ✅ |
| Choose to discard | Delete patch, accept new version |

### CLI

```bash
# Dry-run
python3 git_update.py

# Apply all
python3 git_update.py --apply

# Specific skill
python3 git_update.py --apply --skill <slug>

# Show saved patch
python3 git_update.py --show-patch

# Discard modifications
python3 git_update.py --discard --skill <slug>

```


## License

MIT-0 (Free to use, modify, and redistribute. No attribution required.)
