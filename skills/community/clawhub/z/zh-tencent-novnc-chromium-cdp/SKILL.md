---
name: zh-tencent-novnc-chromium-cdp
description: "做自动发抖音、自动发小红书等等各大平台的网页自动化，还在被滑块、验证码、人机验证卡到任务翻车、反复失败？试试这个一键部署的远程可视化浏览器：Linux（云服务器/NAS/本地）noVNC + Chromium + CDP 三合一，Windows 本机 Edge/Chrome CDP 一键接管，让AI Agent和你共享同一个浏览器，服务器无图形界面也能可视化操控，登录、过验证全靠人工兜底，再也不怕自动化卡壳，发平台内容一次稳到底！"
version: 1.0.45
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [novnc, chromium, cdp, xvfb, x11vnc, remote-browser, windows, edge]
---

## 📖 使用教程

**两步搞定，全程不用动手。**

**第一步：安装本技能**

复制以下提示词发送给 AI Agent 自动安装：

```
请先检查是否已安装 clawhub.ai 商店，若未安装，请先安装 clawhub CLI（npm i -g clawhub 或访问 https://clawhub.ai），然后安装 zh-tencent-novnc-chromium-cdp 技能。若已安装，则直接安装 zh-tencent-novnc-chromium-cdp 技能。
```

**第二步：使用**

对 AI Agent 发送提示词：

```
使用 zh-tencent-novnc-chromium-cdp 技能
```

AI Agent 收到后会全自动处理：检测系统环境 → 安装依赖 → 启动 Chromium 远程浏览器 → 配置开机自启 → 先发 noVNC 地址和密码等核心信息 → 最后截图确认。全程不需要你敲任何命令。

> 💡 部署完成后遇到登录、验证码、滑块，在 noVNC 页面上手动操作即可，完成后告诉 AI 继续。

# noVNC + Chromium + CDP 远程可视可控浏览器（Linux / Windows 双平台）

## 技能简介

本技能同时支持 Linux 和 Windows，覆盖云服务器与本地环境：Linux 服务器上部署 noVNC + Chromium 远程可视化浏览器，Windows 本机通过 CDP 远程调试直接接管 Edge/Chrome 浏览器。

它解决的是传统 Headless 浏览器自动化最常见的痛点：遇到登录、扫码、滑块、验证码、风控验证时，AI 可以暂停并让用户在 noVNC 页面中手动完成验证，验证通过后再继续由 AI 接管操作。

适合用于抖音创作者中心、小红书、微博、番茄小说、各类后台管理系统等需要"AI 自动化 + 人工验证协作"的网页场景。

## 核心能力

- **可视化浏览器**：Chromium 运行在 Xvfb 虚拟屏幕上，用户可通过 noVNC 网页实时查看画面。
- **AI 可控**：Agent 通过 CDP 连接 `127.0.0.1:9223`，可执行打开网页、点击、输入、读取页面、截图等操作。
- **人机协作**：遇到登录、二维码、滑块、验证码时，用户可在 noVNC 中手动处理，处理完成后 AI 继续执行。
- **权限预检**：安装前先确认 root/sudo 权限，权限不足时主动提醒用户授权方式，避免半安装状态。
- **安全边界**：默认只建议开放 noVNC 的 `6080/tcp`，CDP 调试端口 `9223/tcp` 不建议暴露到公网。
- **完成反馈**：部署完成后，Agent 必须先主动发送 noVNC 访问地址、访问密码、开机自启状态和端口开放提醒；截图作为最后一步补充确认发送，截图失败不得阻塞前面的核心信息。
- **Windows 本机模式**：Agent 自动启动 Edge/Chrome 远程调试端口，通过 CDP 接管浏览器，本机屏幕实时可见，截取当前页面反馈，无需安装额外组件。

部署完成后，Agent 通过 CDP 控制浏览器（详见「七、通过 CDP 控制浏览器」）。

> ⚠️ **铁律（最高优先级）**：本技能部署完成后，用户让 AI Agent「打开浏览器 / 看网页 / 截图 / 点击 / 登录」等任何浏览器操作，**默认必须使用本技能部署的 CDP 浏览器**（`127.0.0.1:9223`）。Linux 下即 noVNC 里 `:99` 上的 Chromium，Windows 下即用户本机屏幕上的 Edge/Chrome。**禁止使用 Agent 自带的内置 headless 浏览器或临时拉起其他实例**，否则用户和 Agent 看到的画面不同频。完整规则见「十一、重要原则」。

## 服务器配置要求与端口提醒

### 开始部署前必须先提醒用户

本技能需要安装系统依赖、下载 noVNC、启动 Chromium 图形浏览器和 VNC 转发服务，步骤较多。Agent 在正式执行安装前，应先发一条简短提醒，让用户知道部署需要等待一段时间。

推荐提醒话术（根据检测到的环境类型选择对应话术）：

**CLOUD（云服务器）环境：**
```text
开始部署 noVNC + Chromium + CDP 远程可视可控浏览器。

重要提示：服务器建议至少 2H4G。
端口提醒：必须在云服务器安全组放行 6080/tcp；5900/tcp 为高级用途，可选开放，开放时建议限制来源 IP。9223/tcp（CDP 调试端口）仅供 Agent 本机使用，不建议对公网开放。
预计耗时：通常约 5-15 分钟；如果服务器配置较低、网络较慢或需要安装大量依赖，可能需要 20-30 分钟。部署过程中请耐心等待，不要中断。
Token 提醒：顺利部署预计消耗约 2万-5万 tokens；如果网络较慢、依赖安装失败、需要自动修复或多次重试，可能消耗 5万-10万+ tokens，实际以执行过程为准。开始前请确认当前会话/套餐剩余 Token 必须大于预计消耗，建议至少预留 10万 tokens 以上，避免部署过程中因 Token 不足中断。
进度提醒：安装过程中我会每 30 秒检查一次进度和服务状态，如有常见问题会先自动修复；并且每分钟向你汇报一次部署进度，直到安装成功。
```

