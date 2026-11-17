# 网页划线对话 · 小虾 🦐

> 📦 仓库地址：https://github.com/NoahEleven/webchat-extension

一个 **Chrome / Edge / 千问 / 夸克 等 Chromium 内核浏览器** 扩展：在任意网页上**选中或复制文字**，点一下工具栏图标，就能带着这段网页上下文，直接和 AI 对话、流式得到回答。

> 本质：复用 CodeBuddy Agent SDK 的 **Express + SSE 后端**，前端换成「浏览器扩展 + 网页划线交互」。

---

## 目录结构

```
webchat-extension/
├── README.md
├── webchat-protocol.reg.example   # 仅仓库内模板，不随分享包分发（协议改由部署脚本自动注册）
├── pack.mjs                       # 一键打包分享 zip（按 .gitignore 排除 node_modules/.env/私钥等）
├── extension/                     # 浏览器扩展（Chrome MV3）
│   ├── manifest.json
│   ├── background.js              # service worker：图标点击→开关浮层；心跳 ping 后端
│   ├── content.js                 # 注入网页：开/关浮层、读选区、状态持久化、触发协议
│   ├── panel.html / panel.js / panel.css   # 对话浮层界面与逻辑
│   └── icons/                     # 图标 icon16/32/48/128.png（分享包不含，由 deploy/gen-icons 自动生成）
└── backend/                       # AI 后端（Express + CodeBuddy SDK + SSE）
    ├── server.js                  # /api/chat(SSE) /api/health /api/heartbeat /api/stop
    ├── launcher.mjs               # 协议触发：托管模式静默拉起 server.js
    ├── launcher.vbs               # 隐藏窗口启动 launcher.mjs（由 agent 在部署时用 scripts/gen-vbs.mjs 生成，不随分享包分发）
    ├── patch-sdk.mjs              # postinstall 自动给 SDK 注入 windowsHide，消除 Windows 黑框
    ├── package.json / package-lock.json
    └── .env.example               # 复制为 .env 后填写（含 API Key）
```

---

## 前置依赖（重要）

- **Node.js 18+**：后端是 Node 程序。
- **codebuddy CLI（核心外部依赖，需收件人自备）**：后端通过 `@tencent-ai/agent-sdk` 在运行时 `spawn` 一个 `codebuddy` 子进程来真正调用 AI。`server.js` 的 `resolveCli()` 按以下顺序找它：
  1. 环境变量 `CODEBUDDY_CLI_PATH` 显式指定；
  2. 系统 `PATH` 上的 `codebuddy` 命令；
  3. 兜底固定路径 `~/.workbuddy/binaries/node/versions/22.22.2/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy`（**仅本机 WorkBuddy 托管环境才有**）。
  - 本机因装了 WorkBuddy，托管 Node 已自带 `codebuddy`，所以开箱可用。
  - **分享给别人的机器若没有 WorkBuddy**：需对方自行安装 CLI —— `npm i -g @tencent-ai/codebuddy-code`，并保证 `codebuddy` 在 `PATH` 上（或在 `.env` 设 `CODEBUDDY_CLI_PATH=绝对路径` 指向 CLI）。否则 `query()` 拉不起进程、后端连不上（登录模式和 Key 模式都依赖该 CLI）；此时仅 `WEBCHAT_DEMO=1` 演示模式可跑通交互闭环。

---

## 一、启动后端

```bash
cd backend
npm install
cp .env.example .env        # 然后按需填写 CODEBUDDY_API_KEY
npm start                   # 默认监听 http://localhost:3000
```

启动后访问 `http://localhost:3000/api/health` 应返回 `{ "status": "ok", ... }`。

