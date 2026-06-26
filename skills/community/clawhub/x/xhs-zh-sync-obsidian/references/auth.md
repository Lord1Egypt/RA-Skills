# CookieCloud 认证

CookieCloud 是推荐登录态来源。小红书和知乎经常需要真实浏览器 Cookie；定时任务里用 CookieCloud 比手填原始 Cookie 更稳定。

## 服务端部署方式

首次安装时必须先问用户 CookieCloud 服务端部署在哪里，不要直接假设默认值：

- 本机安装：需要确认本机有 Docker / Docker Compose。
- 非本机安装：需要用户提供服务端地址、UUID 和 Password。

本机 Docker 服务端地址通常是：

```bash
COOKIECLOUD_SERVER_URL=http://127.0.0.1:8088
```

如果 CookieCloud 服务端不在本机，必须让用户提供服务端地址，并写入：

```bash
COOKIECLOUD_SERVER_URL=http://<服务器IP或域名>:8088
COOKIECLOUD_UUID=<uuid>
COOKIECLOUD_PASSWORD=<password>
COOKIECLOUDUUID=<uuid>
COOKIECLOUDPASSWORD=<password>
```

可参考本技能内置模板：

```bash
cp assets/docker-compose.cookiecloud.yml docker-compose.yml
docker compose up -d cookiecloud
```

该模板来自 hc-tec collection skills 的 compose 思路，只保留本技能需要的 CookieCloud 服务：

```yaml
services:
  cookiecloud:
    image: easychen/cookiecloud:latest
    ports:
      - "8088:8088"
    volumes:
      - ./.cookiecloud-data:/data/api/data
    restart: unless-stopped
```

## 自动生成插件凭据

首次运行：

```bash
python scripts/setup.py --init
```

如果 CookieCloud 服务端不是本机：

```bash
python scripts/setup.py --init --cookiecloud-server-url http://<服务器IP>:8088
```

脚本会生成随机：

- `COOKIECLOUD_UUID`
- `COOKIECLOUD_PASSWORD`

并写入：

```text
~/.config/social-favorites-to-obsidian/cookiecloud.env
```

同时会在终端打印这组值。用户需要在自己常用浏览器里安装 CookieCloud 插件，然后填写：

- 服务器地址：`http://<运行 CookieCloud 的机器 IP>:8088`
- UUID：脚本生成的 `COOKIECLOUD_UUID`
- 密码：脚本生成的 `COOKIECLOUD_PASSWORD`

如果选择本机安装 CookieCloud 服务端，也必须做这一步。插件运行在用户常用 Chrome 浏览器里，服务器地址要填写该浏览器能访问到的地址：同机浏览器可用 `http://127.0.0.1:8088`，其它设备浏览器要用运行 CookieCloud 服务端机器的局域网 IP 和端口。

注意：浏览器插件不一定安装在运行 OpenClaw/技能的机器上。只要插件能访问 CookieCloud 服务端地址即可。

## 插件同步要求

在浏览器里登录并同步这些域名：

- `xiaohongshu.com`
- `zhihu.com`

同步后运行：

```bash
python scripts/setup.py --doctor
python scripts/sync.py --platform xhs
python scripts/sync.py --platform zhihu
```

如果出现 403、验证码、空数据或无法读取笔记，先刷新浏览器登录状态并重新同步 CookieCloud。

## 原始 Cookie 兜底

没有 CookieCloud 时，可以在 `cookiecloud.env` 里手动填：

```bash
XIAOHONGSHU_COOKIE='a=...; web_session=...'
ZHIHU_COOKIE='z_c0=...; ...'
```

不推荐把原始 Cookie 用于公开说明、日志或示例输出。
