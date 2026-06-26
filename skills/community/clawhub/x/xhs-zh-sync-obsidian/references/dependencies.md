# 依赖安装

本技能不直接实现小红书/知乎抓取。抓取由 hctec 原子技能负责，本技能负责安装向导、运行状态、分类、Obsidian 导出和定时任务生成。

## 必需 hctec 技能

- `hctec-xiaohongshu-favorites`
- `hctec-zhihu-favorites`
- `hctec-favorites-harvester`

这些技能不在 ClawHub。它们来自：

```text
https://github.com/hc-tec/my-collection-skills/tree/main/skills
```

首次安装建议运行：

```bash
python scripts/setup.py --install-skill-deps
```

脚本会从 GitHub 下载仓库，并把目录映射安装为：

```text
skills/xiaohongshu-favorites -> ~/.openclaw/workspace/skills/hctec-xiaohongshu-favorites
skills/zhihu-favorites       -> ~/.openclaw/workspace/skills/hctec-zhihu-favorites
skills/favorites-harvester   -> ~/.openclaw/workspace/skills/hctec-favorites-harvester
```

如果目标目录不同：

```bash
python scripts/setup.py --install-skill-deps --skills-root /path/to/skills
```

如果要使用 fork 或镜像仓库：

```bash
python scripts/setup.py --install-skill-deps --hctec-repo https://github.com/<owner>/<repo>.git
```

手动安装时，也可以直接下载 GitHub 仓库中的三个目录，然后在配置里指定位置：

```yaml
hctec:
  skills_root: "~/.openclaw/workspace/skills"
```

## hctec 知乎格式补丁

安装或更新 hctec 第三方技能后，运行一次本技能自带补丁：

```bash
python scripts/patch_hctec_zhihu_format.py
```

原因：`hctec-zhihu-favorites/scripts/zhihu_item_content.py` 当前会把知乎 HTML 正文转换成紧凑 plain 文本，段落、标题、列表和换行会被压成一行。本技能导出 Obsidian 时会优先使用 `plain` 字段，因此必须先补丁第三方脚本，让 `plain` 保留基本块级格式。

补丁行为：

- 定位 `hctec-zhihu-favorites/scripts/zhihu_item_content.py`。
- 替换 `_TextExtractor`，保留 `p`、`h1-h6`、`blockquote`、`li`、`br` 等块级换行。
- 将图片位置保留为 `[图片]` 占位；真正图片下载和 `![[...]]` 引用由本技能 `export_obsidian.py` 处理。
- 幂等执行：已打补丁时会输出 `already patched`，不会重复修改。

如果 hctec 技能安装在非默认位置：

```bash
python scripts/patch_hctec_zhihu_format.py --skills-root /path/to/skills
```

## Python 与浏览器依赖

运行：

```bash
python scripts/setup.py --init --install-python-deps --install-playwright
```

这会安装：

- `PyYAML`：读取配置和分类规则
- `requests`：兼容依赖脚本里的 HTTP 流程
- `playwright` 和 Chromium：小红书/知乎浏览器登录态和 fallback
- `Pillow`：兼容媒体处理流程

## 首次安装顺序

1. 从 GitHub 安装 hctec 技能：`python scripts/setup.py --install-skill-deps`。
2. 运行 `python scripts/patch_hctec_zhihu_format.py` 修复知乎正文格式保留。
3. 运行 `setup.py --init --install-python-deps --install-playwright`。首次初始化会随机创建本地 Obsidian 存储目录。
4. 部署 CookieCloud Docker 服务端。默认部署在运行技能的本机；如果不是本机，初始化时加 `--cookiecloud-server-url http://<服务器IP>:8088`。
5. 在本地浏览器安装 CookieCloud 插件，填入脚本生成的 UUID/password 和服务端地址。
6. 如果 CookieCloud 服务端不是本机，编辑 `cookiecloud.env` 里的 `COOKIECLOUD_SERVER_URL`。
7. 运行 `python scripts/setup.py --doctor`。
8. 小规模同步验证：
   ```bash
   python scripts/sync.py --platform xhs
   python scripts/sync.py --platform zhihu
   python scripts/export_obsidian.py --platform all --incremental
   ```

## Obsidian 依赖

如果用户选择官方 Obsidian Sync，需要额外安装 `obsidian-headless`：

```bash
python scripts/setup.py --install-ob
python scripts/setup.py --setup-ob-sync
```

如果用户选择自建同步或只需要本地目录，不运行上面两条命令；保持 `obsidian.run_ob_sync=false`。
