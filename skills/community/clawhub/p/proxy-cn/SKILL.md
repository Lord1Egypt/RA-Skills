---
name: proxy-cn
description: >
  在中国大陆或受限网络环境下，为访问 GitHub、OpenAI、npm、PyPI、Docker Hub 等境外服务自动或按需注入
  http_proxy / https_proxy / ALL_PROXY（本地 SOCKS5 + HTTP 端口）。
  在用户需要执行 curl、git、npm、pip、docker pull 等可能出网的命令时使用；
  也可由用户明确要求「走代理访问外网」时启用。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["bash"] },
        "install": [],
      },
  }
---

# 外网智能代理（proxy-cn）

在**本机已运行** Clash / V2Ray / 类似客户端（常见本地端口：HTTP `10809`、SOCKS5 `10808`）的前提下，用脚本为单次命令或当前 shell **按需注入**代理环境变量，避免全局长开代理带来的内网/公司流量误走代理。

## 平台支持

| 环境 | 推荐入口 | 说明 |
|------|----------|------|
| **macOS** | `bash` + `proxy.sh` / `source proxy-env.sh` | 与 Linux 相同，需 Bash（系统自带或 Homebrew）。 |
| **Linux** | `bash` + `proxy.sh` / `source proxy-env.sh` | 需已安装 `bash`；Alpine 等若只有 `sh` 请 `apk add bash`。 |
| **Windows（PowerShell）** | `proxy.ps1` / 点源 `proxy-env.ps1` | 原生终端用 **PowerShell 5.1+**（含 Windows PowerShell 与 PowerShell 7 `pwsh`）。首次若被策略拦截，可用 `pwsh -ExecutionPolicy Bypass -File proxy.ps1 ...`。 |
| **Windows（Git Bash / MSYS2）** | 与 Linux 相同，使用 `proxy.sh` | 路径用 Unix 风格，如 `bash /c/path/to/proxy-cn/proxy.sh curl ...`。 |
| **WSL** | 与 Linux 相同 | 在 WSL 内用 `bash` 脚本；代理端口指向 **WSL 可访问的本机 IP**（见下）。 |

**WSL2**：Windows 主机上的 `127.0.0.1:10809` 在部分发行版中需通过 **Windows 主机 IP** 访问，可设置 `PROXY_HTTP_HOST`、`PROXY_SOCKS_HOST` 为 `$(grep nameserver /etc/resolv.conf | awk '{print $2}'):端口` 或用户文档中的 WSL 代理转发地址。

**经典 CMD.exe**：不支持直接运行 `.ps1`；可在 CMD 中执行 `powershell -NoProfile -File "<技能目录>\proxy.ps1" ...`，或手动 `set HTTP_PROXY=http://127.0.0.1:10809` 等（与 `proxy-env.ps1` 导出变量一致）。

**NO_PROXY 与 CIDR**：脚本默认在 `no_proxy` 中带私网 CIDR；个别旧版 Windows 工具对 CIDR 支持不完整。若遇异常，可设 `PROXY_AUTO_NO_LOCAL=0`（Bash）或 `$env:PROXY_AUTO_NO_LOCAL = "0"`（PowerShell）再运行，或自行精简 `no_proxy` 列表。

## 何时使用本技能

- 用户提到：访问 GitHub / OpenAI / HuggingFace / npm / PyPI / Docker Hub **超时、TLS 失败、Connection reset**
- 用户要求：**临时走代理**完成 `curl`、`git clone`、`npm install`、`pip install`、`docker pull`
- 用户环境：中国大陆或企业网络对外网有限制

## 何时不要使用

- 访问**纯内网**、公司 VPN 内资源：不要设置代理，或确保 `no_proxy` 已包含内网段（脚本已默认写入常见私网 CIDR）
- 用户**未安装**本地代理客户端：应先引导用户启动 Clash 等，再使用本技能
- **敏感凭据**：代理仅走本机环回地址，勿把 token 发给第三方；仍遵守各服务安全策略

## 文件说明（技能根目录）

| 文件 | 作用 |
|------|------|
| `proxy.sh` | **Bash（macOS / Linux / Git Bash / WSL）**：对「单条命令」做域名启发式检测，匹配则注入代理并 `exec` 子进程 |
| `proxy-env.sh` | **Bash**：`source` 后在当前 shell 中长期生效（无域名检测） |
| `proxy.ps1` | **Windows PowerShell**：与 `proxy.sh` 等价逻辑 |
| `proxy-env.ps1` | **PowerShell**：点源 `. .\proxy-env.ps1` 后在当前会话生效 |

