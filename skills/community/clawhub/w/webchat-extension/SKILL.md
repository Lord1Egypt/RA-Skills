---
name: webchat-extension
description: 部署「网页划线对话」浏览器扩展（Chrome MV3 / 兼容 Chrome·Edge·千问·夸克 等 Chromium 内核浏览器）。在任意网页选中文字，点工具栏图标唤起可拖动对话浮层，带着网页上下文用 CodeBuddy AI 流式问答。包含本地 Express + SSE 后端（CodeBuddy Agent SDK）与前端扩展。当用户要「做一个网页划词对话插件 / 给浏览器装个网页对话工具 / 选中文字问 AI / 部署小虾网页对话扩展 / web highlight chat extension / 把网页内容丢给 AI 聊」时使用本技能。
---

# 网页划线对话 · 小虾 🦐

一个浏览器扩展 + 本地 AI 后端：用户在任意网页**选中文字**或**复制文字**，点工具栏图标弹出对话浮层，带着网页上下文直接和 AI 流式对话。后端基于 **CodeBuddy Agent SDK**（官方 `@tencent-ai/codebuddy-code` CLI 做 transport）。

## 什么时候用
- 用户想要「在网页上选中一段文字，直接问 AI 这是什么 / 帮我总结 / 翻译 / 解释」。
- 用户想把某个网页内容作为上下文和 AI 聊。
- 用户要部署/打包一个浏览器划词对话工具。

## 架构
```
浏览器扩展 (Chrome MV3)                本地后端 (Express + SSE)
┌──────────────────────────┐          ┌────────────────────────────┐
│ 点工具栏图标 → 浮层(iframe) │──fetch──▶│  /api/chat  (SSE 流式)      │
│ content.js 注入网页          │          │  query() → codebuddy CLI    │
│ background.js service worker│          │  (CodeBuddy Agent SDK)      │
│ 选区经 executeScript 跨 iframe│         │  buildSystemPrompt 注入网页上下文│
└──────────────────────────┘          └────────────────────────────┘
```
- 前端只请求 `http://localhost:3000`，**API Key 只在后端**。
- 面板状态（开关/位置/上下文/对话）用 `chrome.storage` 持久化，刷新不丢。

## 文件布局（本 skill 内）
```
webchat-extension/
├── SKILL.md
├── pack.mjs                  # 发布工具：在 deploy 产物(双形态目录)下 node pack.mjs → 生成干净分享包 zip
├── gen-icons.mjs             # 独立图标生成（零依赖）：node gen-icons.mjs [dir]
├── scripts/
│   ├── deploy.mjs            # 脚手架：复制 assets 源码 + npm install + 生成 icons/（Windows 部署时生成 launcher.vbs + 注册协议）
│   ├── gen-vbs.mjs           # 唯一 source of truth：写出 backend/launcher.vbs（agent 部署时调用，不随包分发）
│   └── register-protocol.cjs # 一键注册/修复 webchat:// 协议（协议丢失或被识别成 Store 应用时用）
├── assets/
│   ├── extension/            # 浏览器扩展（manifest/background/content/panel.*/icons）
│   ├── backend/              # server.js / launcher.mjs / patch-sdk.mjs / package.json / .env.example（launcher.vbs 由 agent 在部署时用 scripts/gen-vbs.mjs 生成，不随包分发）
│   └── root/                 # 部署到目标根目录的文档：README.md（.gitignore / 协议模板不随包分发）
└── references/deploy-guide.md  # 详细排错表
```

> **统一原则**：本 skill 是**唯一 source of truth**。运行环境一律由 `deploy.mjs` 生成（assets → 目标目录），不要在别处手维护一份带 `extension/ backend/` 的"双形态"目录，以免与 skill 不同步产生歧义。deploy 产物（目标目录）本身就是双形态目录（含 `extension/ backend/ SKILL.md pack.mjs gen-icons.mjs`），可直接加载运行，也可 `node pack.mjs` 生成分享包。

