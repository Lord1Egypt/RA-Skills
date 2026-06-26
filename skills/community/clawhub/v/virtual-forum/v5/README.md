# 虚拟论坛 Claude Code 并行辩论脚本

## v5.0: 使用外部CLI实现真正的多agent并行

此版本使用 `bash` + `claude --print` 调用外部Claude Code CLI，实现真正的多agent并行辩论。

## 架构对比

| 版本 | 机制 | 状态 |
|------|------|------|
| **v3.x** | Node.js模块 + 子类实现 | 废弃 |
| **v4.0** | OpenClaw sessions_spawn（主代理协调） | 配置驱动 |
| **v5.0** | bash + 外部CLI进程 | ✅ **推荐** |

## v5.0 核心优势

1. **真正的并行** - 5个Claude Code进程同时运行
2. **无架构限制** - 不依赖OpenClaw sessions
3. **可扩展** - 可同时启动任意数量agent
4. **独立运行** - 不受OpenClaw超时限制

## 使用方法

```bash
cd /tmp
./debate_parallel.sh
```

## 工作原理

```bash
# 1. 并行启动5个参与者
(echo "$USER_MSG" | claude --print --system-prompt "$TRUMP_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$NETANYAHU_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$PEZESHKIAN_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$VANCE_PROMPT") &
(echo "$USER_MSG" | claude --print --system-prompt "$PUTIN_PROMPT") &

# 2. 等待所有进程完成
wait

# 3. 主持人顺序总结
claude --print --system-prompt "$STARMER_PROMPT"
```

## 文件结构

```
v5/
├── debate_parallel.sh    # 主脚本
├── README.md           # 本文档
└── example_output.md   # 示例输出
```

## 依赖

- Claude Code CLI (`claude`)
- bash 4.0+
- 支持后台进程 (`&`, `wait`)

## 限制

- 需要安装 Claude Code CLI
- 每个进程消耗独立API配额
- 需要有效的API认证
