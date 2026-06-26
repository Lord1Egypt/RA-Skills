---
name: "china-hotdata"
description: "中国实时热点数据采集工具。当用户询问热搜、热榜、热点、排行榜、榜单、票房、收视率、音乐排行、歌曲排名、报纸、新闻头条、人民日报等话题时使用此技能。覆盖：抖音/微博/百度/B站/快手热搜，QQ音乐/网易云/酷狗/酷我音乐榜，猫眼电影票房/电视剧收视/综艺热度，App Store游戏/应用排行榜，人民日报电子版PDF及高清版面图。通过 Node.js 脚本实时获取数据，JSON 格式输出，无需 API Key，无需服务器。"
---

# 中国实时热点数据采集工具

实时获取中国各大平台热点数据的 OpenClaw Skill。通过运行 Node.js 脚本获取最新数据，JSON 格式输出。

## 何时使用此技能

**当用户的问题涉及以下任意话题时，你应该使用此技能：**

### 热搜/热点类
用户提到：热搜、热榜、热门、热点、趋势、什么最火、大家在搜什么、今天发生了什么、吃瓜、全网热议、抖音、微博、百度、B站、哔哩哔哩、快手

→ 使用 `crawl-hot.js`

### 音乐/歌曲类
用户提到：音乐、歌曲、歌、热歌、新歌、飙升、排行榜、榜单、什么歌好听、现在流行什么歌、QQ音乐、网易云、酷狗、酷我

→ 使用 `crawl-music.js`

### 影视/娱乐/游戏类
用户提到：电影、票房、电视剧、网剧、综艺、收视率、热度、游戏排行、App Store、应用排行、好看的剧、最近上映、猫眼

→ 使用 `crawl-entertainment.js`

### 报纸/新闻类
用户提到：报纸、人民日报、看报、今日新闻头条、头版头条、要闻、日报

→ 使用 `crawl-paper.js`

## 使用方式

所有脚本通过 `node` 命令运行，输出 JSON 到标准输出。需要 Node.js 18+（内置 fetch）。

**重要：运行脚本时，工作目录必须在本技能的根目录下，即脚本路径相对于技能安装目录。**

### 快速选择指南

根据用户意图，选择对应命令：

| 用户想了解的内容 | 运行命令 |
|----------------|---------|
| 某平台热搜 | `node scripts/crawl-hot.js --platform=平台名` |
| 所有平台热搜 | `node scripts/crawl-hot.js` |
| 某平台音乐榜 | `node scripts/crawl-music.js --platform=平台名 --type=hot或rising` |
| 所有音乐榜 | `node scripts/crawl-music.js` |
| 电影票房/电视剧/综艺/游戏等 | `node scripts/crawl-entertainment.js --type=类型` |
| 所有影视游戏数据 | `node scripts/crawl-entertainment.js` |
| 今日/指定日期报纸 | `node scripts/crawl-paper.js --date=日期` |

---

### 🔥 获取热搜数据

采集抖音、微博、百度、B站、快手五大平台的实时热搜榜单。

```bash
# 获取抖音热搜
node scripts/crawl-hot.js --platform=douyin

# 获取微博热搜
node scripts/crawl-hot.js --platform=weibo

# 获取百度热搜
node scripts/crawl-hot.js --platform=baidu

# 获取B站热搜
node scripts/crawl-hot.js --platform=bilibili

# 获取快手热搜
node scripts/crawl-hot.js --platform=kuaishou

# 获取全部平台热搜（默认）
node scripts/crawl-hot.js --platform=all
node scripts/crawl-hot.js
```

**参数：** `--platform=douyin|weibo|baidu|bilibili|kuaishou|all`（默认 all）

**平台名对照：**
- 抖音 / TikTok → `douyin`
- 微博 / Weibo → `weibo`
- 百度 / Baidu → `baidu`
- B站 / 哔哩哔哩 / Bilibili → `bilibili`
- 快手 / Kuaishou → `kuaishou`

