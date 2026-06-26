---
name: XiaoyaDownload
description: 搜索并从小雅 Alist 下载电影/剧集到本地目录。输入电影或剧集名称，通过小雅搜索接口查找，选择结果后下载到本地。安全修复 v1.3.2：强化路径穿越防护，使用 pathlib.relative_to() 做严格 containment 检查。
---

# 🎬 XiaoyaDownload — 小雅影音下载器

搜索小雅/Alist 中的电影/剧集，通过本地 WebDAV 挂载复制到 NAS 指定目录。

## 功能

1. **搜索全库** — 输入电影/剧集名称，直接搜索小雅全库资源
2. **版本选择** — 显示多个版本（不同画质、大小、格式），你可以挑选
3. **WebDAV 复制** — NAS 挂载了小雅 WebDAV 时，用 `rsync` 本地高速复制

## 使用方式

### 搜索电影/剧集

> "搜索肖申克的救赎"
> "帮我找找盗梦空间"

### 选择要下载的版本

搜索后列出所有版本，告诉小虾编号：

> "下载第1个"

### 操作示例

```
🦐: 搜索肖申克的救赎

🔍 正在搜索「肖申克的救赎」...

📋 搜索结果：共 55 个

  ┌───┬──────────────────────────────────┬──────────────────────┬───────┐
  │ # │ 文件                               │ 画质·编码              │ 大小  │
  ├───┼──────────────────────────────────┼──────────────────────┼───────┤
  │  1 │ 📁 【肖申克的救赎】                        │ -                    │ -     │
  │  2 │ 🎬 肖申克的救赎.1994.BluRay.1080p.x265.. │ 1080p BluRay x265   │ 11.8GB│
  │  3 │ 🎬 肖申克的救赎.1994.2160p.WEB-DL.x26.. │ 4K HDR x265         │ 25.6GB│
  │  4 │ 📁 肖申克的救赎 4K REMUX                  │ 4K REMUX            │ -     │
  └───┴──────────────────────────────────┴──────────────────────┴───────┘

🦐: 要下载哪个？(输入编号)

你: 2

🦐: 📁 复制文件: /path/to/your/file.mkv → /path/to/your/download/
    rsync 速度: 39 MB/s
    ✅ 复制完成！
```

## 环境配置

创建 `.env` 文件：

```
# 小雅/Alist 网页地址（必填）
XIAOYA_HOST=http://your-xiaoya-ip:5678

# 下载保存目录（必填）
DOWNLOAD_DIR=/path/to/your/download

# WebDAV 本地挂载路径（推荐）
WEBDAV_MOUNT=/path/to/your/webdav/mount
```

## CLI 命令

```bash
# 配置检查
python3 scripts/xiaoya_download.py setup

# 搜索
python3 scripts/xiaoya_download.py search "肖申克的救赎"

# 复制到本地（WebDAV）
python3 scripts/xiaoya_download.py copy "/电影/IMDB Top 250/200-250/肖申克的救赎...mkv"
```

## 依赖

- **rsync**（系统命令，用于 WebDAV 复制）
- **Python 3 + requests 库**（`pip3 install requests`）
- **WebDAV 本地挂载**（需先在 `.env` 中配置 `WEBDAV_MOUNT`）

## 安全说明

- 所有远程路径经过 **unquote → resolve → 路径穿越检查** 后才使用
- 复制操作限定在 `WEBDAV_MOUNT` 目录内
- `.env` 配置文件不在发布包中，需用户自行创建

## 文件结构

```
skills/XiaoyaDownload/
├── SKILL.md
├── scripts/
│   └── xiaoya_download.py
├── .env           # 用户自建（不在发布包中）
├── .env.example
└── _meta.json
```
