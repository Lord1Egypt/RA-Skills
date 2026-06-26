---
name: shell-safe-exec
description: Run non-destructive repo-local commands with explicit safety rules. Use when the user asks to build, test, lint, format, inspect status, or install project dependencies in the current workspace, and the task can be completed without risky system operations. Do not use for long-running services, background process management, or generic command execution frameworks. Chinese triggers: 执行命令、运行测试、构建项目、安装依赖、跑 lint、跑 format，但要求安全执行.
---

# 安全执行

只执行与项目相关、且明确安全的命令。

## 允许执行

- build、test、lint、format、type-check、health-check
- 使用项目默认包管理器安装依赖
- 验证改动所需的状态和检查命令

## 禁止执行

- 递归删除或其他大范围破坏性文件操作
- 磁盘、分区、内核、服务或系统配置修改
- 提权操作
- 网络扫描、远程执行、端口转发
- 读取与项目无关的系统敏感信息

## 工作流

1. 优先使用仓库已经定义好的命令，不临时拼复杂管道。
2. 把用户提供的路径和参数当作不可信输入，按字面值传递，避免命令注入。
3. 只运行完成当前验证所需的最小命令。
4. 一旦失败立即停止，直接返回真实错误，不做危险重试。
5. 所有命令都限定在项目工作区内。

## 输出

- 执行了什么命令
- 成功或失败
- 如果失败，返回关键错误信息