**NAS 环境：**
```text
开始部署 noVNC + Chromium + CDP 远程可视可控浏览器。

重要提示：NAS 建议至少 2H4G。
端口提醒：部署完成后通过局域网地址访问。如需外网访问，请在路由器上设置端口转发 6080 TCP → <NAS_IP>。9223/tcp（CDP 调试端口）仅供 Agent 本机使用，不建议开放。
预计耗时：通常约 5-15 分钟；如果 NAS 性能较低、网络较慢，可能需要 20-30 分钟。部署过程中请耐心等待，不要中断。
Token 提醒：顺利部署预计消耗约 2万-5万 tokens；实际以执行过程为准。建议至少预留 10万 tokens 以上。
进度提醒：安装过程中我会每 30 秒检查一次进度并每分钟汇报，直到安装成功。
```

**LOCAL（本机 Linux）环境：**
```text
开始部署 noVNC + Chromium + CDP 远程可视可控浏览器。

重要提示：本机建议至少 2H4G。
端口提醒：部署完成后通过内网地址访问。如需外网访问，请在路由器上设置端口转发 6080 TCP → <本机IP>。9223/tcp（CDP 调试端口）仅供 Agent 本机使用，不建议开放。
预计耗时：通常约 5-15 分钟。部署过程中请耐心等待，不要中断。
Token 提醒：顺利部署预计消耗约 2万-5万 tokens。
进度提醒：安装过程中我会每 30 秒检查一次进度并每分钟汇报，直到安装成功。
```

如果检测到服务器配置低于 2H4G，应额外提醒用户可能出现 Chromium 卡顿、白屏或被系统杀掉的问题。

### 安装过程进度监控与自动修复

部署本技能时，Agent 不应长时间静默等待。正式开始安装后，应执行以下进度监控规则：

1. **每 30 秒检查一次进度**：检查当前安装命令是否仍在运行，查看最近日志，确认是否卡在依赖安装、软件下载、服务启动或端口监听阶段。
2. **每 30 秒检查关键状态**：重点检查 `Xvfb`、`chromium`、`x11vnc`、`websockify/noVNC` 是否启动，`6080/tcp` 和 `9223/tcp` 是否正常监听。
3. **常见问题优先自动修复**：如依赖缺失、包管理锁、残留旧进程、端口占用、Chromium 启动失败、noVNC 未下载完整等，应先尝试清理旧进程、重新安装依赖、重新启动服务或重新下载组件。
4. **每分钟汇报一次进度**：向用户发送简短消息，说明当前阶段，例如“正在安装系统依赖”“正在启动 Chromium”“正在检测 6080 端口”“正在准备完成信息”“正在执行最后截图确认”。
5. **不要刷屏**：进度消息保持简短，每分钟一次即可；只有遇到需要用户处理的问题时才立即额外提醒。
6. **直到成功或需要人工介入**：持续监控并汇报，直到 noVNC 地址可访问、Chromium 已打开百度页面、核心完成信息已发送、最后截图已发送或已明确报告截图失败原因；如果自动修复失败，应明确告诉用户失败步骤、原因和下一步需要用户做什么。

### 最低服务器配置

本技能会启动 Chromium 图形浏览器、虚拟显示器和 VNC 转发服务，资源占用高于普通命令行脚本。建议服务器配置不低于：

```text
最低推荐：2 核 CPU / 4GB 内存（2H4G）
系统推荐：Debian 10+ / Ubuntu 20.04+
磁盘建议：至少预留 5GB 可用空间
```

低于 2H4G 的服务器也可能启动成功，但容易出现 Chromium 卡顿、页面白屏、验证码页面 CPU 飙高、浏览器被系统杀掉等问题。

### 端口开放说明

必须开放：

- `6080/tcp`：noVNC 网页访问端口。用户通过 `http://<服务器公网IP>:6080/vnc.html` 打开远程 Chromium 浏览器。

可选开放：

- `5900/tcp`：VNC 原生端口。默认仅供本机 websockify 转发使用，一般不需要公网开放；只有需要用 VNC 客户端直连时才考虑开放，并建议限制来源 IP。
- `9223/tcp`：Chromium CDP 调试端口。默认仅供 Agent 在服务器本机控制浏览器使用；只有明确需要远程调试时才考虑开放，并必须限制来源 IP，避免浏览器被他人接管。

## 适用场景

本技能覆盖两种使用模式：

- **Linux 服务器模式**：在云服务器上启动可视化浏览器，用户通过 noVNC 网页实时查看和手动操作，AI Agent 通过 CDP 控制同一实例。
- **Windows 本机模式**：直接在用户本机启动 Edge/Chrome 远程调试端口，Agent 通过 CDP 接管，用户在本机屏幕上实时看到所有操作。

典型场景：

