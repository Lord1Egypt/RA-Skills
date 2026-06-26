# proxy-cn（外网智能代理）

在本地已有 HTTP/SOCKS 代理（如 Clash 默认 `10809` / `10808`）时，为单条命令或当前 shell 注入 `http_proxy`、`https_proxy`、`ALL_PROXY`。

| 平台 | 单次命令（启发式） | 当前会话（无检测） |
|------|-------------------|-------------------|
| **macOS / Linux / WSL / Git Bash** | `proxy.sh` | `source proxy-env.sh` |
| **Windows PowerShell** | `proxy.ps1` | `. .\proxy-env.ps1`（点源） |

详细触发条件、环境变量、WSL 代理地址与 Agent 指引见 **`SKILL.md`**。

## 快速示例（Bash）

```bash
cd /path/to/proxy-cn
chmod +x proxy.sh proxy-env.sh

./proxy.sh curl -sI https://api.github.com
PROXY_AUTO_FORCE=1 ./proxy.sh npm install lodash

source ./proxy-env.sh
curl -sI https://google.com
```

## 快速示例（Windows PowerShell）

```powershell
Set-Location C:\path\to\proxy-cn
.\proxy.ps1 curl.exe -sI https://api.github.com
$env:PROXY_AUTO_FORCE = "1"; .\proxy.ps1 npm install lodash
. .\proxy-env.ps1
```

若提示无法加载脚本，可先执行：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，或使用 `pwsh -ExecutionPolicy Bypass -File proxy.ps1 ...`。

## 要求

- **Bash 路线**：已安装 `bash`（macOS / Linux / Git Bash / MSYS2 / WSL 均适用）
- **PowerShell 路线**：Windows PowerShell 5.1+ 或 PowerShell 7（`pwsh`）
- 本机代理客户端已启动，且端口与 `PROXY_HTTP_HOST` / `PROXY_SOCKS_HOST` 一致