## 部署步骤（agent 照做）
1. **脚手架**：运行 `node <skill_dir>/scripts/deploy.mjs <targetDir>`（不加 `[targetDir]` 默认 `./webchat-extension` 或 `~/webchat-extension`）。脚本把 `assets/` 里的扩展、后端、根文档复制到目标目录并 `npm install`；**在 Windows 上，agent 会自动用 `scripts/gen-vbs.mjs` 生成 `backend/launcher.vbs`（即使带 `--no-protocol` 也会生成），并自动注册 `webchat://start` 协议**，使面板「🚀 启动后端」按钮免终端生效。`launcher.vbs` 是部署期产物，**绝不随分享包分发/上传**——若目标目录缺失它，可随时补：`node <skill_dir>/scripts/gen-vbs.mjs <target>/backend`。加 `--no-install` 只复制不装依赖；加 `--no-protocol` 跳过协议注册（但 vbs 仍会生成）。非 Windows 或需手动注册时，按 README「四、一键启动后端」用面板「📋 复制启动命令」手动 `npm start`，或参考 README/references 手动 `reg add` 注册协议。
2. **配置后端**：在 `<target>/backend/` 复制 `.env.example` 为 `.env`，按需填 `CODEBUDDY_API_KEY`（**不填也能跑：复用本机 `codebuddy` CLI 已登录凭据走登录模式真实 AI**；只有显式设 `WEBCHAT_DEMO=1` 才进演示模式）。确认 `CODEBUDDY_MODEL=deepseek-v4-flash`（默认，该账户不支持 `claude-sonnet-4`）。
3. **启动后端（后台运行）**：`cd <target>/backend && npm start`。监听 `http://localhost:3000`。改代码后重启才生效。也可用面板「🚀 启动后端」按钮（需协议已注册）。
4. **加载扩展**：浏览器（Chrome / Edge / 千问 / 夸克 等 Chromium 内核）进入**开发者模式 → 加载已解压的扩展程序**，目录选 `<target>/extension/`。（`deploy` 已自动生成 `extension/icons` 四张图标；若手动加载项目根 `extension/`，请先跑 `node gen-icons.mjs`）改了扩展代码要回扩展管理页点「重新加载」。
5. **验证**：访问 `http://localhost:3000/api/health` 应返回 `{"status":"ok",...}`；打开任意网页 → 点工具栏「🦐 小虾」图标 → 弹出面板 → 选中网页文字点「➕ 添加选中文本」→ 提问 → 流式回答。

## 发布分享包（可选，给其他人用）
deploy 产物（目标目录）即为双形态目录，内含 `pack.mjs`。在其中运行：
```bash
cd <target>            # 例如 ~/webchat-extension
node pack.mjs         # 在父目录生成 webchat-extension-share-YYYYMMDD.zip
```
`pack.mjs` 自动按 `.gitignore` + 硬性黑名单排除：`node_modules/`、`.env`、私钥 `*.pem`、`extension.crx`、协议注册表模板、所有 `*.png`（图标由收件人部署时生成）。生成的 zip 即干净分享包，可直接发给他人或推送到仓库。

## CodeBuddy 认证（登录 / API Key 二选一，零配置优先）
后端 `server.js` 通过 CodeBuddy Agent SDK 调真实模型，认证方式参考 dingtalk-auto-reply 的「Key / CLI 已登录」范式：
- **登录模式（默认，零配置）**：未配置 `CODEBUDDY_API_KEY` 时，SDK 自动复用本机 `codebuddy` CLI 已登录凭据（与你在终端 / WorkBuddy 登录的是同一套 `~/.codebuddy/local_storage`），无需任何 Key 即可走真实 AI。首次启动前请确保 `codebuddy` 已登录（终端跑一次 `codebuddy` 完成登录）。
- **Key 模式（推荐无人值守）**：在 `backend/.env` 填 `CODEBUDDY_API_KEY=<你的key>`（申请：https://copilot.tencent.com 控制台）→ 用 Key 直连，不依赖交互登录。
- **演示模式**：仅当显式设 `WEBCHAT_DEMO=1` 时强制进入（返回模拟回复验收交互）；否则无 Key 也走「登录模式」真实模型，**不再降级为 demo**。
- `CODEBUDDY_INTERNET_ENVIRONMENT`：中国版自动设为 `internal`（已在 server.js 兜底），无需手动配。
- 自检：`/api/health` 返回 `mode`（key｜login）、`demo`；`/api/auth` 用一次极短 query 实测登录态（15s 超时兜底，不卡死），失败回退到凭据目录存在性判断并给出明确修复提示。**后端绝不代填 / 存储登录凭据**——认证动作由你本人在终端完成。

> ⚠️ **进程清理绝不误杀**：后端退出（`/api/stop`、空闲超时、托管心跳断、全局退出）时只清理「自己 spawn 出来的 codebuddy CLI 子进程」——按**进程树（本进程后代）+ CLI 路径精确匹配**，绝不按端口 `netstat` 乱扫（端口子串匹配会把 `45012` 误中 `450123`，且易误杀带看门狗、会被自动重拉的进程，如 dingtalk 监控）。即使某进程有看门狗会自愈，我们也连误杀都不做；另有「监听端口 + CLI 路径二次确认」兜底，确保外来进程永不被误杀。