### 三种模式
| 模式 | 条件 | 表现 |
|---|---|---|
| **登录模式（默认，零配置）** | 没填 `CODEBUDDY_API_KEY` 且未设 `WEBCHAT_DEMO` | 复用本机 `codebuddy` CLI 已登录凭据，**真实 AI**（首次需在终端跑一次 `codebuddy` 完成登录） |
| **Key 模式（推荐无人值守）** | 填了 `CODEBUDDY_API_KEY` | 用 Key 直连 CodeBuddy AI，不依赖交互登录，**真实 AI** |
| **演示模式** | 显式设 `WEBCHAT_DEMO=1` | 后端返回模拟流式回复，用来验收「划线→对话」交互闭环（无需任何账号/登录） |

---

## 二、申请 CODEBUDDY_API_KEY（可选，无人值守场景才需要）

> 默认**不填 Key 也是真实 AI**（登录模式，复用本机 `codebuddy` CLI 已登录凭据）。只有想脱离交互登录、无人值守直连时才需要配 Key。

1. 打开 https://www.codebuddy.cn → 登录
2. 进入「个人中心 / API 密钥」生成 Key
3. 把 Key 填进 `backend/.env` 的 `CODEBUDDY_API_KEY=`
4. 重启后端 `npm start`

> 没 Key 也没关系——登录模式默认就是真实 AI；纯验收交互闭环可设 `WEBCHAT_DEMO=1` 进演示模式。

---

## 三、在浏览器加载扩展

本扩展是标准 Chrome MV3，兼容一切 Chromium 内核浏览器（Chrome / Edge / 千问 / 夸克等）。**无法从 `.crx` 文件直接安装**（现代浏览器已禁止本地 `.crx` 安装），请用「加载已解压」方式：

1. 浏览器进入 **扩展管理页 → 开启「开发者模式」**（`chrome://extensions` 或 `edge://extensions` 等）
2. 点 **「加载已解压的扩展程序」**，目录选本项目的 `extension/`
   - ⚠️ **分享包不含图标 png**：加载前请先生成图标——已跑过 `node scripts/deploy.mjs` 会自动生成；手动加载则先跑 `node gen-icons.mjs`。否则报 `Could not load icon` 加载失败。
3. 加载成功后，图标出现在扩展栏
4. **改了扩展代码后**，回扩展管理页点「重新加载」才能生效

---

## 四、一键启动后端（可选但推荐，免开终端）

面板里的「🚀 启动后端」按钮靠自定义协议 `webchat://start` 自动拉起后端，需要**先注册一次协议处理器**。

- **若由 agent 按本 skill 部署（推荐）**：运行 `node scripts/deploy.mjs` 会**自动注册协议**，并自动在 `backend/` 生成 `launcher.vbs` 隐藏启动器，开箱即用，无需手动操作（`launcher.vbs` 是部署期产物，绝不随分享包分发/上传；缺失时可单独 `node scripts/gen-vbs.mjs <backend目录>` 生成）。
- **手动 / 分享给别人（无 WorkBuddy）**：
  - **最省事**：跳过协议，面板点「📋 复制启动命令」→ 终端执行，或直接 `cd backend && npm start`。
  - **想要协议按钮免终端**：手动注册（把下列命令里的路径改成你机器真实的 `backend` 路径）。注意命令指向 `launcher.mjs`，直接用 `node` 跑会有一个 cmd 窗口闪现；若要完全无黑框，先 `node scripts/gen-vbs.mjs <backend目录>` 生成 `launcher.vbs`（唯一 source of truth 见 `scripts/gen-vbs.mjs`，隐藏启动 `launcher.mjs`），再让命令指向该 `.vbs`：
    ```bat
    reg add "HKCU\Software\Classes\webchat" /ve /t REG_SZ /d "webchat Protocol" /f
    reg add "HKCU\Software\Classes\webchat" /v "URL Protocol" /t REG_SZ /d "" /f
    reg add "HKCU\Software\Classes\webchat\shell\open\command" /ve /t REG_SZ /d "\"C:\Windows\System32\wscript.exe\" \"C:\你的路径\webchat-extension\backend\launcher.mjs\" \"%1\"" /f
    ```

注册后：点「🚀 启动后端」即可无感拉起（首次会问「是否允许打开 webchat 链接」，允许即可）。**后端生命周期由扩展心跳托管**：浏览器开着→后端存活；浏览器关→心跳断→约 2.5 分钟后后端自退，不常驻、无需手动停。想立即停可点面板「⏹ 停止后端」或访问 `POST /api/stop`。

