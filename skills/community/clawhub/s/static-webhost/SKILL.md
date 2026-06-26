---
name: static-webhost
description: >
  Deploy static web pages and apps via Caddy or Nginx (auto-detected). Use when:
  通过 Caddy 或 Nginx 部署静态网页和应用（自动检测）。使用场景：
  (1) User asks to create a web page, demo, or static site and make it accessible / 用户要求创建网页并可访问
  (2) User asks to host/deploy HTML, JS, CSS files / 用户要求托管部署静态文件
  (3) User says "做个网页"、"部署一下"、"让我能访问"
  (4) Need to serve any static content over HTTP / 需要通过 HTTP 提供任何静态内容。
  Supports both Caddy and Nginx — auto-detects which is installed and running.
  同时支持 Caddy 和 Nginx，自动检测当前系统安装的 Web 服务器。
  NOT for / 不适用于：dynamic backends, APIs, or reverse proxy configuration.
  
  ⚠️ **权限声明 / Privilege Requirements:** 此 skill 需要 **sudo/root 权限** 才能执行系统级操作（写入 /var/www/html、修改 Web 服务器配置、重启服务）。
---

# Static WebHost

**Author:** [Serein-213](https://github.com/Serein-213)

Deploy static files to Caddy or Nginx. Auto-detects which server is available.

---

## ⚠️ 安全警告 / Security Warning

**此 skill 执行的操作需要 elevated privileges（sudo/root），属于高危操作。**

### 权限需求
- **写入系统目录:** `/var/www/html/`（Web 根目录）
- **修改配置文件:** `/etc/nginx/` 或 `/etc/caddy/Caddyfile`
- **系统服务管理:** `systemctl reload nginx/caddy`
- **包管理器操作:** `pacman -S` / `apt install`（如需要安装 Web 服务器）

### 使用前必须确认
1. ✅ **用户明确授权** — 不要自动执行，必须先向用户说明并获得确认
2. ✅ **备份现有配置** — 修改 Web 服务器配置前务必备份
3. ✅ **测试环境优先** — 首次使用建议在测试环境验证
4. ✅ **了解回滚方案** — 知道如何恢复配置（备份还原、服务重启）

### 备份命令（执行任何修改前）
```bash
# Nginx 配置备份
sudo cp -r /etc/nginx /etc/nginx.backup.$(date +%Y%m%d_%H%M%S)

# Caddy 配置备份  
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup.$(date +%Y%m%d_%H%M%S)

# Web 根目录备份（如已有内容）
sudo cp -r /var/www/html /var/www/html.backup.$(date +%Y%m%d_%H%M%S)
```

### 替代方案（无需 root）
如果不需要系统级部署，考虑：
- 用户级静态服务器：`python3 -m http.server 8080`
- Node.js: `npx serve ./public`
- Docker 容器化部署（隔离环境）

---

## Step 0: Detect Web Server

Before deploying, detect which web server is installed and running:

```bash
# Check Caddy
command -v caddy && systemctl is-active caddy 2>/dev/null

# Check Nginx
command -v nginx && systemctl is-active nginx 2>/dev/null
```

**Priority:** Caddy (if both are running) > Nginx > Neither (prompt user to install one).

---

## Caddy Deployment

### Setup (first time only)

Ensure Caddyfile has a static file block. Add if missing:

```
:80 {
    handle_path /r/* {
        file_server {
            root /var/www/html
        }
    }
}
```

Then `systemctl reload caddy`.

### Deploy

```bash
mkdir -p /var/www/html/<project-name>
cp -r <source-files> /var/www/html/<project-name>/
```

**URL:** `http://<ip>/r/<project-name>/index.html`

No reload needed — files are served instantly.

---

## Nginx Deployment

### Setup (first time only)

Create a location block in the Nginx site config (e.g. `/etc/nginx/sites-available/default` or `/etc/nginx/conf.d/static.conf`):

```nginx
server {
    listen 80;
    # ... existing config ...

    location /r/ {
        alias /var/www/html/;
        autoindex off;
        try_files $uri $uri/ =404;
    }
}
```

Then `nginx -t && systemctl reload nginx`.

### Deploy

```bash
mkdir -p /var/www/html/<project-name>
cp -r <source-files> /var/www/html/<project-name>/
```

**URL:** `http://<ip>/r/<project-name>/index.html`

No reload needed — files are served instantly once placed in web root.

---

## Common Steps (both servers)

### Get access URL

```bash
# Tailscale
tailscale ip -4 2>/dev/null

# Or local IP
hostname -I | awk '{print $1}'
```

### Verify

```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:80/r/<project-name>/index.html
```

Expect `200`.

---

## Notes

- **Web root:** `/var/www/html/` (shared convention for both Caddy and Nginx)
- **URL pattern:** `http://<ip>/r/<subdir>/` (consistent across both servers)
- Files are served instantly — no reload needed after placing files
- For subdirectories, ensure `index.html` exists
- Large files (>50MB) should be considered carefully for disk usage
- If neither Caddy nor Nginx is installed, suggest `pacman -S caddy` / `apt install caddy` / `apt install nginx`
