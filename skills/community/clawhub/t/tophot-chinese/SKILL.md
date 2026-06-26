# 技能：今日热榜爬虫与内容抓取 (TopHub Spider)

## 1. 环境依赖与安装 (Prerequisites)
如果系统尚未安装相关依赖，Agent 应参考以下步骤进行环境部署：

1. **核心库安装**: `pip install crawl4ai requests tqdm pypinyin`（若 `pip` 不可用则用 `pip3`）
2. **浏览器内核初始化**: `python -m playwright install chromium`（若 `python` 不可用则用 `python3`）

> **注意**: 以下命令中的 `python` 在部分平台可能需要替换为 `python3`，Agent 应自行判断当前环境使用哪个。

---

## 2. 技能描述

本技能由两个脚本组成，职责分离：

| 脚本 | 职责 | 说明 |
| --- | --- | --- |
| `{baseDir}/scripts/{baseDir}/scripts/tophub_spider.py` | **获取热榜列表** | 从 tophub.today 拉取热榜，生成 `{标题}.json` 文件（只含 title、description、url，不抓正文） |
| `{baseDir}/scripts/{baseDir}/scripts/fetch_site_content.py` | **抓取正文内容** | 读取 JSON 文件中的 url，用 crawl4ai 抓取 Markdown 正文并保存 |

**典型工作流**：
1. 用 `{baseDir}/scripts/tophub_spider.py` 拉取某网站热榜 → 生成 `{保存路径}/{网站拼音}/{标题}.json`
2. 用 `{baseDir}/scripts/fetch_site_content.py` 对单个文件或整个目录抓取正文内容

---

## 3. 核心指令集

### 3.1 {baseDir}/scripts/tophub_spider.py — 获取热榜列表

获取指定网站热榜（全部）：
```bash
python {baseDir}/scripts/tophub_spider.py <网站名称>
```

获取前 N 条：
```bash
python {baseDir}/scripts/tophub_spider.py <网站名称> --top <数量>
```

指定保存路径：
```bash
python {baseDir}/scripts/tophub_spider.py <网站名称> --output <路径> --top <数量>
```

查看所有可用站点：
```bash
python {baseDir}/scripts/tophub_spider.py
```

### 3.2 {baseDir}/scripts/fetch_site_content.py — 抓取正文内容

抓取单个文件（回写到原文件的 content 字段）：
```bash
python {baseDir}/scripts/fetch_site_content.py <文件.json>
```

抓取单个文件（保存到指定文件）：
```bash
python {baseDir}/scripts/fetch_site_content.py <文件.json> --output <输出文件.json>
```

批量抓取目录下所有文件（回写到各原文件）：
```bash
python {baseDir}/scripts/fetch_site_content.py <目录路径>
```

批量抓取并保存到另一个目录：
```bash
python {baseDir}/scripts/fetch_site_content.py <目录路径> --output <输出目录>
```

强制重新抓取 + 只处理前 N 个：
```bash
python {baseDir}/scripts/fetch_site_content.py <目录路径> --force --top <数量>
```

---

## 4. 参数说明

### {baseDir}/scripts/tophub_spider.py

| 参数 | 缩写 | 必填 | 说明 |
| --- | --- | --- | --- |
| `site` | - | 是 | 网站名称（来源于 tophub.today 的站点名），常见站点见下方列表 |
| `--output` | `-o` | 否 | 保存路径，默认 `./site_contents` |
| `--top` | `-n` | 否 | 获取前N条，默认全部 |

