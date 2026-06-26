# Hook 配置指南

为 OpenClaw 配置自动自我改进触发器。

## 概述

Hook 通过在关键时刻注入提醒来启用主动学习捕获：
- **agent:bootstrap** - 在工作区文件注入之前
- **message:received** - 收到用户消息时
- **tool:after** - 工具执行之后

## OpenClaw 设置

### 1. 安装 Hook

复制 hook 到 OpenClaw 的 hooks 目录：

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-evolution-cn
```

启用 hook：

```bash
openclaw hooks enable self-evolution-cn
```

### 2. 验证 Hook

检查 hook 是否已注册：

```bash
openclaw hooks list
```

### 3. 测试 Hook

1. 启用 hook 配置
2. 重启 gateway
3. 启动新的 OpenClaw 会话
4. 发送任何提示
5. 验证你在上下文中看到 `<self-improvement-reminder>`

## 验证

### 测试激活器 Hook

1. 启用 hook 配置
2. 重启 gateway
3. 启动新的 OpenClaw 会话
4. 发送任何提示
5. 验证你在上下文中看到 `<self-improvement-reminder>`

### 测试错误检测器 Hook

1. 为 Bash 启用 PostToolUse hook
2. 运行失败的命令：`ls /nonexistent/path`
3. 验证你看到 `<error-detected>` 提醒

## 故障排除

### Hook 未触发

1. **检查脚本权限**：`chmod +x scripts/*.sh`
2. **验证路径**：使用绝对路径或相对于项目根目录的路径
3. **检查设置位置**：项目级 vs 用户级设置
4. **重启 gateway**：Hook 在 gateway 启动时加载

### 权限被拒绝

```bash
chmod +x ./skills/self-evolution-cn/scripts/activator.sh
chmod +x ./skills/self-evolution-cn/scripts/error-detector.sh
chmod +x ./skills/self-evolution-cn/scripts/extract-skill.sh
```

### 脚本未找到

如果使用相对路径，确保你在正确的目录中或使用绝对路径：

```json
{
  "command": "/absolute/path/to/skills/self-evolution-cn/scripts/activator.sh"
}
```

## Hook 输出预算

激活器设计为轻量级：
- **目标**：每次激活约 50-100 个 token
- **内容**：结构化提醒，不是冗长的指令
- **格式**：XML 标签以便于解析

如果需要进一步减少开销，可以编辑 `activator.sh` 以输出更少的文本。

## 安全考虑

- Hook 脚本以与 OpenClaw 相同的权限运行
- 脚本仅输出文本；它们不修改文件或运行命令
- 错误检测器读取环境变量
- 所有脚本都是可选的（你必须显式配置它们）

## 禁用 Hook

要在不删除配置的情况下临时禁用：

```bash
openclaw hooks disable self-evolution-cn
```

## OpenClaw Hook 事件

| 事件 | 何时触发 |
|------|---------|
| `agent:bootstrap` | 在工作区文件注入之前 |
| `message:received` | 收到用户消息时 |
| `tool:after` | 工具执行之后 |

## 自动识别触发器

### 用户纠正

检测到关键词："不对"、"错了"、"错误"、"不是这样"、"应该是"

### 命令失败

检测到工具执行失败（非零退出码）

### 知识缺口

检测到用户提供新信息

### 发现更好的方法

检测到"更好的方法"、"更简单"、"优化"等表达