默认假设本机代理：

- HTTP(S) 代理：`127.0.0.1:10809`
- SOCKS5：`127.0.0.1:10808`

若用户端口不同，在命令前设置 `PROXY_HTTP_HOST`、`PROXY_SOCKS_HOST`（见下）。

## 工作流（Agent 操作指引）

1. **确认**用户本机代理已监听（可建议用户执行 `curl -sI --connect-timeout 2 http://127.0.0.1:10809` 或查看 Clash 端口说明；Windows 可用 `curl.exe`）。
2. **单次命令**优先使用包装器（将 `<技能目录>` 换为实际路径）。

   **Bash（macOS / Linux / Git Bash / WSL）：**

   ```bash
   bash "<技能目录>/proxy.sh" curl -sI https://api.github.com
   ```

   **PowerShell（Windows）：**

   ```powershell
   Set-Location "<技能目录>"
   .\proxy.ps1 curl.exe -sI https://api.github.com
   ```

3. 若参数里**没有明显 URL**（例如仅 `npm install`），启发式可能**不会**自动开代理，此时使用强制：

   ```bash
   PROXY_AUTO_FORCE=1 bash "<技能目录>/proxy.sh" npm install
   ```

   ```powershell
   $env:PROXY_AUTO_FORCE = "1"; & "<技能目录>\proxy.ps1" npm install
   ```

4. 需要**整段会话**走代理时：

   ```bash
   source "<技能目录>/proxy-env.sh"
   ```

   ```powershell
   . "<技能目录>\proxy-env.ps1"
   ```

5. 执行完后，新开终端或清除变量：Bash 用 `unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY ALL_PROXY all_proxy`；PowerShell 用 `Remove-Item Env:\HTTP_PROXY,Env:\HTTPS_PROXY,...` 或对上述变量逐个 `$env:HTTP_PROXY = $null`（`proxy-env` 脚本未自动清除）。

## 环境变量（可选）

Bash 与 PowerShell 使用**同名**环境变量（PowerShell 中通过 `$env:PROXY_AUTO_FORCE = "1"` 设置）。

| 变量 | 含义 | 默认 |
|------|------|------|
| `PROXY_AUTO_FORCE` | 设为 `1` 时强制为本次命令设置代理 | 未设置 |
| `PROXY_HTTP_HOST` | HTTP 代理 `host:port` | `127.0.0.1:10809` |
| `PROXY_SOCKS_HOST` | SOCKS5 `host:port` | `127.0.0.1:10808` |
| `PROXY_AUTO_NO_LOCAL` | 设为 `0` 可不导出 `no_proxy` | `1` |

## 启发式匹配说明（proxy.sh / proxy.ps1）

对**所有参数**做子串匹配（不区分大小写），命中下列模式之一则自动开代理（节选）：`github.com`、`googleapis.com`、`openai.com`、`anthropic.com`、`npmjs.org`、`pypi.org`、`docker.io`、`ghcr.io`、`huggingface.co`、`crates.io` 等。

**限制**：若 URL 写在配置文件里而不在命令行参数中，脚本**无法**检测，请用 `PROXY_AUTO_FORCE=1`。

## 验证命令

```bash
# 经 SOCKS 直连探测（不依赖包装脚本；Linux / macOS / Git Bash）
curl -sI --connect-timeout 5 --socks5 127.0.0.1:10808 https://www.google.com

# 经包装器（会设环境变量后执行 curl）
bash proxy.sh curl -sI https://api.github.com
```

```powershell
# Windows：建议显式使用 curl.exe，避免与 Invoke-WebRequest 别名冲突
curl.exe -sI --connect-timeout 5 --socks5 127.0.0.1:10808 https://www.google.com
.\proxy.ps1 curl.exe -sI https://api.github.com
```

## 与 OpenClaw / 容器路径

若部署在容器中，技能路径可能是 `/root/.openclaw/skills/proxy-cn/`，请将上文 `<技能目录>` 替换为实际绝对路径。

## 安全与合规

- 代理出口节点与日志策略由用户本地客户端决定，本技能**仅设置环境变量**。
- 遵守当地法律法规与用户公司网络政策；不得用于绕过明确禁止访问的资源。