- 登录类后台：抖音创作者中心、小红书创作者平台、微博、公众号后台等。
- 风控验证：滑块验证、扫码登录、短信验证、图形验证码、设备验证等。
- 内容发布：自动打开发布页、填写标题/正文/标签/封面，并让用户处理最后的人工验证。
- 网页调试：需要用户和 AI 同时看到同一个浏览器画面，方便排查页面状态。

不适合场景：

- 纯 API 调用任务，不需要浏览器画面。
- 对安全要求极高、不能暴露任何远程桌面入口的生产环境。
- Linux 模式：无法开放 `6080/tcp` 或无法提供 root/sudo 权限的服务器。（Windows 模式无此限制）

最终效果：

**Linux 模式：**
- 用户访问：`http://<服务器IP>:6080/vnc.html`
- Agent 控制：`http://127.0.0.1:9223/json` / CDP WebSocket
- 浏览器运行在虚拟显示器 `:99`

**Windows 模式：**
- 用户在本机屏幕直接看到 Edge/Chrome 浏览器
- Agent 控制：`http://127.0.0.1:9223/json` / CDP WebSocket
- 无需额外安装任何组件

> 💡 统一使用 **9223** 端口，避免与 AI Agent 自带的 Playwright/Chromium 抢占 **9222** 端口。

数据流：

**Linux：** Xvfb → 虚拟显示器 `:99` → Chromium (CDP `9223`) → x11vnc → noVNC/websockify → 用户浏览器
**Windows：** Edge/Chrome (CDP `9223`) + 本机屏幕 → Agent 控制，无需额外组件

## 零、系统检测（第一步，必须执行）

Agent 加载本技能后，**第一步必须先检测当前操作系统**：

```bash
# 第一步：检测操作系统
uname -s 2>/dev/null | grep -qi linux && echo "LINUX" || true

# 如果是 Linux，再细分环境类型（云服务器 / NAS / 本地 Linux）
if [ "$(uname -s)" = "Linux" ]; then
  # 检测是否云服务器（腾讯云/阿里云/AWS metadata）
  if curl -s --connect-timeout 2 http://metadata.tencentyun.com/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://100.100.100.200/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  elif curl -s --connect-timeout 2 http://169.254.169.254/latest/meta-data/ 2>/dev/null | grep -q .; then
    echo "ENV_TYPE=CLOUD"
  # 检测是否 NAS（群晖 Synology / QNAP 威联通）
  elif [ -f /etc/synoinfo.conf ]; then
    echo "ENV_TYPE=NAS"
  elif [ -f /etc/platform.conf ] || [ -f /etc/version ]; then
    echo "ENV_TYPE=NAS"
  else
    echo "ENV_TYPE=LOCAL"
  fi
fi
```

**分流逻辑**：

- **检测到 Linux（CLOUD / NAS / LOCAL）** → 继续执行「一、检查系统与服务器配置」及后续章节（noVNC + Chromium 远程部署流程）。完成后根据环境类型发送对应地址：
  - `CLOUD`（云服务器）→ 发送公网 IP 的 noVNC 地址
  - `NAS`（NAS 设备）→ 发送本地内网 IP 的 noVNC 地址，并提醒用户在 NAS 控制面板开放 6080 端口
  - `LOCAL`（本地 Debian/Ubuntu）→ 发送本地内网 IP 的 noVNC 地址，并提醒用户放行系统防火墙 6080 端口
- **检测到 Windows** → 跳过 Linux 部署章节，直接跳转到「十二、Windows 系统：远程调试 CDP 控制 Edge/Chrome」。

> 以下「一」至「六-bis」仅适用于 Linux 系统（含 CLOUD / NAS / LOCAL）。

> ⚠️ **铁律：系统检测是强制步骤，不可跳过。** Agent 拿到 `ENV_TYPE` 后，**必须严格按以下规则发送对应 IP 地址，不得自行判断或偷懒**：
>
> | ENV_TYPE | 发送地址 | 硬规则 |
> |---|---|---|
> | `CLOUD` | **公网 IP** | 必须用 `curl -4 -s https://ifconfig.me` 获取公网 IP，**严禁**发 `192.168.x.x` / `10.x.x.x` / `172.16-31.x.x` 内网地址 |
> | `NAS` | **内网 IP** | 用 `hostname -I` 取内网 IP，同时提醒用户在 NAS 控制面板开放 6080 端口 |
> | `LOCAL` | **内网 IP** | 用 `hostname -I` 取内网 IP，同时提醒用户放行系统防火墙 6080 端口 |
>
> **常见错误（禁止）**：检测到 `CLOUD` 却发内网 IP → **严重错误**，用户无法从公网访问。检测到 `NAS`/`LOCAL` 却试图获取公网 IP → 同样错误，本地环境可能根本没有公网 IP。Agent 必须严格执行上述映射，不能凭"感觉"选 IP。

## 一、检查系统与服务器配置

```bash
cat /etc/os-release | head -3
uname -m
nproc
free -h
df -h /
```

推荐环境：Debian 10+ / Ubuntu 20.04+ / 较新的 Linux 发行版。

配置要求：建议至少 **2 核 CPU / 4GB 内存（2H4G）**。如果内存低于 4GB，Agent 应先提醒用户可能出现 Chromium 卡顿、白屏或被系统杀掉的问题，再继续安装。

## 二、权限预检（必须）

部署本技能需要安装系统包、写入 `/opt` 和 `/root/start-remote-browser.sh`，需要 `root` 或可用的 `sudo` 权限。

