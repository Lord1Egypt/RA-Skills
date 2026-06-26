# Safe Bitwarden CLI (Agent Skill)

[English](./README.md)

一个工业级、安全且支持对话的 Bitwarden 保险库桥接工具。

## 核心理念：AI 密码盲视 (AI Password Blindness)
本 Skill 实现了 **原生剪切板代理 (Native Clipboard Proxy)** 模式。它允许 AI Agent 搜索您的保险库并触发拷贝操作，但**明文密码永远不会进入 AI 的上下文、日志或内存**。

### 工作原理：
1. **搜索**：Agent 仅获取非敏感元数据（项目名称、ID、用户名）。
2. **传输**：当您让 Agent “拷贝密码”时，它会执行一条直接的系统级管道指令：`bw get password $ID | pbcopy`。
3. **隔离**：秘密通过系统内核直接从 Bitwarden 流向您的系统剪切板，实现完全隔离。

## 审计级安全加固 (v1.5.1)
- **纯 Shell 实现**：使用 Bash 编写，规避了高级运行时（如 Node.js）子进程管理的漏洞风险。
- **零 Eval 调用**：所有原生工具均通过解析后的绝对路径直接调用，杜绝 Shell 注入风险。
- **零三方依赖**：仅使用系统自带工具（`bw`、`pbcopy`/`clip`、`python3`），无需额外安装包。

## 安装与设置

1. **必要条件**：
   - [Bitwarden CLI (`bw`)](https://github.com/bitwarden/clients/tree/master/apps/cli)
   - Python 3 (macOS/Linux 通常预装)

2. **环境变量**：
   您必须在本地导出 Session Token。本 Skill **不会**也**无法**询问您的主密码。
   ```bash
   export BW_SESSION=$(bw unlock --raw)
   ```

3. **验证环境**：
   ```bash
   bash scripts/main.sh setup
   ```

## 使用场景

- **Agent**: “我已经为您搜索了 Bitwarden 中关于 'Gmail' 的项目。发现一个用户名为 'user@gmail.com' 的账号。需要我把密码拷贝到剪切板吗？”
- **用户**: “好的。”
- **Agent**: (执行拷贝操作) “完成。密码已存入您的系统剪切板。”

## 注册表元数据 (ClawHub)
本 Skill 针对 ClawHub 等高信任注册表进行了优化，显式声明了所有必要的二进制文件和环境变量。