### 🎵 获取音乐排行榜

采集QQ音乐、网易云音乐、酷狗音乐、酷我音乐的热歌榜和飙升榜。

```bash
# 获取QQ音乐热歌榜
node scripts/crawl-music.js --platform=qq --type=hot

# 获取网易云飙升榜
node scripts/crawl-music.js --platform=wangyi --type=rising

# 获取酷狗全部榜单
node scripts/crawl-music.js --platform=kugou

# 获取全部平台全部榜单（默认）
node scripts/crawl-music.js
```

**参数：**
- `--platform=qq|wangyi|kugou|kuwo|all`（默认 all）
- `--type=hot|rising|all`（默认 all，hot=热歌榜，rising=飙升榜）

**平台名对照：**
- QQ音乐 → `qq`
- 网易云音乐 / 网易 → `wangyi`
- 酷狗音乐 → `kugou`
- 酷我音乐 → `kuwo`

### 🎬 获取影视/游戏数据

采集猫眼票房和App Store排行数据。

```bash
# 获取电影票房
node scripts/crawl-entertainment.js --type=movie

# 获取电视剧收视
node scripts/crawl-entertainment.js --type=tv

# 获取网播热度
node scripts/crawl-entertainment.js --type=web

# 获取综艺热度
node scripts/crawl-entertainment.js --type=variety

# 获取App Store免费游戏排行
node scripts/crawl-entertainment.js --type=game_free

# 获取App Store付费游戏排行
node scripts/crawl-entertainment.js --type=game_paid

# 获取App Store免费应用排行
node scripts/crawl-entertainment.js --type=app_free

# 获取App Store付费应用排行
node scripts/crawl-entertainment.js --type=app_paid

# 获取全部影视/游戏数据（默认）
node scripts/crawl-entertainment.js
```

**参数：** `--type=movie|tv|web|variety|game_free|game_paid|app_free|app_paid|all`（默认 all）

**类型对照：**
- 电影 / 票房 → `movie`
- 电视剧 / 收视 → `tv`
- 网播 / 网剧 / 网络剧 → `web`
- 综艺 / 综艺节目 → `variety`
- 免费游戏 → `game_free`
- 付费游戏 → `game_paid`
- 免费应用 / 免费APP → `app_free`
- 付费应用 / 付费APP → `app_paid`

### 📰 获取人民日报电子版

采集人民日报每日各版面的 PDF 下载链接和高清版面图片。

```bash
# 获取今日人民日报全部版面 PDF
node scripts/crawl-paper.js

# 获取昨日报纸
node scripts/crawl-paper.js --date=yesterday

# 获取指定日期报纸
node scripts/crawl-paper.js --date=2026-03-10

# 只获取前 5 个版面
node scripts/crawl-paper.js --pages=1,2,3,4,5
```

**参数：**
- `--date=today|yesterday|YYYY-MM-DD`（默认 today）
- `--pages=1,2,3`（可选，指定版面编号，默认全部）

**提示：** 返回结果中的 `image_url` 字段是版面高清大图链接，你可以用 Markdown 语法 `![版面标题](image_url)` 直接在聊天窗口渲染图片给用户阅读，无需让用户下载 PDF。

## 输出格式

所有脚本统一输出 JSON：

```json
{
  "status": "ok",
  "results": {
    "平台名": {
      "success": true,
      "label": "描述",
      "data": {
        "sj": [ ... ],
        "time": "2026-01-01 12:00:00"
      },
      "count": 50
    }
  }
}
```

### 热搜数据字段
| 字段 | 说明 |
|------|------|
| `word` | 热搜关键词 |
| `hot_value` | 热度值 |
| `url` | 搜索链接 |
| `label` | 标签（热/新等） |

### 音乐数据字段
| 字段 | 说明 |
|------|------|
| `name` | 歌曲名 |
| `geshou` | 歌手 |
| `hot` | 排名/热度 |
| `img` | 封面URL（部分） |

### 影视数据字段

