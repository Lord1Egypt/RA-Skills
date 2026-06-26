---
name: social-favorites-to-obsidian
description: 将小红书和知乎收藏增量同步到 Obsidian：依赖 hctec-* 抓取技能，使用 CookieCloud 登录态，支持首次安装、依赖检查、分类规则、Markdown 导出和 OpenClaw 定时任务生成。当用户要安装、配置、诊断、归档、分类、导出或定时同步社交平台收藏到 Obsidian 时使用。
---

# Social Favorites to Obsidian

这个技能把“小红书/知乎收藏 -> 抓取 -> 分类 -> Obsidian 导出 -> 定时同步”做成可发布的安装流程。平台抓取由 hctec 原子技能负责，本技能负责安装引导、配置、状态、分类、导出和 cron 生成。

## 工作流

1. 首次安装时不要直接使用默认值开跑。先读取 `references/first-install.md`，并向用户确认这些可选项：
   - CookieCloud 服务端：本机 Docker 安装，还是使用已有远程服务端；远程服务端需要地址、UUID 和 Password。
   - Obsidian vault：自动创建并使用官方 Obsidian Sync，自动创建但只本地导出，还是使用已有本地 vault 目录。
   - 官方 Obsidian Sync：需要 Obsidian 账号邮箱/用户名、登录密码或交互登录、远程 vault 名字或 ID，必要时还要端到端加密密码。
   - 分类标准：由 LLM 初始化生成分类规则，还是用户稍后自行编辑。
2. 收集完首次安装选项后，再运行安装和初始化命令。例如：
   ```bash
   python install.py
   ```
   如果安装环境只能调用 scripts 目录，也可以运行：
   ```bash
   python scripts/interactive_install.py
   ```
   非交互拆分安装时再使用底层命令：
   ```bash
   python scripts/setup.py --init --install-skill-deps --install-python-deps --install-playwright
   ```
3. 安装 hctec 第三方技能后，必须运行一次知乎格式补丁，避免知乎正文 plain 文本丢失段落和换行：
   ```bash
   python scripts/patch_hctec_zhihu_format.py
   ```
   详见 `references/dependencies.md`。
4. 首次安装时按用户选择部署 CookieCloud 服务端并安装浏览器插件。详见 `references/auth.md`。
5. 如果 CookieCloud 服务端不在运行本技能的机器上，用 `--cookiecloud-server-url http://<服务器IP>:8088` 初始化，或让用户手动填写 `COOKIECLOUD_SERVER_URL`、`COOKIECLOUD_UUID` 和 `COOKIECLOUD_PASSWORD`。
6. 首次安装时按用户选择配置 Obsidian 同步方式。官方 Sync 走 `obsidian-headless`、`ob login` 和 `ob sync-setup`；本地模式则只初始化本地目录。详见 `references/obsidian-sync.md`。
7. agent 判断是否首次安装时，运行：
   ```bash
   python scripts/setup.py --status --json
   ```
8. 检查配置：
   ```bash
   python scripts/setup.py --doctor
   ```
9. 同步并导出：
   ```bash
   python scripts/sync.py --platform xhs
   python scripts/sync.py --platform zhihu
   python scripts/export_obsidian.py --platform all --incremental
   ```
10. 如果用户要自动化，生成 OpenClaw cron 配置：
   ```bash
   python scripts/install_cron.py --platform xhs --time 06:00 --print
   python scripts/install_cron.py --platform zhihu --time 05:00 --print
   ```

## 按需阅读

- 首次安装访谈和选项决策：`references/first-install.md`
- 首次安装和外部依赖：`references/dependencies.md`
- CookieCloud 服务端、浏览器插件和 cookie 兜底：`references/auth.md`
- 配置字段：`references/config.md`
- Obsidian Headless Sync 和本地目录模式：`references/obsidian-sync.md`
- 定时任务：`references/cron.md`
- Obsidian 目录和分类：`references/obsidian-layout.md`

## 安全

不要把用户数据发布进技能包：`cookiecloud.env`、原始 Cookie、状态文件、日志、已下载笔记、图片、Obsidian 导出内容都只能作为运行时数据保存在用户本机。
