# skill-everyday

抓取 Clawhub 热门技能榜单，每次运行分析一个未处理过的技能，并写入 `data/reports/`。

## 依赖

- Node.js（ESM）
- Playwright 与 Chromium：在技能目录执行 `npm install`，再 `npx playwright install chromium`（或按 [Playwright 文档](https://playwright.dev/docs/intro) 安装浏览器）。

## 运行

```bash
cd /path/to/skill-everyday
npm install
npx playwright install chromium
node scripts/runner.mjs
```

首次运行会创建 `data/`、`data/reports/` 与 `data/analyzed.json`。

运行结束后会：

1. 写入 **`data/reports/YYYY-MM-DD-<slug>.md`**（按日归档）
2. 同时覆盖写入 **`data/reports/LATEST.md`**（固定路径，内容=最近一次运行；**若终端/聊天里看不到长文，请直接在 IDE 中打开此文件**）
3. 终端先打印几行摘要（排名、技能名、路径、`file://` 链接），再尝试输出全文（部分环境仍会截断）

## 说明

- Agent 行为与流程见根目录 `SKILL.md`。
- `data/` 为本地状态，发布到 Clawhub 时无需预置；由脚本自动生成。