**电影：** `name`（片名）、`piaofang`（票房）、`pfzb`（占比）、`syts`（上映天数）

**电视剧/网播/综艺：** `name`（名称）、`piaofang`（收视率/热度）、`pfzb`（频道/平台）

**App Store：** `name`（应用名）、`pingfen`（评分）、`img`（图标）、`url`（链接）

### 报纸数据字段
| 字段 | 说明 |
|------|------|
| `page` | 版面编号（1, 2, 3...） |
| `title` | 版面标题（如「01版：要闻」） |
| `pdf_url` | PDF 下载链接 |
| `file_name` | PDF 文件名 |
| `image_url` | 版面高清大图链接（可用 `![标题](url)` 直接渲染） |

## 用户意图 → 命令映射（完整参考）

以下是用户可能的提问方式和对应的命令。如果用户的问题与下表中的示例语义相近，请调用对应命令：

| 用户可能的问法 | 应运行的命令 |
|--------------|------------|
| "现在抖音上什么最火？" | `node scripts/crawl-hot.js --platform=douyin` |
| "今天微博热搜有哪些？" | `node scripts/crawl-hot.js --platform=weibo` |
| "帮我看看百度热搜" | `node scripts/crawl-hot.js --platform=baidu` |
| "B站上大家在看什么？" | `node scripts/crawl-hot.js --platform=bilibili` |
| "快手热门是什么？" | `node scripts/crawl-hot.js --platform=kuaishou` |
| "全网在讨论什么？" | `node scripts/crawl-hot.js` |
| "看看所有热搜" | `node scripts/crawl-hot.js` |
| "有什么热点新闻？" | `node scripts/crawl-hot.js` |
| "今天有什么大事？" | `node scripts/crawl-hot.js` |
| "帮我吃个瓜" | `node scripts/crawl-hot.js` |
| "现在最火的歌是什么？" | `node scripts/crawl-music.js --type=hot` |
| "有什么好听的歌推荐？" | `node scripts/crawl-music.js --type=hot` |
| "QQ音乐热歌榜" | `node scripts/crawl-music.js --platform=qq --type=hot` |
| "网易云音乐飙升榜" | `node scripts/crawl-music.js --platform=wangyi --type=rising` |
| "酷狗飙升榜有什么新歌？" | `node scripts/crawl-music.js --platform=kugou --type=rising` |
| "现在流行听什么歌？" | `node scripts/crawl-music.js` |
| "音乐排行榜" | `node scripts/crawl-music.js` |
| "今天电影票房排行" | `node scripts/crawl-entertainment.js --type=movie` |
| "最近什么电影好看？" | `node scripts/crawl-entertainment.js --type=movie` |
| "最近有什么好看的电视剧？" | `node scripts/crawl-entertainment.js --type=tv` |
| "综艺节目排行" | `node scripts/crawl-entertainment.js --type=variety` |
| "网播热度排行" | `node scripts/crawl-entertainment.js --type=web` |
| "App Store游戏排行" | `node scripts/crawl-entertainment.js --type=game_free` |
| "有什么好玩的游戏？" | `node scripts/crawl-entertainment.js --type=game_free` |
| "App Store付费应用排行" | `node scripts/crawl-entertainment.js --type=app_paid` |
| "看今日报纸" | `node scripts/crawl-paper.js` |
| "今天人民日报说了什么？" | `node scripts/crawl-paper.js` |
| "看昨天的报纸" | `node scripts/crawl-paper.js --date=yesterday` |
| "3月10号的人民日报" | `node scripts/crawl-paper.js --date=2026-03-10` |
| "头版头条是什么？" | `node scripts/crawl-paper.js --pages=1` |

## 注意事项

1. 需要 Node.js 18+ 版本（使用内置 fetch API）
2. 所有数据实时获取，响应时间取决于上游数据源（通常 1-3 秒）
3. 快手热搜较不稳定，偶尔可能返回空数据
4. 无需任何 API Key 或密钥配置
