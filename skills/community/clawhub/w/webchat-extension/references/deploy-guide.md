# 网页划线对话 · 部署与排错指南

本文件是 skill 的详细排错表，配合 `SKILL.md` 使用。扩展版本 1.5.5。

## 〇、前置依赖：codebuddy CLI（外部依赖，不随包分发）

后端通过 `@tencent-ai/agent-sdk` 在运行时 `spawn` 一个 `codebuddy` 子进程来真正调用 AI。`server.js` 的 `resolveCli()` 按序找它：① `CODEBUDDY_CLI_PATH` 显式指定 → ② 系统 `PATH` 上的 `codebuddy` → ③ 兜底 `~/.workbuddy/binaries/node/versions/22.22.2/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy`（仅本机 WorkBuddy 托管环境有）。

- **本机**（装了 WorkBuddy）：托管 Node 已自带 `codebuddy`，开箱可用。
- **分享给别人的机器若没有 WorkBuddy**：需对方 `npm i -g @tencent-ai/codebuddy-code` 并确保 `codebuddy` 在 `PATH`，或在 `.env` 设 `CODEBUDDY_CLI_PATH` 指向 CLI。否则 `query()` 拉不起进程 → 后端连不上（登录/Key 模式都依赖该 CLI）；仅 `WEBCHAT_DEMO=1` 演示模式可跑通交互闭环。

> 注意：`backend/` 目录**必须随扩展一起分享**——扩展只是 UI 外壳，AI 能力全在后端。

## 一、后端启动与模式

| 步骤 | 命令 | 说明 |
|---|---|---|
| 进入后端 | `cd <target>/backend` | — |
| 安装依赖 | `npm install` | 仅首次；用受管 node 即可 |
| 复制配置 | `cp .env.example .env` | 按需填 `CODEBUDDY_API_KEY` |
| 启动 | `npm start` | 默认 `http://localhost:3000` |
| 健康检查 | `curl http://localhost:3000/api/health` | 返回 `{"status":"ok",...}` |

**三种模式**
- 登录模式（默认，零配置）：未填 `CODEBUDDY_API_KEY` 且未设 `WEBCHAT_DEMO`，复用本机 `codebuddy` CLI 已登录凭据走**真实 AI**（首次需终端跑一次 `codebuddy` 登录）。
- Key 模式（推荐无人值守）：填了 `CODEBUDDY_API_KEY`，用 Key 直连 CodeBuddy AI，不依赖交互登录。
- 演示模式：显式设 `WEBCHAT_DEMO=1`，后端返回模拟流式回复，验收交互闭环用，无需账号/登录。

---

## 二、现象 → 排查

| 现象 | 原因 / 排查 |
|---|---|
| 面板提示「连接后端失败」 | 确认 `cd backend && npm start` 已启动；端口 3000 |
| 点「🚀 启动后端」没反应 | 多半是 `webchat://` 协议未注册（见第四节）。可改用面板「📋 复制启动命令」手动 `npm start` |
| 点图标没反应 | 多见于 `chrome://`、`edge://` 等系统页（扩展无法注入）；普通网页正常。确认扩展已加载且未被禁用 |
| 选中文字点「添加选中文本」没反应 | 选区由 `chrome.scripting.executeScript(allFrames)` 读取，正常能抓微信读书/千问 iframe。若阅读器是 **sandboxed iframe（无 allow-scripts）** 或屏蔽 copy，则只能手动粘贴/输入到输入框发送（发送自动收上下文）。属平台限制非 bug |
| 收到的是演示（模拟）回复 | 说明设了 `WEBCHAT_DEMO=1`。删掉它重启即走登录模式真实 AI；登录态失效则终端跑一次 `codebuddy` 重登，或 `.env` 填 `CODEBUDDY_API_KEY` 走 Key 模式 |
| `/api/health` 返回 `demo:true` | 说明设了 `WEBCHAT_DEMO=1`（演示模式）；移除该变量走默认登录模式真实 AI，或填 Key |
| **真实模式一直转圈、面板无回答**（后端日志 `EADDRINUSE` / CLI 卡死） | 官方 CLI 的 prewarm 端口与 WorkBuddy 桌面应用撞车。在 `.env` 设 `SERVER__PORT=40123`（或空闲端口）并重启；若环境变量残留旧 `SERVER__PORT`，启动时用 `SERVER__PORT=40123 npm start` 显式覆盖 |
| 后端报 `400 model [...] service info not found` | 模型名不对，把 `CODEBUDDY_MODEL` 改成 `deepseek-v4-flash`、`hy3` 或 `auto`（本账户不支持 `claude-sonnet-4`） |
| 后端报 `initialize` 超时 / 永远 0 字节 | 用了 WorkBuddy 自带那份 cli（协议不匹配）。必须用官方 `@tencent-ai/codebuddy-code`；`server.js` 的 `resolveCli()` 已自动定位，必要时用 `CODEBUDDY_CLI_PATH` 显式指定 |
| 拖拽抖动 / 跳左上角 | 扩展 V1.5.2 已修复拖拽坐标公式；若仍异常，扩展管理页「重新加载」并确认 manifest 版本 ≥ 1.5.2 |
| **Windows 上每次对话 / 启动后端弹黑框** | SDK 内部 spawn CLI 默认 `windowsHide:false`。`package.json` 的 `postinstall` 会自动跑 `patch-sdk.mjs` 给 `@tencent-ai/agent-sdk` 的 `process-transport.js` 两处 spawn 注入 `windowsHide:true`；`npm install` 后即生效。若依赖是手动装、跳过了 postinstall，运行一次 `node backend/patch-sdk.mjs` 即可 |