```bash
if [ "$(id -u)" = "0" ]; then
  echo "PERMISSION_OK: 当前是 root 用户"
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  echo "PERMISSION_OK: 当前用户可免密 sudo"
else
  echo "PERMISSION_DENIED: 当前用户不是 root，且无法免密 sudo。"
fi
```

如果输出 `PERMISSION_OK`，直接继续部署。

如果输出 `PERMISSION_DENIED`，按以下优先级处理：

**首选：配置免密 sudo**

引导用户在服务器终端执行一行命令即可，密码不离开用户机器：

```bash
echo "$(whoami) ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/hermes-deploy
```

完成后 Agent 即可通过 `sudo` 继续部署。部署完成后执行 `sudo rm /etc/sudoers.d/hermes-deploy` 收回权限。

**备选：提供 SSH 凭证**

仅当用户无法访问服务器终端时使用。Agent 应说明凭证用途：

```text
当前环境权限不足。请提供以下 SSH 信息以便我登录服务器完成安装：

- 服务器 IP
- SSH 端口（默认 22）
- SSH 用户名
- SSH 密码

以上凭证仅用于以下操作，不做其他用途：
1. 安装系统依赖（apt install xvfb x11vnc git python3-pip 等）
2. 下载 noVNC 到 /opt/noVNC
3. 创建启动脚本 /root/start-remote-browser.sh
4. 配置 systemd 开机自启（写入 /etc/systemd/system/）
5. 放行防火墙端口 6080

部署完成后请立即修改密码。
```

> ⚠️ Agent 收到凭证后不得存储、记录，部署完成后必须提醒用户修改密码。

## 三、安装依赖

Debian / Ubuntu：

```bash
apt update && apt upgrade -y
apt install -y xvfb x11vnc git python3-pip curl wget ca-certificates
```

### 优先安装 deb 版 Chromium/Chrome

本技能需要通过 CDP 控制浏览器，安装浏览器时推荐**优先安装 deb 包形式的 Chromium/Chrome**。如果 deb 版安装失败，再自动切换至系统可用的其他 Chromium/Chrome 版本，保证部署流程尽量不中断。

安装时应先检测系统类型，并按“deb 版优先、失败后自动切换至其他版本”的策略执行：

```bash
. /etc/os-release

if [ "$ID" = "debian" ]; then
  apt install -y chromium || apt install -y chromium-browser || true
elif [ "$ID" = "ubuntu" ]; then
  echo "Ubuntu 环境优先安装 deb 版 Chrome 作为 Chromium/CDP 兼容浏览器。"
  if wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb; then
    apt install -y /tmp/google-chrome-stable_current_amd64.deb || true
  fi
  if command -v google-chrome-stable >/dev/null 2>&1; then
    ln -sf /usr/bin/google-chrome-stable /usr/local/bin/chromium
    # Chrome 与 Chromium 共享同一套 CDP 调试协议和 user-data-dir。
    # 「六-bis」的 systemd 模板中 --disable-session-crashed-bubble / --restore-last-session=false 和 ExecStartPre 同样适用于 Chrome。
  else
    echo "deb 版 Chrome 安装失败，尝试安装系统源 Chromium/Chromium Browser。"
    apt install -y chromium || apt install -y chromium-browser || true
  fi
else
  apt install -y chromium || apt install -y chromium-browser || true
fi

CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: 未找到 Chromium/Chrome 可执行文件"
  exit 1
fi

echo "浏览器路径：$CHROME_BIN"
```

安装 noVNC 和 websockify：

```bash
cd /opt
if [ ! -d /opt/noVNC ]; then
  git clone https://github.com/novnc/noVNC.git
fi
pip3 install websockify --break-system-packages
```

如果 noVNC master 版本在 Chrome 中出现 ES module 报错，可固定到稳定版：

```bash
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
```

## 四、开放端口

端口放行规则随环境类型不同而变化。Agent 必须根据前面确定的环境类型（`$ENV_TYPE`）选择对应的防火墙指令：

**CLOUD（云服务器）：**
```bash
# 系统防火墙放行 noVNC
ufw allow 6080/tcp || true
ufw reload || true

# 云厂商安全组也要放行：
# - 6080/tcp：noVNC 网页访问端口
# - 9223/tcp：CDP 调试端口，**不建议对公网开放**，仅供 Agent 本机 127.0.0.1 使用
```

**NAS：**
```bash
# NAS 部署：内网直接访问，无需操作防火墙。
# 如需外网访问：在路由器上设置端口转发 6080 TCP → <NAS_IP>
# 9223/tcp CDP 端口仅供本机，不转发。
echo "NAS 环境：noVNC 通过内网地址访问。如需外网访问，请在路由器做端口转发 6080。"
```

**LOCAL（本机 Linux）：**
```bash
# 系统防火墙放行 noVNC
ufw allow 6080/tcp || true
ufw reload || true

# 如需外网访问：在路由器上设置端口转发 6080 TCP → <本机IP>
# 9223/tcp CDP 端口仅供本机，不转发。
```

## 五、创建一键启动脚本

### 1. 生成 noVNC 访问密码（必须）

为防止 noVNC 端口（6080）被裸暴露公网导致浏览器被任何人接管，启动前必须生成一个 **8 位随机密码**（字母+数字混合），并让 x11vnc 用密码模式启动。Agent 必须把这个密码原文保存到固定路径，方便部署后回复给用户。