**支持的网站名称**（数据来源于 [tophub.today](https://tophub.today)，实际可用站点以运行时为准）：

| 分类 | 站点名称 |
| --- | --- |
| 综合 | 知乎、微博、微信、澎湃、百度、今日头条、抖音、百度贴吧 |
| 科技 | 36氪、少数派、虎嗅网、IT之家 |
| 人工智能 | 掘金、机器之心、量子位、Readhub |
| 娱乐 | 哔哩哔哩、抖音、快手、AcFun |
| 社区 | 吾爱破解、百度贴吧、腾讯新闻、虎扑社区 |
| 购物 | 淘宝、天猫、京东、今日热卖 |
| 财经 | 雪球、第一财经、华尔街见闻、新浪财经 |
| 影视 | 豆瓣电影、猫眼、IMDb、百度视频 |
| 阅读 | 微信读书、当当、七猫中文网 |
| 游戏 | TapTap、3DM游戏网、机核网、游研社 |
| 音乐 | Apple Music、QQ音乐、豆瓣音乐 |
| 体育 | 新浪体育、虎扑社区、懂球帝 |
| 开发 | GitHub、CSDN、掘金、开源中国 |
| 设计 | 站酷、UI中国、优设网、Behance |
| 产品 | 人人都是产品经理、PMCAFF、即刻、Product Hunt |
| 汽车 | 汽车之家、懂车帝、易车网、太平洋汽车网 |
| 日报 | 知乎日报、开眼视频、历史上的今天 |
| 大学 | 水木社区、北大未名、北邮人论坛 |
| 地方 | 高楼迷、宽带山、厦门小鱼、过早客 |
| 应用 | App Store、爱范儿、少数派 |

> **提示**: 不确定时可运行 `python {baseDir}/scripts/tophub_spider.py` 查看当前所有可用站点。

### {baseDir}/scripts/fetch_site_content.py

| 参数 | 缩写 | 必填 | 说明 |
| --- | --- | --- | --- |
| `input` | - | 是 | JSON 文件路径 或 包含 JSON 文件的目录路径 |
| `--output` | `-o` | 否 | 输出路径。不指定则回写到原文件的 `content` 字段；指定则单独保存 |
| `--force` | `-f` | 否 | [目录模式] 强制重新抓取已有内容的文件 |
| `--top` | `-n` | 否 | [目录模式] 只处理前 N 个文件 |

---

## 5. 输出结构

### {baseDir}/scripts/tophub_spider.py 生成的文件

```
<保存路径>/
  <网站拼音>/              # 如 zhi_hu、wei_xin
    <标题1>.json           # 标题中所有符号替换为下划线
    <标题2>.json
    ...
```

每个 JSON 文件包含（此时 content 为空）：
```json
{
  "title": "文章标题",
  "description": "简介",
  "url": "原始链接",
  "created_at": "创建时间",
  "content": ""
}
```

### {baseDir}/scripts/fetch_site_content.py 抓取后

回写模式（无 `--output`）：直接将 `content` 字段填入原文件，并添加 `fetched_at` 和 `error` 字段。

输出模式（有 `--output`）：保存到指定路径，包含完整字段：
```json
{
  "title": "文章标题",
  "description": "简介",
  "url": "原始链接",
  "fetched_at": "抓取时间",
  "content": "Markdown 正文内容",
  "error": null
}
```

---

## 6. 使用示例

| 用户指令 | 预期的 Agent 行为 |
| --- | --- |
| "帮我抓取知乎热榜前10条" | `python {baseDir}/scripts/tophub_spider.py 知乎 --top 10` |
| "爬取微信热榜保存到 /tmp/data" | `python {baseDir}/scripts/tophub_spider.py 微信 -o /tmp/data` |
| "抓取B站热榜前5条存到指定目录" | `python {baseDir}/scripts/tophub_spider.py B站 -o /path/to/dir -n 5` |
| "有哪些网站可以抓" | `python {baseDir}/scripts/tophub_spider.py` |
| "帮我获取这篇文章的正文" | `python {baseDir}/scripts/fetch_site_content.py <文件.json>` |
| "把这个目录下的文章都抓取一下" | `python {baseDir}/scripts/fetch_site_content.py <目录路径>` |
| "重新抓取这个目录前5篇" | `python {baseDir}/scripts/fetch_site_content.py <目录路径> --force --top 5` |
| "抓取这篇文章保存到 /tmp/out.json" | `python {baseDir}/scripts/fetch_site_content.py <文件.json> -o /tmp/out.json` |

---

## 7. 约束与安全

* **隐私声明**: 仅抓取公开可访问的热榜内容，不涉及登录态数据。
* **频率控制**: 每条抓取间隔 1 秒，微信链接额外等待 2 秒，避免触发反爬。
* **数据来源**: 热榜列表来自 tophub.today，正文通过 Crawl4AI 抓取原始链接。
