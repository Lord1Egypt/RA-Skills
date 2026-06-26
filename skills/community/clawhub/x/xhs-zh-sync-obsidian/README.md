# Social Favorites to Obsidian

把小红书和知乎收藏增量同步到 Obsidian 的 Codex/OpenClaw 技能。

这个技能负责安装引导、CookieCloud 登录态配置、第三方抓取技能安装、分类规则、图片下载压缩、Markdown 导出，以及可选的 OpenClaw 定时任务生成。小红书和知乎的实际抓取依赖 hctec 第三方技能。

## 功能

- 增量抓取小红书收藏和知乎收藏。
- 导出为 Obsidian Markdown。
- 下载正文图片，压缩为质量 70 的 WebP。
- 图片保存到 vault 的 `_assets/<platform>/<id>/`。
- Markdown 中使用 Obsidian wiki 图片引用：`![[_assets/...]]`。
- 支持本地 vault、已有 vault、官方 Obsidian Sync。
- 支持生成 OpenClaw cron 定时任务配置。
- 使用 CookieCloud 管理浏览器登录态。

## 基础依赖

需要满足下面任一 CookieCloud 条件：

- 本机有 Docker / Docker Compose，可以在本机运行 CookieCloud 服务端；并且你的常用 PC 浏览器就在本机，或可以通过网络访问到这台机器的 `8088` 端口。
- 或者你已经自行安装并运行了 CookieCloud 服务端 （ https://github.com/easychen/CookieCloud ），可以提供服务端地址、UUID 和 Password。

需要满足下面任一 Obsidian 同步条件：

- 有 Obsidian 官方 Sync 服务，用 `obsidian-headless` / `ob sync` 自动同步。
- 或者有自建同步方案，例如 Syncthing、Git、网盘等，本技能只写入本地 vault 目录。
- 或者只想先导出到本地 vault，不立即同步。

还需要：

- Python 3.10+
- Node.js / npm，只有使用官方 Obsidian Sync 时需要
- Chrome 或 Chromium，Playwright 会自动安装浏览器运行环境
- 能访问 GitHub，用于安装 hctec 第三方抓取技能

## 安装

### 方式一：npx 安装

可以运行：

```bash
npx @sunfang2cn/social-favorites-to-obsidian install.py
```

安装脚本会交互式询问：

- CookieCloud 是本机安装还是使用已有服务端。
- Obsidian vault 是自动创建、使用已有目录，还是配置官方 Sync。
- 是否初始化默认分类规则。
- 如果检测到 OpenClaw，是否生成 cron 定时任务配置。

### 方式二：让 LLM/Codex 安装

你也可以告诉 Openclaw/Codex等：

```text
安装并配置 GitHub 上 sunfang1cn/social-favorites-to-obsidian 这个技能。
```

LLM/Codex 会读取技能内的 `SKILL.md` 和 `references/first-install.md`，按交互式安装流程完成初始化。

### 方式三：本地手动运行

克隆或下载仓库后，在仓库根目录运行：

```bash
python install.py
```

如果需要显式脚本路径：

```bash
python scripts/interactive_install.py
```

## 首次配置要点

### CookieCloud

如果选择本机安装 CookieCloud，安装器会：

- 使用 `assets/docker-compose.cookiecloud.yml` 启动 CookieCloud 服务端。
- 自动生成 `COOKIECLOUD_UUID` 和 `COOKIECLOUD_PASSWORD`。
- 写入 `~/.config/social-favorites-to-obsidian/cookiecloud.env`。

安装器结束后，你还需要在自己常用的 Chrome 浏览器中安装 CookieCloud 插件，并填写：

- 服务器地址：同机浏览器可用 `http://127.0.0.1:8088`；其它设备浏览器要用 `http://<本机局域网IP>:8088`。
- UUID：安装器生成的 `COOKIECLOUD_UUID`。
- Password：安装器生成的 `COOKIECLOUD_PASSWORD`。

然后在该 Chrome 浏览器中登录：

- `xiaohongshu.com`
- `zhihu.com`

最后执行 CookieCloud 插件同步。

### Obsidian

安装器会让你选择：

- 自动创建本地 vault，并使用官方 Obsidian Sync。
- 自动创建本地 vault，但只做本地导出。
- 使用已有本地 vault 目录。

如果选择官方 Obsidian Sync，需要提供或交互输入：

- Obsidian 官方账号。
- Obsidian 官方账号密码。
- 远程 vault 名字或 ID。
- 如果启用了端到端加密，还需要 Sync 加密密码。

## 常用命令

检查安装状态：

```bash
python scripts/setup.py --status --json
python scripts/setup.py --doctor
```

抓取并导出：

```bash
python scripts/sync.py --platform xhs
python scripts/sync.py --platform zhihu
python scripts/export_obsidian.py --platform all --incremental
```

生成 OpenClaw cron 配置：

```bash
python scripts/install_cron.py --platform xhs --time 06:00 --print
python scripts/install_cron.py --platform zhihu --time 05:00 --print
```