```bash
# 8 位随机密码（字母+数字混合）
NOVNC_PASS=$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 8)
echo -n "$NOVNC_PASS" > /root/.novnc_password
chmod 600 /root/.novnc_password

# 用 x11vnc 自己的工具生成 VNC 密码文件
x11vnc -storepasswd "$NOVNC_PASS" /root/.vncpasswd
chmod 600 /root/.vncpasswd

echo "noVNC 访问密码已生成：$NOVNC_PASS"
echo "明文存储于：/root/.novnc_password（仅 root 可读）"
echo "VNC 密码文件：/root/.vncpasswd"
```

> 后续 x11vnc 启动必须使用 `-rfbauth /root/.vncpasswd`，**不再使用 `-nopw`**。

### 2. 写入 `/root/start-remote-browser.sh`

写入 `/root/start-remote-browser.sh`：

```bash
cat > /root/start-remote-browser.sh <<'SCRIPT_END'
#!/bin/bash
set -e

pkill -9 -f x11vnc 2>/dev/null || true
pkill -9 -f Xvfb 2>/dev/null || true
pkill -9 -f websockify 2>/dev/null || true
pkill -9 -f 'chromium.*remote-debugging-port=9223' 2>/dev/null || true
sleep 2

echo "[1/4] 启动虚拟显示器..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1
export DISPLAY=:99

echo "[2/4] 启动 Chromium (CDP:9223)..."
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable || true)
if [ -z "$CHROME_BIN" ]; then
  echo "ERROR: 未找到 Chromium/Chrome 可执行文件"
  exit 1
fi
# CDP 仅供 Agent 本机控制，监听 127.0.0.1，不对外暴露。
# ⚠️ 严禁添加 --headless 或 --headless=new，否则 noVNC 画面无法显示。
"$CHROME_BIN" \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9223 \
  --remote-debugging-address=127.0.0.1 \
  --remote-allow-origins='*' \
  --window-size=1920,1080 \
  --start-maximized \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir=/root/.chromium-remote \
  --restore-last-session=false \
  https://www.baidu.com/ &
sleep 3

echo "[3/4] 启动 x11vnc..."
x11vnc -display :99 -forever -rfbauth /root/.vncpasswd -quiet -listen 127.0.0.1 &
sleep 1

echo "[4/4] 启动 noVNC (端口:6080)..."
websockify --web /opt/noVNC 6080 127.0.0.1:5900 &
sleep 1

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "========================================"
echo "  ✅ 远程浏览器已就绪"
echo "  用户访问: http://${IP}:6080/vnc.html"
echo "  CDP: http://127.0.0.1:9223/json（仅供本机 Agent）"
echo "========================================"
SCRIPT_END

chmod +x /root/start-remote-browser.sh
```

## 六、启动远程浏览器

```bash
bash /root/start-remote-browser.sh
```

启动完成后，用户访问：

```text
http://<服务器IP>:6080/vnc.html
```

CDP 检查地址：

```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

**⚠️ 部署到这一步时，手动脚本启动的 Chromium 还在后台运行。接下来配置 systemd 自启前，必须先杀掉手动进程，避免两个 Chromium 实例抢同一个 `--user-data-dir`，导致标签页不断堆叠。**

```bash
pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" 2>/dev/null || true
sleep 2
```

> 否则会出现：手动脚本开一个百度 → systemd 自启又开一个 → OOM 重启再开一个，堆成三个百度页。

## 六-bis、配置开机自启（必须）

为了确保服务器重启后 noVNC + Chromium + CDP 仍能自动恢复运行，必须把整套服务做成 **systemd 单元**，不能只依赖一次性的 `bash /root/start-remote-browser.sh`。

部署完成后必须执行以下步骤，并启用 `enable --now`，使服务**立即生效 + 开机自启**：

```bash
# 1) Xvfb 虚拟显示器
cat > /etc/systemd/system/xvfb.service <<'EOF'
[Unit]
Description=Xvfb virtual display :99
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/Xvfb :99 -screen 0 1920x1080x24 -ac
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 2) x11vnc（必须使用 -rfbauth 走密码模式）
cat > /etc/systemd/system/x11vnc.service <<'EOF'
[Unit]
Description=x11vnc server on :99 (password protected)
After=xvfb.service
Requires=xvfb.service

[Service]
Type=simple
Environment=DISPLAY=:99
ExecStart=/usr/bin/x11vnc -display :99 -forever -shared -rfbauth /root/.vncpasswd -rfbport 5900 -quiet
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 3) noVNC websockify
cat > /etc/systemd/system/novnc.service <<'EOF'
[Unit]
Description=noVNC websockify on 6080
After=x11vnc.service
Requires=x11vnc.service

[Service]
Type=simple
ExecStart=/usr/local/bin/websockify --web=/opt/noVNC 6080 localhost:5900
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 4) Chromium + CDP（自动找可用 Chromium/Chrome 二进制）
CHROME_BIN=$(command -v chromium || command -v chromium-browser || command -v google-chrome-stable)
cat > /etc/systemd/system/chromium-remote.service <<EOF
[Unit]
Description=Chromium with CDP on :9223, display :99
After=xvfb.service
Requires=xvfb.service
StartLimitBurst=3
StartLimitInterval=120

