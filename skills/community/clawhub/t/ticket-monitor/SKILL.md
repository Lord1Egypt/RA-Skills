---
name: ticket-monitor
description: 实时监控大麦网已开售演出的余票与售罄状态，在放票、回流票、售罄等变化时通过终端/日志、Webhook（Server酱/企业微信/钉钉/通用）或 Windows 桌面弹窗告警。当用户要监控大麦演出余票、抢票提醒、售罄/回流提醒时使用。
---

# ticket-monitor

监控大麦网某场已开售演出的余票可用状态，轮询发现变化即告警。Node.js 实现，零第三方依赖（仅用内置 `fetch`/`crypto`）。

## 快速开始

1. 复制配置模板并填写 itemId：
   ```powershell
   Copy-Item config.example.json config.json
   ```
2. 在大麦详情页拿到 itemId（URL 里的 `id=` 参数，例如
   `https://detail.damai.cn/item.htm?id=7123456789` 中的 `7123456789`），
   填入 `config.json` 的 `itemId`（或直接填 `url`）。
3. 试跑一次（抓取一次并打印解析后的快照）：
   ```powershell
   node .claude/skills/ticket-monitor/monitor.mjs --once
   ```
4. 持续监控：
   ```powershell
   node .claude/skills/ticket-monitor/monitor.mjs
   ```

## 命令参数

- `--config <path>` 指定配置文件（默认同目录 `config.json`）
- `--item-id <id>` / `--url <url>` 直接指定演出，覆盖配置文件
- `--interval <秒>` 轮询间隔，覆盖配置
- `--once` 抓取一次并打印解析后的快照后退出（调试用）
- `--raw` 抓取一次并打印接口**原始返回 JSON**后退出（用于确认字段结构）

## 配置说明

见 `config.example.json`。要点：

- `interval`：轮询秒数，建议 30–60 秒。过短会触发风控、被封。
- `notify.log` / `notify.logFile`：写本地日志。
- `notify.toast`：Windows 托盘气泡弹窗。
- `notify.webhooks`：数组，支持 `serverchan`（Server酱）、`wecom`（企业微信机器人）、`dingtalk`（钉钉机器人）、`generic`（自定义 URL）。
- `damai.cookie`：**可选**，填入浏览器登录后的 Cookie 字符串，用于携带真实会话以绕过反爬（见下文）。

## 能力与限制（务必了解）

- 接口为 `mtop.alibaba.damai.detail.getdetail/1.2`（appKey `12574478`），签名/令牌流程已实测可用。
- 大麦公开详情接口只暴露「可售(salable)/售罄」状态，**精确剩余张数通常不对外公开**；
  本工具会尽力提取任何数字型余票字段（如 `residueNum`/`ticketNum`），缺失时按「有票/售罄」监控。
- 监控的是**状态变化**：放票（售罄→有票）、回流票、售罄、场次/档位变化，变化即告警。
- **反爬**：大麦对数据中心 IP / 高频请求会返回「对不起，小二很忙」或重定向到 `punish` 挑战页。
  如遇此提示，请：① 在本机（家庭/公司网络）运行；② 用浏览器登录大麦后，把该域名下的 Cookie 复制到
  `damai.cookie`；③ 适当增大 `interval`。
- 仅做**只读监控**，不代抢、不下单、不绕过验证码。请遵守平台规则，控制轮询频率。
