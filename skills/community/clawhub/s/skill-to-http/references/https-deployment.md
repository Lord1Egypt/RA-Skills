# HTTPS 部署指南

针对 `skill-to-http` 的 HTTPS 部署，覆盖三种典型场景。

---
> **路径说明**：本文档用 `<HTTP_ROOT>` 表示证书根目录。
> - OpenClaw 环境默认是 `~/.openclaw/workspace/.http/`（跟 PVC 持久化）
> - 非 OpenClaw 环境兜底 `~/.http/`
> - 通过 `OPENCLAW_HTTP_ROOT` 环境变量可显式覆盖
> - 用 `python3 server.py cert --cert-action info` 查看实际路径

## 场景 1：内网部署（最常见的使用场景）

**推荐**：自签证书 + 内网 IP 直接访问

### 一键流程

```bash
# 首次：跑 init wizard，选「自签证书」（默认）
cd /path/to/skill-to-http/scripts
python3 server.py   # 触发 init wizard → 自动生成证书到 <HTTP_ROOT>/certs/

# 后续验证
python3 server.py cert --cert-action info
# → 显示 SAN（本机 IP 已自动嗅探）、到期时间
```

### 客户端如何信任自签证书

```bash
# curl
curl --cacert <HTTP_ROOT>/certs/server.crt https://10.40.x.x:8080/health

# Python requests
import requests
requests.get('https://10.40.x.x:8080/health', verify='<HTTP_ROOT>/certs/server.crt')

# 浏览器
# - macOS: 双击 server.crt → 钥匙串 → 改为「始终信任」
# - Linux: cp <HTTP_ROOT>/certs/server.crt /usr/local/share/ca-certificates/ && update-ca-certificates
# - Windows: 双击 → 安装到「受信任的根证书颁发机构」
```

---

## 场景 2：导入已有证书（公司颁发 / mkcert / Let's Encrypt）

如果你已有合法证书（如公司内部 CA 签发的、或 mkcert 生成的本机受信证书），直接导入：

```bash
python3 server.py cert --cert-action import \
    --cert-src /path/to/your.crt \
    --key-src /path/to/your.key
```

导入后证书会被复制到 `<HTTP_ROOT>/certs/server.crt`（权限 644）和 `<HTTP_ROOT>/certs/server.key`（权限 600）。

### mkcert 推荐（开发环境本机受信）

```bash
# 安装 mkcert（macOS）
brew install mkcert nss
mkcert -install   # 自动信任本机 CA

# 生成证书（含本机 IP 和 localhost）
mkcert localhost 127.0.0.1 10.40.69.146 your-host.local
# → 生成 localhost+3.pem 和 localhost+3-key.pem

# 导入
python3 server.py cert --cert-action import \
    --cert-src localhost+3.pem \
    --key-src localhost+3-key.pem
```

**优点**：浏览器和 curl 都开箱信任（无需 `-k` 或 `--cacert`），适合频繁本机开发。

---

## 场景 3：公网部署 + Let's Encrypt（少数场景）

**前提**：
- 有公网域名（如 `api.yourdomain.com`）
- DNS A 记录指向服务器公网 IP
- 80 端口可被公网访问（用于 HTTP-01 ACME 验证）

### 安装 certbot

```bash
sudo apt install certbot                    # Debian/Ubuntu
sudo yum install certbot                    # CentOS/RHEL
brew install certbot                        # macOS
```

### 申请证书

```bash
# 方案 A：standalone 模式（服务停掉时跑）
sudo certbot certonly --standalone \
    -d api.yourdomain.com \
    --agree-tos --email you@yourdomain.com -n

# 证书路径：
#   /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem
#   /etc/letsencrypt/live/api.yourdomain.com/privkey.pem

# 方案 B：webroot 模式（服务用 80 端口时不停服）
sudo certbot certonly --webroot \
    -w /var/www/html \
    -d api.yourdomain.com
```

### 导入 LE 证书到 skill-to-http

```bash
python3 server.py cert --cert-action import \
    --cert-src /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem \
    --key-src /etc/letsencrypt/live/api.yourdomain.com/privkey.pem
```

### 自动续期（Let's Encrypt 证书 90 天有效）

```bash
# cron 每天检查一次（certbot 自动跳过未到期的）
echo "0 3 * * * certbot renew --quiet --post-hook 'cd /path/to/skill-to-http/scripts && python3 server.py cert --cert-action import --cert-src /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem --key-src /etc/letsencrypt/live/api.yourdomain.com/privkey.pem && python3 server.py restart'" | sudo crontab -
```

---

## 升级现有 HTTP 服务

如果你的 `skill-to-http` 已经以 HTTP 模式跑着，一键升级到 HTTPS：

```bash
python3 server.py upgrade-to-https
# → 停服 → 改 config.json 的 tls_enabled=true → 生成证书 → 提示重启
```

升级后客户端调用方式：
- 旧：`http://10.40.x.x:8080/...`
- 新：`https://10.40.x.x:8080/...` + `X-API-Key` header

---

## 证书自检（doctor）

```bash
python3 server.py doctor          # 全面检查（含证书）
python3 server.py doctor --fix    # 自动续期 30 天内过期的证书
```

doctor 会检查：
- ✅ 证书文件存在
- ⚠️ 30 天内过期 → 提示续期（可 `--fix` 自动续）
- ⚠️ 本机 IP 不在 SAN 中（IP 变化常见于 K8s pod 漂移）→ 提示重新生成

---

## 安全提示

- 证书私钥 `<HTTP_ROOT>/certs/server.key` 权限必须 0600（自动设置）
- API Key 强制配合 HTTPS 使用，单独 HTTPS 没鉴权 = 信道加密但任何人能调
- 不要把 `<HTTP_ROOT>/certs/server.crt` 推到 git（已 gitignore；公网部署用 LE 证书）
- 内网 IP HTTPS 不能完全防御中间人（自签证书需客户端预先信任），但能挡掉明文嗅探
