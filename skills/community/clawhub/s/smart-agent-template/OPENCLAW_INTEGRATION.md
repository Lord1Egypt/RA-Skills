# OpenClaw 集成说明

## 自动检测机制

Smart Agent Bot 会自动检测是否安装了 OpenClaw：

- ✅ **已安装 OpenClaw** → 使用 `memory_search` 工具进行语义搜索
- ❌ **未安装 OpenClaw** → 使用本地文件 + AI 压缩方案

## 优势对比

| 特性 | OpenClaw 模式 | 本地模式 |
|------|--------------|---------|
| 语义搜索 | ✅ 支持 | ❌ 不支持 |
| 向量索引 | ✅ 自动 | ❌ 无 |
| 依赖 | 需要 OpenClaw | 无依赖 |
| 性能 | 更快、更准确 | 较慢 |

## 使用方式

### 方式1：安装 OpenClaw（推荐）

```bash
# 安装 OpenClaw
npm install -g openclaw

# 启动 Bot（自动检测）
cd integrations/telegram
python bot.py
```

**启动日志：**
```
✅ 检测到 OpenClaw，使用 memory_search 语义搜索
```

### 方式2：不安装 OpenClaw

```bash
# 直接启动 Bot
cd integrations/telegram
python bot.py
```

**启动日志：**
```
📁 未检测到 OpenClaw，使用本地文件 + AI 压缩方案
```

## 配置 OpenClaw Workspace（可选）

如果你的 OpenClaw workspace 不在默认位置，可以配置：

```python
# 在 bot.py 中
handlers = MessageHandlers(
    ai_adapter, 
    storage_dir="./data/memory",
    openclaw_workspace="/path/to/your/workspace"  # 指定 workspace
)
```

## 工作原理

### OpenClaw 模式

1. 用户发送消息："我上次说的那个项目进展如何？"
2. Bot 调用 `openclaw memory search "项目进展"`
3. OpenClaw 返回语义相关的记忆片段
4. Bot 结合片段 + 完整记忆生成回复

### 本地模式

1. 用户发送消息："我上次说的那个项目进展如何？"
2. Bot 加载完整记忆文件
3. AI 从记忆中提取相关信息
4. Bot 生成回复

## 性能对比

| 场景 | OpenClaw 模式 | 本地模式 |
|------|--------------|---------|
| 记忆量 < 1000 字符 | 差异不大 | 差异不大 |
| 记忆量 > 5000 字符 | 快速、准确 | 较慢、可能遗漏 |
| 多用户场景 | 高效 | 可能卡顿 |

## 检查当前模式

发送 `/status` 命令，查看 OpenClaw 状态：

```
✅ 系统状态

• Bot 状态: 运行中
• AI 引擎: 已连接
• 版本: v2.1.0
• OpenClaw: ✅ 已启用（语义搜索）  ← 这里显示当前模式

🧠 你的记忆状态：
...
```

## 常见问题

### Q: 如何切换模式？

A: 安装/卸载 OpenClaw 后重启 Bot 即可自动切换。

### Q: OpenClaw 模式需要额外配置吗？

A: 不需要，Bot 会自动调用 `openclaw memory search` 命令。

### Q: 两种模式的记忆数据互通吗？

A: 是的，记忆数据存储在 `./data/memory/` 目录，两种模式共享。

---

**版本：** v2.1.0
**更新日期：** 2026-03-29