---

## 三、端口冲突根因说明

官方 `@tencent-ai/codebuddy-code` 启动时会起一个 prewarm 本地 server，端口由 `SERVER__PORT` 环境变量控制。本机 **WorkBuddy 桌面应用自身也会起同类 server 占端口**（实测占 54975 之类），两者撞车 → CLI 一绑定就 `EADDRINUSE` → SDK `query()` 永远 0 字节超时。

- `server.js` 启动时会自动分配空闲端口注入 `SERVER__PORT`（兜底）。
- 若自动分配仍冲突（极少见），在 `.env` 显式 `SERVER__PORT=40123` 并重启。
- dotenv **不会覆盖已存在的环境变量**，所以如果当前 shell 里残留 `SERVER__PORT=旧值`，必须用 `SERVER__PORT=40123 npm start` 显式传，或在新 shell 里启动。

---

## 四、一键启动（webchat:// 协议注册）

面板「🚀 启动后端」按钮（以及离线横幅里的启动按钮）靠自定义协议 `webchat://start` 免终端拉起后端。这要求 **Windows 已注册协议处理器**（让系统知道遇到 `webchat://` 就调用 `launcher.vbs`）。

- **由 agent 按 skill 部署**：`node scripts/deploy.mjs` 在 Windows 上自动写入注册表（HKCU，无需管理员），开箱即用。非 Windows 或加了 `--no-protocol` 时跳过。
- **手动 / 分享给别人**：二选一
  1. 把 `webchat-protocol.reg.example` 里的 `__BACKEND_DIR__` 替换为真实 `backend` 绝对路径（反斜杠写成 `\\`），存为 `webchat-protocol.reg` 双击导入；
  2. 或命令行：`reg add "HKCU\Software\Classes\webchat\shell\open\command" /ve /t REG_SZ /d "\"C:\Windows\System32\wscript.exe\" \"<backend路径>\launcher.vbs\" \"%1\"" /f`（并建好 `webchat` 主键与 `URL Protocol` 值，详见 .reg.example 头部注释）。
- **注册内容**：`HKCU\Software\Classes\webchat`（`URL Protocol=""`）+ `shell\open\command` → `"C:\Windows\System32\wscript.exe" "<backend>\launcher.vbs" "%1"`。
- **未注册时**：按钮点了没反应，但可用面板「📋 复制启动命令」手动 `npm start`，功能不受影响。

---

## 五、后端生命周期（心跳托管）

后端由 `webchat://start` 协议（面板按钮）经 `launcher.vbs → launcher.mjs` 拉起。`launcher.mjs` 探测端口，未占用则以**托管模式**（`WEBCHAT_MANAGED=1`）用 `spawn(detached)` 拉起 `server.js`，随后自身退出——**后端作为独立进程运行，不与启动器绑定**。

生命周期完全由「扩展心跳」驱动，**不依赖任何浏览器进程名**，因此 Chrome / Edge / 千问 / 夸克 / 任意 Chromium 内核通用：

- `background.js` 用 `chrome.alarms`（约每 60s）POST `/api/heartbeat` 续命，`server.js` 记录 `lastHeartbeat`。
- `server.js` 的看门狗每 5s 检查：若 `Date.now() - lastHeartbeat > HEARTBEAT_TTL` 则 `process.exit(0)` 自退。
- 浏览器开着 → 心跳不断 → 后端存活；浏览器关闭 → service worker 被回收、alarms 停 → 心跳断 → 约 `HEARTBEAT_TTL`（默认 2.5min，覆盖 SW 闹钟节流）后后端自退。
- 另有「无请求自退」兜底：连续 `IDLE_TIMEOUT_MIN`（默认 30min）无任何请求，后端自退。

**想立即停**：面板「⏹ 停止后端」按钮（`POST /api/stop`）或 `curl -X POST http://localhost:3000/api/stop`。

**可调项（`.env`）**
- `HEARTBEAT_TTL`（毫秒，默认 150000）：心跳宽限，浏览器关后多久自退。
- `IDLE_TIMEOUT_MIN`（分钟，默认 30）：空闲自退时长。
- ⚠️ 旧的 `WEBCHAT_BROWSER_PROCS` 配置**已废弃**，心跳机制不再读取它，无需设置。

---

## 六、安全须知

- API Key 只放后端 `.env`，**绝不进前端**。
- 跨域：后端 `CORS *` 开发期够用；公网部署需改成具体来源。
- 后端必须本地运行；关掉后端对话连不上（面板提示连接失败）。
- 分享包不要带：`extension.pem`（签名私钥）、`extension.crx`、`backend/.env`（Key）、`*.log`、测试草稿 `*.cjs`（已在 `.gitignore` 忽略）。
