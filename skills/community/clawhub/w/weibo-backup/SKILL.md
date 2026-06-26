---
name: weibo-downloader
description: |
  使用 Playwright 自动化下载微博(weibo)收藏内容，本人或其他博主发表微博内容所有历史记录，包括图片、视频和长文章。
  当用户提到"微博收藏"、"下载微博"、"备份微博"、"weibo favorites"、
  "抓取微博内容"、"保存微博图片"或任何与微博数据备份相关的需求时，
  支持 headless 模式、支持图片尺寸选择、视频下载、长文章提取等功能，以Markdown格式保存。。
---
# 微博下载工具使用指南

## 概述

此工具使用 Playwright 自动化浏览器来下载微博内容，包括：
- 支持下载微博收藏、本人微博、他人微博
- 图片（支持九宫格排列，支持多种尺寸：360px、480px、690px、2000px、原图 large）
- 视频（可选下载， 默认最高质量）
- 长文章（可选下载）
- **Markdown 双向链接** - 在保存的 Markdown 文件中添加"前一条"和"下一条"导航链接，方便浏览

请正确使用本技能，用于微博收藏、个人数据备份或者关注博主的内容备份保存。不能用于大规模的商业数据采集。
## 前置要求

1. **Python 环境**：需要 Python 3.8+
2. **依赖安装**：
   ```bash
   pip install playwright
   playwright install chromium
   ```

## Script Directory

Determine this SKILL.md directory as `{baseDir}`.

| Script                        | Purpose                        |
| ----------------------------- | ------------------------------ |
| `weibo_favorites_4skill.py` | Main python script entry point |

## 使用流程

1. 检查 {baseDir}/cookies.json 文件是否存在, 或 {baseDir}/user_data_dir or user input user_data_dir 是否存在且包含有效的用户数据 
2. 如果用户cookies数据不存在，或者用户没有提供 target url,  则提示用户: 我将运行script以打开浏览器，请在60秒内完成登录，并进入需要下载的页面：收藏页 / 本人主页 / 他人主页。
3. 完成提示后再使用命令脚本下载微博收藏内容， 第一次下载可以用无参数运行快速得到预览结果。
4. 如果用户提供--url参数， 且用户cookies数据存在，则参照日常使用命令示例，不提示用户直接运行下载脚本。
5. 运行完成后，提示用户输出目录的具体位置

### 注意 ： 如果不存在/cookies.json，或者用户没有提供 target url， 一定不能直接运行下载脚本， 你要分两步， 先提示用户再运行。

## 常用命令示例

首先提示用户在60秒内完成登录，并进入需要下载的页面：收藏页 / 本人主页 / 他人主页。
完成提示后再使用命令脚本下载微博收藏内容， 第一次下载可以用无参数运行快速得到预览结果。
如果用户提供--url参数， 且{baseDir}/cookies.json 文件存在，则推荐使用headless 模式。

### 基础使用（下载10条记录，360px图片， 不下载视频， 推荐给用户首次使用，可以快速得到预览结果）

```bash
python {baseDir}/weibo_favorites_4skill.py
```
 注： 不提供output-dir参数，默认输出到skill脚本所在目录下的output目录。

### 日常使用（推荐配置， 推荐给用户后续的日常使用，headless 模式，下载600条记录包括高清图片，视频，长文章， 跳过已存在的记录 ）

```bash
python {baseDir}/weibo_favorites_4skill.py \
  --image-size large \
  --download-video \
  --download-article \
  --max-download 600 \
  --skip-existing \
  --headless
```

## 参数说明

| 参数                  | 说明                           | 默认值                                      |
| -------------------  | ------------------------------ | ---------------------------------------    |
| `--url`              | 目标微博用户主页或收藏页面URL      | https://weibo.com                          |
| `--max-download`     | 最大下载数量                     | 10                                         |
| `--skip-existing`    | 跳过已存在的记录                  | False                                      |
| `--image-size`       | 图片尺寸：360/480/690/2000/large | 360                                        |
| `--download-video`   | 下载视频到本地                    | 开关参数，不需要指定值，无此参数则只保留视频链接   |
| `--download-article` | 下载长文章到本地                  | 开关参数，不需要指定值，无此参数则只保留文章链接   |
| `--batch-size`       | 分批次每次下载记录数               | 20                                         |
| `--headless`         | 无头模式（不显示浏览器）            | 开关参数，不需要指定值，无此参数则显示浏览器窗口   |
| `--user-data-dir`    | 浏览器用户数据目录                 | 无此参数默认使用 cookies.json                 |
| `--output-dir`       | 自定义输出目录                    | python脚本所在目录下的output目录               |

## 输出目录结构

```
output/
├── pictures/          # 图片目录
│   └── {record_id}/   # 每条微博的图片
├── videos/            # 视频目录
├── articles/          # 长文章目录
│   └── pictures/      # 文章中的图片
└── {author}_{date}_{id}.md  # 微博内容Markdown文件
```

## 工作流程

1. **启动浏览器**：根据参数选择启动方式
2. **检查登录状态**：如需要登录，提示用户手动登录
3. **滚动页面**：自动滚动加载更多微博
4. **提取数据**：解析微博内容、图片、视频链接
5. **下载资源**：下载图片、视频到本地
6. **生成 Markdown**：保存微博文本和图片引用

## 注意事项

1. **首次登录**：不能使用 headless 模式，需要看到浏览器窗口进行登录
2. **登录状态**：建议定期更新 cookies 或用户数据目录，避免登录过期
3. **下载限制**：微博可能有反爬限制，建议合理设置下载数量
4. **网络环境**：确保网络可以正常访问微博
5. **存储空间**：下载大量高清图片和视频需要足够的磁盘空间

## 故障排除

### 登录问题

- 检查网络连接
- 尝试删除 cookies.json 或 browser_data 目录重新登录
- 确保没有开启 VPN 或代理导致访问异常

### 下载失败

- 检查磁盘空间
- 检查目录权限
- 尝试降低 `--max-download` 数量

### 浏览器启动失败

- 确保已运行 `playwright install chromium`
- 检查系统是否支持 Chromium 运行