[Service]
Type=simple
Environment=DISPLAY=:99
# 启动前杀掉残留的 chromium/chrome 进程，避免 user-data-dir 冲突导致标签页堆叠
ExecStartPre=/usr/bin/pkill -9 -f "(chromium|chrome).*remote-debugging-port=9223" || true
ExecStartPre=/bin/sleep 2
# ⚠️ 严禁添加 --headless 或 --headless=new，否则 noVNC 画面无法显示。
ExecStart=${CHROME_BIN} --no-sandbox --disable-gpu --disable-dev-shm-usage --disable-session-crashed-bubble --restore-last-session=false --remote-debugging-port=9223 --remote-debugging-address=127.0.0.1 --remote-allow-origins=* --user-data-dir=/root/.chromium-remote --no-first-run --no-default-browser-check --window-size=1920,1080 --start-maximized https://www.baidu.com/
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now xvfb.service x11vnc.service novnc.service chromium-remote.service
```

验证（应全部 `active`）：

```bash
systemctl is-active xvfb x11vnc novnc chromium-remote
ss -tlnp | grep -E ':6080|:5900|:9223'
```

> 重启服务器后，Agent 和用户都不需要再手动跑 `start-remote-browser.sh`，整套服务会自动拉起来。

---

**部署和自启已全部完成。现在按顺序执行三步收尾，不可跳过或调换：**

**第一步：打开百度确认** — 参考第七节 CDP 代码，将 `url` 改为 `'https://www.baidu.com/'`，只调 `Page.enable → Page.navigate → sleep(3)`，删掉 `Runtime.enable` 和 `Runtime.evaluate`。

**第二步：先发送核心完成信息** — 按第八节模板先把 noVNC 地址、访问密码、开机自启状态、端口提醒和验证码处理说明发给用户。**这一步必须先发，不能等待截图成功后再发。**

**第三步：最后截图并发送** — 执行 `DISPLAY=:99 import -window root /tmp/remote-browser.png`，再按第八节截图发送方式发送图片。截图是最后一步补充确认；如果截图失败，必须在核心信息已发送后报告失败原因并尝试修复/重试，严禁因为截图失败导致地址和密码没有发出去。

---

## 七、通过 CDP 控制浏览器（参考代码，需要打开网页时使用）

使用 Python 控制已启动的 Chromium：

```bash
python3 - <<'PY'
import json, time, urllib.request
import websocket

url = 'https://example.com'
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
ws = websocket.create_connection(
    page['webSocketDebuggerUrl'],
    header=['Origin: http://127.0.0.1:9223'],
    timeout=20,
)

msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg

