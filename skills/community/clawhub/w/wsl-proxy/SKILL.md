---
name: wsl-proxy
description: WSL2 HTTP proxy setup via Windows host. Automatically detects proxy running on Windows (Clash/V2Ray/SS/Surge etc.) and configures WSL2 environment variables. Trigger when users need to access blocked websites, configure VPN/proxy, or enable external network access from WSL2.
---

# WSL2 Proxy — WSL2 代理上网方案

此机器为 WSL2 + Windows 代理工具环境。Skill 会自动扫描宿主机上运行的 HTTP 代理端口，无需用户指定端口号或代理地址。

技能安装路径：`skills/wsl-proxy/`
脚本目录：`skills/wsl-proxy/scripts/`

## 快速上手

### 1️⃣ 检测代理

```bash
bash skills/wsl-proxy/scripts/detect_proxy.sh
```

自动扫描宿主机常见端口（7890, 7897, 1080, 10808, 10809, 8888, 8080, 9090, 6152 等），找到可达的 HTTP 代理。

### 2️⃣ 设置代理（当前 shell）

```bash
eval "$(bash skills/wsl-proxy/scripts/setup_proxy.sh)"
```

自动检测 + 设置环境变量，一步到位。

### 3️⃣ 检查完整状态

```bash
bash skills/wsl-proxy/scripts/check_proxy.sh
```

显示端口检测结果、环境变量、外网连通性。

### 4️⃣ 直接使用（不依赖脚本）

```bash
HOST_IP=$(ip route show default | awk '{print $3}')
for PORT in 7890 7897 1080 10808 10809 8888 8080 9090; do
    timeout 1 bash -c "echo > /dev/tcp/${HOST_IP}/${PORT}" 2>/dev/null && echo "Port ${PORT} reachable" && break
done
export http_proxy="http://${HOST_IP}:${PORT}"
export https_proxy="http://${HOST_IP}:${PORT}"
```

### 5️⃣ 验证

```bash
curl -s -o /dev/null -w '%{http_code}' https://www.google.com
# 200 → OK
```

### 6️⃣ 清除代理

```bash
eval "$(bash skills/wsl-proxy/scripts/unset_proxy.sh)"
```

## 永久生效

追加到 `~/.bashrc` 或 `~/.zshrc`：

```bash
export host_ip=$(ip route show default | awk '{print $3}')
export http_proxy="http://${host_ip}:${PORT}"
export https_proxy="http://${host_ip}:${PORT}"
```

## 常见代理端口参考

| 工具 | 默认端口 | 协议 |
|------|----------|------|
| Clash / Clash Verge | 7890, 7897 | HTTP |
| V2Ray / Xray | 10808, 10809 | HTTP/SOCKS |
| Shadowsocks | 1080 | SOCKS5 |
| Surge | 6152 | HTTP |
| Squid | 3128 | HTTP |
| Charles | 8888 | HTTP |

## 故障排查

- **端口全扫不到** → Windows 上代理工具未启动，检查任务栏图标
- **端口可达但 403** → 代理工具的分流规则未包含目标域名
- **Git 不走代理** → `git config --global http.proxy http://${host_ip}:${PORT}`
- **部分程序不走代理** → 某些程序不读 `http_proxy`，需单独配置

## 架构说明

```
┌────────────────────────┐
│   Windows Host          │
│   Clash/V2Ray/SS etc.   │  ← HTTP proxy (auto-detected port)
└────────┬───────────────┘
         │ 172.x.x.1 (gateway IP)
         ▼
┌────────────────────────┐
│   WSL2 Linux            │
│   curl → http_proxy     │  ← via gateway IP
└────────────────────────┘
```
