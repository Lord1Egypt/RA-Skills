# 路径规范（subagent-orchestrator）

本文档列出 skill 中所有引用的路径和资源，供验证和快速查阅。

## 任务文件路径

| 文件 | 路径规范 | 用途 |
|------|---------|------|
| 任务文件 | `~/.openclaw/workspace/tasks/[子任务]_[日期]_任务.md` | Main Agent 写一次，Subagent 只读 |
| 状态文件 | `~/.openclaw/workspace/tasks/[子任务]_[日期]_状态.md` | Subagent 增量写，Main Agent 快速扫 |
| 数据文件 | `~/.openclaw/workspace/tasks/[子任务]_[日期]_数据.md` | Subagent 增量写，Main Agent 汇总 |
| 最终产出 | `~/.openclaw/workspace/tasks/[项目]_[日期]_最终.md` | Phase 4 输出，用户指定的最终交付 |

## SessionKey 命名规范

格式：`[项目]-[子任务简称]-[YYYYMMDD]`
示例：`travel-xiaohongshu-20260426`

## 依赖 skill

| Skill | 路径 | 触发时调用 |
|-------|------|-----------|
| xiaohongshu-crawler | `skills/xiaohongshu-crawler/SKILL.md` | 小红书攻略抓取 |
| wechat-article-spider | `skills/wechat-article-spider/SKILL.md` | 公众号文章爬取 |
| session-cleanup | `skills/session-cleanup/SKILL.md` | 每日 session 清理（辅助功能） |
| agent-browser-clawdbot | `skills/agent-browser-clawdbot/SKILL.md` | 浏览器自动化（需串行） |

## 依赖脚本

| 脚本 | 路径 | 用途 |
|------|------|------|
| session 扫描 | `skills/session-cleanup/scripts/scan_sessions.sh` | session 清理扫描 |

## 验证检查点

执行任务前，Main Agent 应验证路径可达性：

```bash
# 验证 tasks 目录存在
ls ~/.openclaw/workspace/tasks/ 2>/dev/null || mkdir -p ~/.openclaw/workspace/tasks/

# 验证依赖 skill 存在（按需）
ls ~/.openclaw/workspace/skills/[skill-name]/SKILL.md 2>/dev/null && echo "✅ [skill] 可用" || echo "⚠️ [skill] 未安装"
```

## wiki 关联

最终产出可选择性输出到 wiki：
- Wiki 路径：`~/llm-wiki/raw/articles/[目的地]综合攻略.md`（需用户确认）