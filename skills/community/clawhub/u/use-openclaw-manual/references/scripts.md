# 脚本详细说明

## sync-docs.sh

**位置**: `scripts/sync-docs.sh`

**功能**: 从 GitHub 同步 OpenClaw 官方文档到本地

### 参数

| 参数 | 说明 |
|------|------|
| `--init` | 首次初始化（完整克隆，约 700+ 文件） |
| `--sync` | 增量同步（仅更新变更文件） |
| `--check` | 仅检查更新，不执行同步 |

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_MANUAL_PATH` | `~/.openclaw/workspace/docs/openclaw_manual` | 文档存储路径 |
| `LAST_COMMIT_FILE` | `$OPENCLAW_MANUAL_PATH/.last-docs-commit` | 记录同步的 commit hash |
| `DOC_UPDATE_LOG` | 技能目录内 `docs-update.log` | 同步日志文件路径 |
| `DOC_NOTIFY_CHANNEL` | `webchat` | 通知渠道 |

### 工作流程

1. **获取最新 commit** - 调用 GitHub API 获取 `openclaw/openclaw` 仓库 `docs/` 目录的最新 commit
2. **比较基线** - 读取 `.last-docs-commit` 文件，判断是否有更新
3. **同步文件** - 使用 `git archive` 或 `curl` 下载变更文件
4. **更新基线** - 写入新的 commit hash 到 `.last-docs-commit`
5. **发送通知** - 通过指定渠道发送同步结果

### 输出示例

```
🔄 同步文档更新...

检查更新：github.com/openclaw/openclaw/docs/
当前版本：a1b2c3d
最新版本：e4f5g6h
变更文件：12 个

新增:
  - cli/new-feature.md
  - channels/new-channel.md

更新:
  - concepts/agent.md
  - automation/cron.md

删除:
  - deprecated/old-config.md

同步完成！耗时 8.3s
```

### 通知内容

通过 `openclaw message` 或渠道插件发送通知：

```
📚 OpenClaw 文档已更新

新增：3 个文件
更新：8 个文件
删除：1 个文件

查看详情：~/.openclaw/workspace/docs/openclaw_manual/
```

---

## search-docs.sh

**位置**: `scripts/search-docs.sh`

**功能**: 搜索本地文档库

### 参数

| 参数 | 说明 |
|------|------|
| `--search <词>` | 搜索关键词（必需） |
| `--type <类型>` | 搜索类型：content（内容）, filename（文件名）, title（标题） |
| `--limit <数>` | 结果数量限制（默认：10） |
| `--list <目录>` | 列出目录内容 |
| `--read <文档>` | 阅读文档内容 |
| `--stats` | 显示文档统计 |

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_MANUAL_PATH` | `~/.openclaw/workspace/docs/openclaw_manual` | 文档目录路径 |
| `DOC_UPDATE_LOG` | 技能目录内 `docs-update.log` | 日志文件路径 |

### 搜索类型

#### content（默认）
搜索文件内容，使用 `grep -r`：
```bash
grep -rn "关键词" "$OPENCLAW_MANUAL_PATH" --include="*.md"
```

#### filename
搜索文件名：
```bash
find "$OPENCLAW_MANUAL_PATH" -name "*关键词*.md"
```

#### title
搜索 Markdown 标题（# 开头的行）：
```bash
grep -rn "^#.*关键词" "$OPENCLAW_MANUAL_PATH"
```

### 输出格式

```
📚 搜索结果："cron schedule"

1. automation/cron.md:15
   ## 配置定时任务
   使用 schedule.kind 指定触发类型...

2. cli/cron.md:42
   ### cron add 命令
   添加新的定时任务...

3. concepts/automation.md:8
   定时任务通过 cron 技能管理...

共找到 3 个结果
```

### --stats 输出

```
📊 文档统计

文件总数：719
目录总数：44
总大小：2.3 MB
最后同步：2026-03-11 00:57
当前版本：a1b2c3d
```

---

## run.sh

**位置**: `run.sh`（技能根目录）

**功能**: 技能入口脚本，解析命令行参数并调用相应子脚本

### 参数映射

| 参数 | 调用脚本 |
|------|---------|
| `--init` | `scripts/sync-docs.sh --init` |
| `--sync` | `scripts/sync-docs.sh --sync` |
| `--check` | `scripts/sync-docs.sh --check` |
| `--search` | `scripts/search-docs.sh --search` |
| `--list` | `scripts/search-docs.sh --list` |
| `--read` | `scripts/search-docs.sh --read` |
| `--stats` | `scripts/search-docs.sh --stats` |

### 使用示例

```bash
# 进入技能目录
cd path/to/use-openclaw-manual/

# 初始化
./run.sh --init

# 搜索
./run.sh --search "agent workspace"

# 指定通知渠道
DOC_NOTIFY_CHANNEL=discord ./run.sh --sync
```

---

## 性能优化建议

### 搜索优化

- **限制搜索范围**：如果知道大致目录，先用 `--list` 浏览再用 `--read`
- **使用精准关键词**：避免过短的关键词（如 "config" 会匹配太多）
- **利用文件名搜索**：如果记得文件名片段，用 `--type filename` 更快

### 同步优化

- **增量同步**：日常使用 `--sync` 而非 `--init`
- **定期检查**：配置 cron 每天检查一次即可
- **避免频繁同步**：GitHub API 有速率限制

### 缓存策略

- `.last-docs-commit` 文件记录同步基线，避免重复下载
- 搜索结果可缓存到临时文件（技能未实现，用户可自行扩展）
