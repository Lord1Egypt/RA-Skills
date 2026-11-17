---
name: tradingbot
description: 从 GitHub 下载、更新、构建、启动并检查 paoosi/tradingbot。用户要求安装、运行、启动、升级或排查本地 TradingBot，或者希望先用模拟模式体验网格交易机器人时使用。
metadata:
  openclaw:
    requires:
      bins:
        - git
        - go
        - node
        - npm
        - openssl
        - cc
        - curl
    emoji: "🤖"
    homepage: https://github.com/paoosi/tradingbot
---

# TradingBot

在 macOS 或 Linux 用户机器上安装并运行 [paoosi/tradingbot](https://github.com/paoosi/tradingbot)。首次启动只验证本地管理界面和 Mock 模式，不配置真实交易。当前脚本不自动支持 Windows。

## 安全边界

- 执行下载、更新、依赖安装、构建或启动命令前，先向用户说明目标目录和将要执行的操作并取得确认。
- 不在对话、命令参数、日志或截图中索取或展示交易所 API Key、API Secret、JWT 密钥或 `APP_SECRET_KEY`。
- 首次启动时不创建交易所账户；应用的账户创建页面可能默认选择 `live`，后续体验必须由用户明确改选 `demo`。
- 任何真实交易、API 账户绑定或策略启动都不属于本 Skill 的默认流程，必须另行说明风险并取得用户明确确认。
- 不开放防火墙、不配置公网转发，仅向用户提供 `http://127.0.0.1:8088`。当前服务会监听所有网卡，启动前必须提醒用户保持系统防火墙开启，不要把端口映射到公网。
- 不使用 `git reset`、`git clean`、强制覆盖或删除用户已有目录。

## 安装流程

1. 检查操作系统、CPU 架构和 `git`、Go 1.21+、Node.js 18+、npm、OpenSSL、C 编译器。缺少依赖时只报告缺项；安装系统软件前再次取得确认。
2. 确定安装目录。用户未指定时，建议使用当前工作目录下的 `tradingbot`，不要静默写入其他位置。
3. 告知用户安装脚本会：
   - 从 `https://github.com/paoosi/tradingbot.git` 克隆代码，或对干净的同源仓库执行 fast-forward 更新；
   - 安装锁文件固定的前端依赖；
   - 构建前端、`server`、`worker-supervisor` 和 `strategy-runner`；
   - 在仓库内生成权限为 `0600` 的 `.env.local`，密钥只保存在用户本机。
4. 用户确认后运行：

   ```bash
   bash <当前 Skill 目录>/scripts/install.sh "<安装目录>"
   ```

5. 报告脚本输出的实际 commit，不把“命令无报错”表述成已经启动。

## 启动与验证

1. 在可持续运行的终端中执行：

   ```bash
   bash <当前 Skill 目录>/scripts/run.sh "<安装目录>"
   ```

2. 等待服务启动后检查：

   ```bash
   curl --fail --silent http://127.0.0.1:8088/api/health
   ```

   正常返回结构示例：

   ```json
   {"code":0,"message":"ok","data":{"ok":true}}
   ```

3. 告知用户访问 `http://127.0.0.1:8088`，并明确首轮不要添加 live 账户。
4. 最终报告安装目录、commit、监听端口、健康检查结果和停止方式。不得输出 `.env.local` 内容。

## 更新与异常处理

- 已有目录不是目标 Git 仓库、工作区有未提交改动或远端地址不匹配时停止，不自动修复。
- 端口占用时，只修改 `.env.local` 中的 `PORT`；编辑时不得回显其他密钥。
- 构建失败时，先报告失败阶段和原始错误，再检查对应版本。不要通过删除锁文件、数据库或用户源码来重试。
- 停止服务优先在运行终端发送 `Ctrl+C`，不要按端口批量杀进程。