---

## 五、怎么用

1. 打开任意网页（新闻、文档、微信读书、千问等都行）
2. **点工具栏上的「🦐 小虾」图标** → 右侧弹出对话面板（高约视口 2/3，自适应）
3. **拖动浮层**：拖顶部标题栏移动面板（移出浮层也跟手、不抖）；**双击标题栏**复位到右上角。位置自动记住，刷新/换页后还在
4. 喂上下文，任选：
   - **选中网页文字** → 点 **「➕ 添加选中文本」**（同时读网页选区 + 系统剪切板：选区由 background 用 `chrome.scripting.executeScript(allFrames)` 直插每帧读取，**微信读书/千问等 iframe 阅读器也能抓到**；剪切板含输入法复制内容）
   - **直接发送**：在输入框粘贴/输入并回车，发送时**自动把本次内容（剪贴板或提问文本）收进上下文**
5. 上下文片段只显示 **10~20 字摘要 + …**（悬停看全文），不可直接编辑；多段累加，右侧 ✕ 单独删除
6. 回车发送，AI 回答**逐字流式**显示，多轮保持上下文
7. **状态持久化**：开关/位置/上下文/对话存 `chrome.storage`，刷新或换页后自动重开不丢（手动 ✕ 关闭后记住关闭状态）

---

## 六、分享给别人 / 打包

**`backend/` 是必须的，必须一起打包。** 浏览器扩展只是「UI 外壳」——真正的 AI 能力（连接 CodeBuddy SDK、spawn `codebuddy` CLI、管理 API Key）全在后端。没有 `backend/`，扩展没有 AI 能力、连不上。**所以分享时 `extension/` + `backend/` 两个目录都要带。**

- **不要**只发 `.crx`：现代 Chrome/Edge 禁止本地 `.crx` 安装，发了也装不上。
- **正确做法**：把整个 `webchat-extension/` 文件夹发给对方 → 对方按上面步骤 `npm install` + 加载 `extension/` +（可选）注册协议。
- **一键打包（推荐）**：在项目根目录执行 `node pack.mjs` → 自动按 `.gitignore` 在父目录生成干净的 `webchat-extension-share-YYYYMMDD.zip`。**打包出来是一个「二合一」目录 `webchat-extension/`**：
  - `SKILL.md` 直接位于 `webchat-extension/` **根目录**（满足技能规范：SKILL.md 在根目录或一级目录）。
  - 同时含 `extension/`、`backend/`（手动安装用）与 `scripts/`、`references/`、`assets/`（agent 技能用）。
  - 给**不使用 WorkBuddy** 的收件人：用里面的 `extension/` + `backend/` 按上面步骤 `npm install` + 加载扩展即可。
  - 给**用 WorkBuddy** 的收件人：把整个 `webchat-extension/` 文件夹复制到 `~/.workbuddy/skills/webchat-extension/`，agent 部署时自动注册协议、开箱即用。
  - 脚本已自动排除 `node_modules/`、`.env`、私钥、`.crx`、`*.log`、`*.cjs`；保留 `.env.example` 模板与技能目录。
