---
name: silas_wechat_article_search
description: 微信公众号文章搜索与解析。搜狗微信+新榜双源搜索，Python脚本解析全文（零Node依赖），Serper转载兜底。
metadata:
  openclaw:
    os: linux
---

# 微信公众号文章搜索与解析 v2.0

搜索微信公众号文章 → 解析全文 → 评分 → 入库知识库。

## 搜索源（按优先级）

### 源1：搜狗微信（主力，零依赖）
```bash
curl -s "https://weixin.sogou.com/weixin?type=2&query=关键词" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```
用 Python 正则提取标题和链接，返回搜狗中间链接列表。

### 源2：新榜（补充）
```bash
curl -s "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -d '{"q":"site:newrank.cn 关键词","num":10}'
```

### 源3：Serper 转载兜底
当微信原文无法解析时，搜索转载版：
```bash
curl -s "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -d '{"q":"文章标题","num":5}'
```
优先选新浪/搜狐/网易等全文转载。

## 内容解析（Python 脚本）

**核心脚本**：`scripts/parse_article.py`

### 依赖
```bash
pip3 install requests beautifulsoup4
```

### 用法
```bash
python3 scripts/parse_article.py "https://mp.weixin.qq.com/s/xxxxx"
python3 scripts/parse_article.py "URL" --save
python3 scripts/parse_article.py "URL" --save --output article.json
```

### 输出 JSON
```json
{
  "title": "文章标题",
  "author": "公众号名称",
  "publish_time": "2026-04-18",
  "content": "正文全文...",
  "word_count": 5594,
  "images_count": 21,
  "images": ["url1", "url2", ...],
  "url": "原始链接",
  "parsed_at": "2026-04-18 22:00:00"
}
```

### 原理
- **iPhone UA** 绕过微信验证（关键！）
- **BeautifulSoup** 解析 `rich_media_content` 提取正文
- **段落结构保留**，过滤 <10 字的噪声
- **图片提取**：`data-src` 属性（微信防盗链图）

### 微信原文解析失败时
1. Serper 搜转载版（新浪/搜狐/网易）
2. web_fetch 抓转载全文
3. browser-search 兜底

## 入库流程

### 1. 搜索
```
选词（从 web-keywords.json）→ 搜狗搜索 → 新榜补充 → 合并去重
```

### 2. 解析
```
对每篇目标文章：
a. 先用 Python 脚本解析微信原文
b. 失败 → Serper 搜转载 → web_fetch 抓全文
c. 提取：标题、作者、正文、图片
```

### 3. 评分
```
5 维度评分（同 web-search 技能标准）：
- 数据密度 30%、实操性 25%、时效性 20%、相关性 15%、来源权威 10%
- < 5.0 不入库
- ≥ 8.5 通知管理员
```

### 4. 去重
```
a. feishu_search_doc_wiki 搜索知识库标题
b. memory/collect-log.json 查历史
c. URL + 标题去重
```

### 5. 入库
```
a. 读 wiki-directory-manager 技能匹配目录
b. feishu_create_doc 创建文档（标题不带评分）
c. 正文格式：
   > 来源：URL
   > 发布日期：YYYY-MM-DD
   > 采集日期：YYYY-MM-DD
   > 评分：X.X 🟢/🟡/🟠/🔴
   
   正文内容...
d. 有信息量图片 → 保存本地 → feishu_doc_media insert
e. 写多维表格索引（目录必须和实际一致）
```

## 图片处理

- **保存标准**：数据图表/流程图/对比截图/产品截图
- **跳过**：装饰图/广告/头像/logo
- 每篇最多 10 张，单张 <20MB
- 保存路径：`/tmp/openclaw/images/`

## 踩坑指南

- **微信验证码**：iPhone UA 可绕过，Desktop UA 会被拦截
- **搜狗中间链接**：不能直接 web_fetch，需先解析跳转或用 Python 脚本
- **微信图片防盗链**：`data-src` 是真实地址，但直接访问需要 Referer
- **频繁请求被封**：搜狗搜索间隔 3-5 秒
- **转载版内容可能有删减**：优先用微信原文，转载版做兜底
- **不要用 Node.js**：Python 脚本足够，避免 cheerio 依赖
- **save_to_feishu.py 不用**：飞书写入用 agent 原生工具（feishu_create_doc）

## 频率

Cron：每小时第22分钟（ID: de3ee2d3）
每次 1 个关键词，搜索 → 解析 → 评分 → 入库
