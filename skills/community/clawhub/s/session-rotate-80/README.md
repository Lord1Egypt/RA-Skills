# Session Rotate 80

不依赖记忆系统的 OpenClaw 会话轮换技能。

当上下文占用率达到 80% 时，自动输出新会话触发指令，避免长对话把上下文顶满。

## 特性

- ✅ 默认 OpenClaw 可用（无 Mem0、无文件记忆也能工作）
- ✅ 上下文占用率阈值触发（默认 80%）
- ✅ 标准化新会话触发消息（`[NEW_SESSION] ...`）
- ✅ 提供最小交接提示，减少会话切换后的信息断层

## 适用场景

- 你只想要“到 80% 就切新会话”的硬规则
- 你不准备搭建完整记忆系统
- 你在 Discord 长时间连续对话，想避免上下文溢出降质

## 快速开始

### 安装

```bash
clawhub install session-rotate-80
```

或手动：

```bash
git clone https://github.com/0range-x/session-rotate-80.git
```

### 运行

```bash
python scripts/context_guard.py <used_tokens> <max_tokens> --threshold 0.8 --channel boss
```

示例：

```bash
python scripts/context_guard.py 220000 272000 --threshold 0.8 --channel boss
```

## 输出说明

### 触发时

- `[ROTATE_NEEDED]`
- `[NEW_SESSION] 上下文达到80%（used/max），自动切换新会话`
- `[HANDOFF_HINT] 在旧会话保留3行交接：当前目标、已完成、下一步`

### 未触发时

- `[ROTATE_NOT_NEEDED] ratio=x.xx < 0.800`

## 接入建议（Heartbeat）

在你的心跳或状态检查流程里：

1. 读取当前上下文占用（used/max）
2. 调用 `context_guard.py`
3. 命中后直接发送 `[NEW_SESSION] ...`
4. 旧会话只做交接，不再承载新任务

## 与记忆系统关系

- 本技能可以独立工作
- 即使无记忆系统，也能稳定执行“80%自动切换”
- 若后续接入记忆系统，可在触发前加“自动交接摘要写入”获得更好连续性

## 实用指南

推荐搭配规则：

1. 阈值固定 80%
2. 切换后第一条消息粘贴交接三行
3. 单会话尽量只做一个主题
4. 2到3天主动切一次会话，即使没到 80%

## 作者

小橘（vulcanx_14970）

Twitter: [@maru_49940](https://x.com/maru_49940)

## 许可证

MIT