call('Page.enable')
call('Runtime.enable')
call('Page.navigate', {'url': url})
time.sleep(3)
res = call('Runtime.evaluate', {
    'expression': '({title: document.title, url: location.href})',
    'returnByValue': True,
})
print(json.dumps(res['result']['result']['value'], ensure_ascii=False, indent=2))
ws.close()
PY
```

如果缺少 websocket 包：

```bash
pip3 install websocket-client --break-system-packages
```

## 八、回复模板

收尾时必须先发送核心完成信息，再把截图作为最后一步发送。严禁因为截图生成或发送失败，导致 noVNC 地址、访问密码等核心信息没有发出去。

### 1. 发送前准备

运行脚本获取 noVNC 地址：

```bash
# 根据环境类型选择 IP（ENV_TYPE 在「零、系统检测」步骤中已设置）
if [ "$ENV_TYPE" = "CLOUD" ]; then
  # 云服务器：优先使用公网 IP
  PUBLIC_IP=$(curl -4 -s https://ifconfig.me 2>/dev/null || curl -4 -s https://api.ipify.org 2>/dev/null || true)
  if [ -n "$PUBLIC_IP" ]; then
    NOVNC_URL="http://${PUBLIC_IP}:6080/vnc.html"
  else
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
  fi
else
  # NAS / 本地 Linux：直接使用内网 IP
  LOCAL_IP=$(hostname -I | awk '{print $1}')
  NOVNC_URL="http://${LOCAL_IP}:6080/vnc.html"
fi
echo "$NOVNC_URL"
echo "ENV_TYPE=$ENV_TYPE"
```

读取访问密码：

```bash
cat /root/.novnc_password
```

### 2. 发送顺序铁律（最高优先级）

1. **先发核心完成信息**：必须先把 noVNC 地址、访问密码、浏览器状态、开机自启状态、端口提醒和验证码处理说明发送给用户。
2. **截图最后发送**：核心信息发出后，再截图并发送图片。截图只是可视化确认，不得阻塞核心信息。
3. **截图失败处理**：如果截图命令失败、图片复制失败或平台发图失败，不允许吞掉核心信息；应先保证用户拿到访问入口，再说明截图失败原因并尝试修复/重试。
4. **禁止只给路径**：截图成功生成后必须通过当前平台的图片/文件能力发送，不能只说“截图在 `/tmp/remote-browser.png`”。
5. **单条回复场景**：如果当前 Agent 只能发一条最终回复，必须把文本核心信息放在前面，截图标签放在最后面。

### 3. Linux 模式回复

```text
远程 Chromium 浏览器已启动：

- noVNC 地址：http://<IP>:6080/vnc.html
- noVNC 访问密码：<读取 /root/.novnc_password>
- 浏览器状态：已自动打开百度页面，截图将作为最后一步补充确认发送
- 开机自启：已配置 systemd，重启后自动拉起
- CDP 地址：仅供 Agent 本机控制，不建议公开
- 如果遇到登录、验证码、滑块，请在 noVNC 页面手动完成，完成后告诉我继续。
```

**根据环境类型追加（Agent 必须严格使用检测到的 ENV_TYPE）：**
- `CLOUD`：请确认云服务器安全组已放行 6080/tcp
- `NAS`：🌐 这是 NAS 局域网地址，请在 NAS 控制面板放行 6080/tcp；通过路由器访问需设置端口转发
- `LOCAL`：🌐 这是本机局域网地址，请确保防火墙已放行 6080/tcp

**🔴 环境误判禁令（最高优先级）：**
- ❌ 对 `NAS`/`LOCAL` 用户**严禁**提「云安全组」「云服务器」「腾讯云」「阿里云」
- ❌ `NAS`/`LOCAL` 环境**严禁**发送公网 IP 的 noVNC 链接（公网 IP 不属于用户，打不开）
- ❌ `CLOUD` 环境**严禁**发送内网 IP 地址给用户
- ❌ **严禁**跳过环境检测步骤直接按云服务器假设来回复

**端口提醒：** `9223/tcp` 是 CDP 调试端口，仅供 Agent 本机使用，不建议对公网开放。

#### 最后一步：截图发送方式

> ⚠️ **铁律：截图必须在核心完成信息发送之后执行和发送。QQ/QQbot 通道截图必须严格遵守以下规则，违反即部署失败。以下方式已经过 QQ 通道实测验证可以正常发送，Agent 必须逐字照做，不得有任何偏离。**

**第一步：生成并复制截图到 QQbot 媒体目录（必须执行 bash 命令，不能只描述）**

```bash
DISPLAY=:99 import -window root /tmp/remote-browser.png
mkdir -p ~/.openclaw/media/qqbot
cp /tmp/remote-browser.png ~/.openclaw/media/qqbot/remote-browser.png
```

**第二步：用 `<qqmedia>` 标签发送（Agent 必须在回复中输出以下标签，一字不差）**

```text
<qqmedia>/root/.openclaw/media/qqbot/remote-browser.png</qqmedia>
```

> 🔴 **禁止事项（违反任何一条视为部署失败）**：
> - 🚫 **严禁**使用 `MEDIA:/tmp/remote-browser.png` 格式发图（QQ 通道不支持，发出去用户看不到）
> - 🚫 **严禁**跳过第一步的 `DISPLAY=:99 import` + `mkdir -p` + `cp` 三步 bash 命令（只文字描述不执行 = 文件不存在 = 发不出）
> - 🚫 **严禁**把 `<qqmedia>` 标签写成其他变体（比如 `<qq-media>`、`<qqmedia>` 路径少写 `/root`、路径用相对路径等）
> - 🚫 **严禁**自行判断"用其他方式也能发"——QQ 通道只认 `<qqmedia>` + 绝对路径这一种方式，没有例外
> - 🚫 **严禁重复发送**：同一张截图**只发一次**，用了 `<qqmedia>` 就不要再同时加 `MEDIA:` 标签，否则用户会收到两张重复图片
>
> ✅ **正确示例（Agent 必须模仿这个模式）**：
> 1. 终端执行：`DISPLAY=:99 import -window root /tmp/remote-browser.png && mkdir -p ~/.openclaw/media/qqbot && cp /tmp/remote-browser.png ~/.openclaw/media/qqbot/remote-browser.png`
> 2. 回复中输出：`<qqmedia>/root/.openclaw/media/qqbot/remote-browser.png</qqmedia>`

**平台分流铁律（最高优先级）：**

- **只有当前会话明确是 QQ / QQbot 通道时，才允许使用 `<qqmedia>` 标签。**
- Telegram / Discord / 邮件 / 终端 / Web UI / 其它平台 **严禁使用 `<qqmedia>`**，否则图片会原样变成文本或发送失败。
- 其它通道必须使用当前平台支持的媒体发送方式；如果 Agent 支持通用媒体标签，优先使用 `MEDIA:/tmp/remote-browser.png`。
- 未知平台不要套 QQ 特例；默认走通用 `MEDIA:` 或该平台官方附件/图片发送能力。

**其他通道（Telegram / Discord / 邮件 / 终端 / Web UI 等）：**

```text
MEDIA:/tmp/remote-browser.png
```

### 4. Windows 模式回复

```text
✅ 浏览器已完全由 AI Agent 控制。

- 浏览器：Edge/Chrome（CDP 端口 9223）
- 你可以在屏幕上看到所有操作，随时手动接管
- 请勿关闭这个浏览器窗口
- 如果遇到登录、验证码、滑块，你直接操作即可，完成后告诉我继续
```

Windows 模式也必须先发送上面的接管完成信息，再把截图作为最后一步发送。截图通过 CDP `Page.captureScreenshot`（完整代码见「十二-3 截图当前页面」）；截图失败不得影响接管完成信息。

## 九、验证清单

### Linux 模式验证

```bash
ss -tlnp | grep -E '6080|5900|9223'
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:6080/vnc.html
curl -s http://127.0.0.1:9223/json/version
```

应满足：

- `6080` 正在监听
- `5900` 正在监听本机 VNC
- `9223` 正在监听 CDP
- `vnc.html` 返回 `200`
- 用户能在浏览器看到远程 Chromium 画面

### Windows 模式验证

```bash
curl -s http://127.0.0.1:9223/json/version
curl -s http://127.0.0.1:9223/json
```

应满足：

- `9223` 正在监听 CDP
- `json/version` 返回浏览器信息
- `json` 返回至少一个 page 类型的标签
- 用户本机屏幕上能看到 Edge/Chrome 浏览器窗口

## 十、常见问题

### Linux 模式

### 1. noVNC 打开空白或连不上

检查进程：

```bash
ps -ef | grep -E 'Xvfb|chromium|x11vnc|websockify' | grep -v grep
ss -tlnp | grep -E '6080|5900|9223'
```

重新运行：

```bash
bash /root/start-remote-browser.sh
```

### 2. 外网打不开 6080

需要同时检查：

- 云服务器安全组是否放行 `6080/tcp`
- 系统防火墙是否放行 `6080/tcp`
- `websockify` 是否监听 `0.0.0.0:6080`

### 3. CDP WebSocket 403

Chromium 启动参数需要包含：

```bash
--remote-allow-origins='*'
```

Python websocket 连接时建议带 Origin：

```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

### 4. 浏览器画面卡住

可清理重启：

```bash
pkill -9 -f chromium || true
pkill -9 -f Xvfb || true
pkill -9 -f x11vnc || true
pkill -9 -f websockify || true
bash /root/start-remote-browser.sh
```

### 5. noVNC 报前端 JS 错误

如果使用 noVNC master 分支出现浏览器兼容问题，固定稳定版本：

```bash
cd /opt/noVNC
git fetch --tags
git checkout v1.6.0
bash /root/start-remote-browser.sh
```

### Windows 模式

### 6. Edge/Chrome 无法以 CDP 模式启动

浏览器可能已经在运行中。需要先关闭所有 Edge/Chrome 窗口，再执行：

```powershell
taskkill /F /IM msedge.exe
taskkill /F /IM chrome.exe
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

### 7. CDP 端口 9223 被占用

检查端口占用并释放：

```powershell
netstat -ano | findstr :9223
taskkill /F /PID <PID>
```

然后重新启动浏览器。

### 8. CDP WebSocket 403 / 连接拒绝

确认启动参数包含 `--remote-allow-origins=*`。如果仍然 403，尝试在连接时带 Origin header：

```python
websocket.create_connection(ws_url, header=['Origin: http://127.0.0.1:9223'])
```

## 十一、重要原则

> ⚠️ 部署后，Agent 所有浏览器操作必须通过 CDP（`127.0.0.1:9223`）控制本技能部署的浏览器——Linux 下为 noVNC 中 `:99` 上的 Chromium，Windows 下为用户本机 Edge/Chrome。**严禁给 Chromium 添加 `--headless` 或 `--headless=new` 启动参数**，否则 noVNC 画面无法正常显示。**禁止使用 Agent 内置 headless 浏览器或其他实例**，否则用户与 Agent 画面不同频，无法协作处理验证码。唯一例外：用户明确要求使用其他浏览器。

## 十二、Windows 系统：远程调试 CDP 控制 Edge/Chrome

当「零、系统检测」判断为 Windows 时，走以下流程。**Windows 模式下无需安装任何依赖，直接利用系统自带的 Edge 或 Chrome 浏览器。**

### 启动流程

**Agent 必须优先自动尝试启动浏览器**，失败后才让用户手动执行。

#### 1. 自动启动（Agent 执行）

Agent 先尝试启动 Edge，失败则回退到 Chrome：

```powershell
# 优先尝试 Edge
start msedge --remote-debugging-port=9223 --remote-allow-origins=*
```

```powershell
# Edge 不可用时尝试 Chrome
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

如果两个命令都执行失败（浏览器未安装、权限不足等），才告诉用户手动执行以下命令：

```text
请以管理员身份打开 PowerShell 或 CMD，执行以下命令：

Edge：
start msedge --remote-debugging-port=9223 --remote-allow-origins=*

或 Chrome：
start chrome --remote-debugging-port=9223 --remote-allow-origins=*
```

#### 2. 验证 CDP 连通性

```bash
curl -s http://127.0.0.1:9223/json/version
```

#### 3. 截图当前页面

验证连通后，通过 CDP 对当前默认页面（新标签页或浏览器主页）截图。**Windows 模式不需要额外导航到百度页面**，直接截取浏览器当前画面即可。

```bash
# 获取当前页面
curl -s http://127.0.0.1:9223/json
# 通过 CDP 截取页面截图，保存为 PNG
python3 - <<'PY'
import json, base64, urllib.request
tabs = json.load(urllib.request.urlopen('http://127.0.0.1:9223/json'))
page = next(t for t in tabs if t.get('type') == 'page')
import websocket
ws = websocket.create_connection(page['webSocketDebuggerUrl'], header=['Origin: http://127.0.0.1:9223'], timeout=20)
msg_id = 0
def call(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == msg_id:
            return msg
call('Page.enable')
res = call('Page.captureScreenshot', {'format': 'png'})
with open('/tmp/browser_screenshot.png', 'wb') as f:
    f.write(base64.b64decode(res['result']['data']))
print('截图已保存: /tmp/browser_screenshot.png')
ws.close()
PY
```

截图生成后，将截图作为最后一步通过 MEDIA 发送给用户；如果是 QQ/QQbot 通道，应使用「八」中的 `<qqmedia>` 规则。

#### 4. 完成提醒

按「八-4」Windows 回复模板**先发送接管完成信息**，然后执行「十二-3」截图并作为最后一步发送。截图失败不得阻塞接管完成信息。

### Windows 模式后续使用

接管完成后，Agent 后续所有浏览器操作（打开网页、点击、输入、截图等）均通过 `127.0.0.1:9223` 的 CDP 接口控制这个浏览器实例。用户在本机屏幕上可实时看到所有操作，遇到登录、验证码时可随时手动介入。
