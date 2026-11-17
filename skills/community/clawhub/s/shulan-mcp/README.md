# ShuLan MCP Server

数懒（ShuLan）MCP Server — 把数懒 AI 数据中台 REST API 包装为 Model Context Protocol 工具，供 Claude Code / Cursor / ChatGPT Actions 等 AI 客户端调用。

ShuLan MCP Server wraps the ShuLan AI data platform REST API as MCP tools for Claude Code, Cursor, ChatGPT Actions and other AI clients.

## 能力 / Capabilities

- `shulan_health` — 服务状态检查 / service health check
- `shulan_create_task` — 创建数据调研任务（行业数据、达人清单、招标汇总、企业洞察、招聘信号、舆情趋势）/ create data research tasks
- `shulan_get_task` — 查询任务状态与报告 / query task status & report
- `shulan_market` — 查询报告市集 / browse the report marketplace
- `shulan_get_report` — 获取报告详情 / fetch report details

## 安装 / Install

```bash
npm install
SHULAN_API_KEY=sl_your_key SHULAN_BASE_URL=https://shulan.io npm start
```

或全局安装：`npm install -g shulan-mcp`（npm 包已发布：https://www.npmjs.com/package/shulan-mcp）

完整接入文档见 [docs/mcp.md](docs/mcp.md)，Agent 技能见 [SKILL.md](SKILL.md)。

## 官网 / Website

https://shulan.io — 在「开放平台」生成 `sl_` 前缀 API Key（按实际用量结算，多退少不补）。

## License

MIT
