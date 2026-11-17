# Windows 环境：Chromium 下载失败时用 Edge 兜底

在 Windows 上跑网页测试时，`agent-browser` 默认会下载并启动自带的 Chrome for Testing。但部分网络环境无法访问 `storage.googleapis.com`（下载在极低进度就反复超时失败）。本参考给出"借本机 Edge（Chromium 内核，协议兼容）兜底"的完整步骤，让 Windows 用户无需翻墙即可跑通测试。

## 1. 安装 CLI

优先用隔离的 managed Node，避免污染系统环境：

```bash
npm install -g agent-browser
```

验证版本（若 `agent-browser` 命令不在 PATH，见第 4 节"直调二进制"）：

```bash
agent-browser --version
```

## 2. 尝试默认 Chromium（失败可跳过）

```bash
agent-browser install
```

若卡在 5% 左右反复超时、报 `storage.googleapis.com` 连接失败，直接走第 3 节用 Edge 兜底，不必纠结下载。

## 3. 改用本机 Edge（兜底方案）

> ⚠️ **每次测试开头的强制动作**：先用 `agent-browser close` 清掉可能存在的残留 daemon（见 4.2 / 4.4），再 `open` 带 Edge 参数。否则新参数会被静默忽略，跑的还是上一次的浏览器。

### 3.1 确认 Edge 路径

```bash
ls "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" 2>/dev/null && echo FOUND_X86
ls "C:/Program Files/Microsoft/Edge/Application/msedge.exe" 2>/dev/null && echo FOUND_X64
```

找到其一即可。Edge 通常随 Windows 自带，本机一般已存在。

### 3.2 设置可执行路径

```bash
export AGENT_BROWSER_EXECUTABLE_PATH="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
```

也可每次命令加 `--executable-path` 参数，效果相同。

### 3.3 以 Edge 驱动打开被测页

```bash
agent-browser --executable-path "$AGENT_BROWSER_EXECUTABLE_PATH" --args "--no-sandbox" open "https://目标网址"
agent-browser snapshot -i        # 取可交互元素（得到 @eN 元素ID）
agent-browser fill "@e6" "内容"  # 按元素ID填表
agent-browser click "@e4"        # 点击
agent-browser get url            # 取URL用于断言
agent-browser screenshot out.png # 留证
```

> Edge 为 Chromium 内核，Playwright 协议完全兼容，执行 / 断言 / 截图能力与官方 Chromium 一致，测试结论无差异。

## 4. 常见坑（Windows 必看）

### 4.1 Git Bash 把 `C:/` 错拼成 `d:\c\`

MSYS 会把 Windows 绝对路径 `C:/...` 误当成类 Unix 相对路径拼成 `d:\c\...`，导致全局 shim 找不到模块。两种解决：

- **方案 A（推荐）**：所有命令前加 `MSYS_NO_PATHCONV=1`：
  ```bash
  MSYS_NO_PATHCONV=1 agent-browser --executable-path "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" open "https://..."
  ```
- **方案 B**：绕过 shim，用 Node 直调包内脚本：
  ```bash
  node "$(npm root -g)/agent-browser/bin/agent-browser.js" --version
  ```

### 4.2 daemon 持久 + 每次开头必须先 close（关键）

`open` 会启动一个常驻浏览器 daemon，且**更换 `executable-path` / `--args` 时，若 daemon 已在跑，新参数会被静默忽略**（报 `daemon already running`，但浏览器仍是上一次的）。这极易在"残留 daemon 来自上一次会话"时踩坑——你以为用上了 Edge，实际跑的是旧的 / 默认浏览器，还毫无报错。

**强制首步**：每次开始测试前，先执行一次 `agent-browser close`（见 4.4，偶尔需重试），确认无残留 daemon，**再** `open` 带 Edge 参数。不要在疑似有旧 daemon 的情况下直接 `open` 带新参数。

```bash
# 标准开头：先清场，再开新会话（Windows 必须 MSYS_NO_PATHCONV=1）
MSYS_NO_PATHCONV=1 agent-browser close   # 必要时按 4.4 重试一次
MSYS_NO_PATHCONV=1 agent-browser --executable-path "$AGENT_BROWSER_EXECUTABLE_PATH" --args "--no-sandbox" open "https://目标网址"
```

### 4.3 安装位置

`npm install -g agent-browser` 后，二进制位于全局 node 前缀下的 `node_modules/agent-browser/`，可直接调用：

- 脚本入口：`node "<全局前缀>/node_modules/agent-browser/bin/agent-browser.js"`
- 原生二进制（Windows）：`<全局前缀>/node_modules/agent-browser/bin/agent-browser-win32-x64.exe`

"全局前缀"可通过 `npm root -g` 查看（例如 `C:/Users/<用户名>/.workbuddy/binaries/node/versions/22.22.2`）。

### 4.4 `close` 偶发超时，重试一次即可

Windows 上 `close` 偶尔报 `os error 10060`（连接超时）而退出码非 0，但 daemon 通常随后已关闭。不要误判为浏览器崩溃——直接再执行一次 `close`，返回 `✓ Browser closed` 即干净收尾。若仍失败，手动结束残留的 `msedge` / `agent-browser` 进程后重试。

## 5. 验证驱动可用

`open` 后执行 `snapshot -i`，若返回带 `@eN` 的可交互元素列表（如用户名输入框、按钮），即说明 Edge 驱动成功，可继续流程化测试。
