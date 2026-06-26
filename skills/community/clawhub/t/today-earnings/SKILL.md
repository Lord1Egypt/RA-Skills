---
name: today-earnings
description: 从 Yahoo Finance 获取财报日历数据。适用于查询指定日期或当天财报、输出公司列表、按财报发布时间区分 BMO/AMC/TNS。当前实现基于 Chrome Extension + Native Messaging，需要本地安装 Chrome 扩展、Native Host、Google Chrome 与 Node.js。支持 macOS、Linux（含 Ubuntu）和 Windows。
---

# Today Earnings

通过 Chrome Extension + Native Messaging 打开 Yahoo Finance 财报日历页面，并返回结构化 JSON。

## 快速流程

1. 先安装并加载 `chrome-extension/`，拿到扩展 ID。
2. 运行 `bash native-host/install.sh <扩展ID>` 安装 Native Host。
3. 在 `chrome://extensions` 刷新扩展。
4. 用 `./scripts/get-company-list.sh [日期]` 获取结果。

## 常用命令

```bash
# 今天
./scripts/get-company-list.sh

# 指定日期
./scripts/get-company-list.sh 2026-03-14
```

## 资源导航

- 读取 `references/usage_guide.md`：当你需要完整安装步骤、运行方式、输出格式、报错排查时。
- 读取 `references/yahoo_earnings_calendar.md`：当你需要查看 Yahoo 页面结构、字段映射、DOM 假设和解析维护点时。
- 读取 `design.md`：当你需要理解扩展、Native Host、Node CLI 之间的整体架构时。

## 组件职责

- `scripts/get-company-list.sh`：命令入口，负责参数透传与 Node CLI 调用。
- `scripts/get-company-list.mjs`：负责 socket 通信、参数校验、JSON 输出（含市值数字化转换）。
- `chrome-extension/`：负责打开页面、等待内容加载、注入解析逻辑。
- `native-host/`：负责 Chrome Native Messaging 与本地 socket 桥接。

## 使用提醒

- 当前实现依赖本地 GUI 环境，不能在纯无头环境中直接完成完整流程。
- **若 Chrome 尚未启动**，请先通过命令行打开浏览器，再运行脚本：
  ```bash
  # macOS
  open -a "Google Chrome"
  # Linux
  google-chrome &
  # Windows (PowerShell)
  Start-Process "chrome"
  ```
- 运行前必须确保 Chrome 已启动，扩展已加载，Native Host 已安装。
- 当前能力以单日期查询为主；如页面结构变化，优先检查 `references/yahoo_earnings_calendar.md` 中的解析假设。
- Linux 用户注意：Ubuntu snap 版 Chromium 不支持 Native Messaging，建议使用 deb 版 Google Chrome。
- Windows 用户需在 `install.sh` 生成文件后，额外运行 `native-host/install-windows.bat` 完成注册表注册。详见 `references/usage_guide.md`。