- **⚠️ 收件人还需自备 codebuddy CLI**：本项目不随包分发该 CLI（见「前置依赖」一节）。对方机器若没有 WorkBuddy，需 `npm i -g @tencent-ai/codebuddy-code` 并确保在 `PATH` 上，否则后端连不上（仅 `WEBCHAT_DEMO=1` 演示模式可跑）。
- **正式广分发**：上架 Chrome / Edge 应用商店，发商店链接。
- **打包清单**
  - ✅ 带：`SKILL.md`（技能入口，根目录）、`extension/`（**不含 icons png，加载前由 deploy / gen-icons 自动生成**）、`backend/` 源码（`server.js` `launcher.mjs` `patch-sdk.mjs` `package.json` `package-lock.json` `.env.example`）、`scripts/`（部署脚手架，含内联生成 launcher.vbs + 图标生成）、`references/`（排错表）、`assets/`（技能资源）、`README.md`、`gen-icons.mjs`
  - ❌ 不带：`backend/node_modules/`（让收件人 `npm install` 即可）、`backend/.env`（含真实 Key）、`extension.pem`/`extension.crx`、**`*.png`（图标不进包，由 agent 部署时生成）**、`*.log`、`*.cjs` 测试草稿、**`launcher.vbs` / `webchat-protocol.reg.example` / `.gitignore`（不随分享包分发；launcher.vbs 由部署脚本自动生成、协议由部署自动注册）**
  - 这些由打包脚本按 `.gitignore` + 硬性禁止列表排除，打包前确认没混进去。

---

## 七、已知限制 / 注意

- **后端必须本地运行**：插件通过 `http://localhost:3000` 调后端。关掉后端，对话连不上（面板提示连接失败）。
- **跨域**：后端已开 `CORS *`，开发期够用。上线公网需改具体来源并部署后端。
- **side_panel**：本方案用「网页内注入浮层（iframe）」而非浏览器侧边栏，兼容性最好。
- **API Key 安全**：Key 只放后端 `.env`，**绝不进前端**。
- **真实 AI 能力**：来自 CodeBuddy Agent SDK，模型默认 `deepseek-v4-flash`，可在 `.env` 用 `CODEBUDDY_MODEL=` 改（`auto`/`hy3`/`glm-5.2`/`kimi-k2.x`/`deepseek-v4-*` 等，本账户不支持 `claude-sonnet-4`）。

---

## 八、出问题怎么办

| 现象 | 排查 |
|---|---|
| 面板提示「连接后端失败」 | 确认 `cd backend && npm start` 已启动；端口是 3000 |
| 点「🚀 启动后端」没反应 | 多半是 `webchat://` 协议未注册（见第四节）。可改用面板「📋 复制启动命令」手动 `npm start` |
| 点图标没反应 | 多见于 `chrome://`、`edge://` 等系统页（扩展无法注入）；普通网页正常。确认扩展已加载且未被禁用 |
| 选中文字点「添加选中文本」没反应 | 选区读取走 `chrome.scripting.executeScript(allFrames)`，正常能抓 iframe 阅读器；若阅读器是 **sandboxed iframe（无 allow-scripts）** 且屏蔽 copy，则只能手动粘贴/输入发送（发送会自动收上下文）。平台限制非 bug |
| 收到的是演示（模拟）回复而非真实 AI | 说明设了 `WEBCHAT_DEMO=1`。删掉该变量重启即走登录模式真实 AI；若登录态失效，终端跑一次 `codebuddy` 重新登录，或在 `.env` 填 `CODEBUDDY_API_KEY` 走 Key 模式 |
| `/api/health` 返回 `demo:true` | 说明设了 `WEBCHAT_DEMO=1`（演示模式）。想要真实 AI 请移除该变量（默认登录模式）或填 Key |
| **真实模式一直转圈、无回答**（后端日志 `EADDRINUSE` / CLI 卡死） | 官方 CLI 的 prewarm 端口和本机 WorkBuddy 桌面应用撞车。在 `.env` 设 `SERVER__PORT=40123`（或空闲端口）并重启；若环境变量残留旧 `SERVER__PORT`，启动时用 `SERVER__PORT=40123 npm start` 显式覆盖 |
| 后端报 `400 model [...] service info not found` | 模型名不对，把 `CODEBUDDY_MODEL` 改成 `deepseek-v4-flash`、`hy3` 或 `auto` |
| **Windows 上每次对话 / 启动后端都弹黑框** | SDK 内部 spawn CLI 默认 `windowsHide:false`。后端 `package.json` 已加 `postinstall` 自动跑 `patch-sdk.mjs` 给 SDK 注入 `windowsHide:true`；`npm install` 后自然生效。若重装后仍弹，手动跑一次 `node backend/patch-sdk.mjs` |