## 关键坑（务必先读，否则部署必踩）
- **端口冲突导致一直转圈**：官方 CLI 启动会起 prewarm 本地 server，端口由 `SERVER__PORT` 控制。若该端口被本机其他程序（**WorkBuddy 桌面应用**）占用，CLI 会 `EADDRINUSE` 卡死。解决：`.env` 设 `SERVER__PORT=40123`（空闲端口）并重启。**面板「🚀 启动后端」按钮路径**下，`launcher.mjs` 会自动从 `.env` 读取 `SERVER__PORT` 并**显式注入**子进程环境，覆盖本机可能存在的系统级 `SERVER__PORT`（dotenv 不覆盖已存在变量，故必须靠 launcher 注入）；未设置时则不注入、由 `server.js` 自动分配空闲端口。若走 `npm start` 手动启动且系统变量残留旧值，用 `SERVER__PORT=40123 npm start` 显式覆盖。
- **模型名 400**：本账户不支持 `claude-sonnet-4`。用 `deepseek-v4-flash`（默认）、`hy3` 或 `auto`。
- **CLI 路径**：`server.js` 通过 `resolveCli()` 自动定位官方 CLI（优先级：显式 `CODEBUDDY_CLI_PATH` → PATH 上的 `codebuddy` → 受管 node 目录固定路径）。不要用 WorkBuddy 自带的那份 cli（协议不匹配会 initialize 超时）。
- **演示 vs 真实**：未填 `CODEBUDDY_API_KEY` 时后端走「登录模式」复用 codebuddy CLI 已登录凭据，是**真实 AI**（不是模拟回复）；只有显式设 `WEBCHAT_DEMO=1` 才进演示模式（模拟回复用来验收交互闭环）。填了 Key 则走 Key 模式，也是真实 AI。
- **扩展不注入系统页**：`chrome://`、`edge://` 等页面扩展无法注入，点图标无反应属正常。
- **图标由 agent 部署时生成（分享包不含任何 *.png）**：`manifest.json` 声明了 `icons/icon{16,32,48,128}.png`，加载扩展前这 4 张必须存在，否则报 `Could not load icon` 加载失败。`deploy.mjs` 复制 extension 后会**自动生成**珊瑚橙 PNG（不依赖源图标）；手动从项目根加载（不跑 deploy）时，请先跑 `node gen-icons.mjs` 生成。想换正式品牌图标，部署后替换这 4 张 png 即可。
- **launcher.vbs 由 agent 部署时生成（绝不随包分发/上传）**：`backend/launcher.vbs` 是 Windows 隐藏启动器，用于「🚀 启动后端」按钮免终端拉起 `launcher.mjs`。它**不进分享包、不进 git**（被 `pack.mjs` 与 `.gitignore` 排除），由 agent 在部署时经 `scripts/gen-vbs.mjs` 现生成。若某次部署后按钮失效 / 报「找不到 launcher.vbs」，直接重跑 `node scripts/gen-vbs.mjs <target>/backend`（或重新 `deploy.mjs`）即可，无需手动编辑 vbs 内容。
- **微信读书等 iframe 阅读器**：选区由 `background.js` 用 `chrome.scripting.executeScript({allFrames:true})` 直插每一帧读取，能抓到；若阅读器是 sandboxed iframe（无 allow-scripts）且屏蔽 copy，则只能手动粘贴/输入到输入框再发送（发送会自动收进上下文）。
- **webchat:// 协议被识别成 Microsoft Store 应用（弹"获取打开此链接的应用"）**：这是 `HKCU\Software\Classes\webchat` 注册表项丢失/损坏导致，Windows 找不到处理程序就去 Store 找 UWP 应用了。修复：运行 `node scripts/register-protocol.cjs`（自动探测 `launcher.vbs` 位置并重新注册协议，支持 `--check` 仅检查、`--force` 强制重写）。注册指向的 `launcher.vbs` 由 agent 在部署时用 `scripts/gen-vbs.mjs` 在目标目录生成，若你迁移过项目目录，用 `WEBCHAT_DIR=新目录 node scripts/register-protocol.cjs --force` 重新指向（缺失则先 `node scripts/gen-vbs.mjs <新目录>/backend` 生成）。

## 使用方式（交付给用户）
- 任意网页 → 点工具栏「🦐 小虾」图标 → 右侧弹出对话面板（高约视口 2/3，可拖动，双击标题栏复位，位置自动记住）。
- 喂上下文：选网页文字点「➕ 添加选中文本」（同时读选区 + 系统剪切板，含输入法复制）；或直接发送（自动收剪贴板/提问文本）。
- 上下文只显示 10~20 字摘要 + …，不可编辑；多段累加，✕ 删除。
- 输入框回车发送，AI 逐字流式回答，多轮保持上下文。

## 验证清单
- [ ] `http://localhost:3000/api/health` 返回 ok
- [ ] 扩展已加载、未被禁用
- [ ] 点图标弹出面板、可拖动不抖、不跳左上角
- [ ] 选中文字 → 添加上下文 → 提问有流式回答
- [ ] 刷新网页后面板自动重开、上下文/对话不丢
- [ ] 真实 AI 模式（登录模式默认零配置 / 或填 Key）回答正常；`WEBCHAT_DEMO=1` 演示模式也能跑通闭环

## 参考
- 详细排错表见 `references/deploy-guide.md`。
- 来源项目：本地 `webchat-extension/`（本 skill 由其封装，扩展版本 1.5.5；路径随各人工作区不同，无硬编码）。
