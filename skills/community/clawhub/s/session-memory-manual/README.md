# session-memory-manual 🔄

跨 Session 记忆查找与同步机制（完全手动触发）

## 功能

当你需要查找其他 session 中的记忆、决策或待办事项时，这个技能帮你高效检索和同步。

**⚠️ 重要：完全手动触发**
- 只有用户明确要求时才执行检索
- 不会自动检测暗示或假设
- 所有操作透明可追溯

## 使用场景

只有用户明确说以下话语时，我才会执行检索：

- ✅ "帮我查一下昨天的事"
- ✅ "搜索一下其他 session"
- ✅ "找找看蒙老师的报告时间"
- ✅ "检查下其他平台的记录"
- ✅ "同步一下记忆"

**我不会：**
- ❌ 自动检测用户话语中的暗示
- ❌ 静默执行检索
- ❌ 在用户没要求前搜索其他 session

## 安装

```bash
# 如果已经通过 npm 安装 OpenClaw，技能会自动可用
# 或者从 clawhub 安装
openclaw skill install session-memory-manual
```

## 工作原理

1. **用户明确触发** - 只有用户明确要求时才启动
2. **快速扫描** - 列出活跃 session，查看最近消息
3. **记忆文件优先** - 先查 `memory/YYYY-MM-DD.md` 和 `MEMORY.md`
4. **深度检索** - 必要时读取特定 session 的完整历史
5. **智能同步** - 将发现的重要信息写入共享 memory 文件（用户确认后）

## 示例

**用户：** "帮我查一下微信 session 里有没有蒙老师的报告提醒"

**技能执行：**
```
1. 列出活跃 session：sessions_list(activeMinutes=1440)
2. 搜索 memory 文件：grep -r "蒙老师" memory/
3. 读取相关 session 历史
4. 向用户展示发现
5. 用户确认后写入 memory/2026-03-27.md
```

## 安全设计

- ✅ 无自动检测 - 不会自动分析用户话语
- ✅ 用户明确触发 - 只有用户明确要求时才执行检索
- ✅ 透明操作 - 所有文件读写都会向用户报告
- ✅ 隐私保护 - 敏感信息不写入共享 memory
- ✅ 最小权限 - 仅执行用户明确请求的操作

## 技术细节

- 使用 `sessions_list` 获取 session 元数据
- 使用 `sessions_history` 读取完整对话
- 使用 `grep/find` 搜索 memory 文件
- 使用 `write/edit` 同步发现的信息

## 许可证

MIT - 自由使用、修改、分发

---

Created by 郭泉 (Dr. Guo) 🎯
Available on [ClawHub](https://clawhub.ai)
