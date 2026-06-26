---
name: weekly-ai-news
description: 每周AI前沿动态生成工具。自动抓取 RSS 订阅源的 AI 新闻，筛选应用向内容（剔除技术性太高的内容），生成旧报纸风格的 HTML 简报，支持发送到飞书。使用场景：每周一自动/手动生成上周 AI 应用动态周报，以复古报纸形式呈现并推送到飞书。
metadata:
  openclaw:
    requires:
      bins: [python3, bash]
---

# 每周AI前沿动态

自动抓取、筛选、生成 AI 应用新闻周报，以旧报纸风格呈现，支持发送到飞书。

## 订阅源

- 阮一峰的网络日志: https://www.ruanyifeng.com/blog/atom.xml
- 36氪: https://36kr.com/feed
- 虎嗅科技: https://www.huxiu.com/rss/0.xml
- 钛媒体: https://www.tmtpost.com/rss.xml
- IT之家: https://www.ithome.com/rss/

## 功能

1. **RSS 抓取** - 自动获取订阅源最新内容
2. **智能筛选** - 识别 AI 相关内容，过滤纯技术文章
3. **应用导向** - 优先保留产品发布、商业动态、市场趋势等内容
4. **复古风格** - 生成旧报纸风格的 HTML 简报
5. **飞书推送** - 生成格式化消息，支持发送到飞书

## 使用方法

### 快速生成

```bash
weekly-ai-news
```

生成到默认目录 `~/weekly-ai-news/`

### 指定输出目录

```bash
weekly-ai-news /path/to/output
```

### 指定天数范围

```bash
weekly-ai-news ~/weekly-ai-news 7
```

### 生成并发送飞书消息

```bash
# 生成后会提示如何发送
weekly-ai-news ~/weekly-ai-news 7 --send

# 或者使用 openclaw 命令直接发送
weekly-ai-news ~/weekly-ai-news 7 && openclaw message send "$(cat ~/weekly-ai-news/message.txt)"
```

### 手动分步执行

```bash
# 1. 抓取 RSS（过去7天）
python3 ~/.openclaw/skills/weekly-ai-news/scripts/fetch_rss.py --days 7 > news.json

# 2. 生成 HTML
python3 ~/.openclaw/skills/weekly-ai-news/scripts/generate_newspaper.py \
    --input news.json \
    --output weekly-ai-news.html

# 3. 格式化飞书消息
python3 ~/.openclaw/skills/weekly-ai-news/scripts/format_feishu_msg.py \
    --news-json news.json \
    --html-file weekly-ai-news.html > message.txt
```

## 筛选逻辑

**保留（应用向）：**
- 产品发布、上线
- 融资、投资、并购
- 商业合作、战略
- 市场趋势、用户增长
- 政策法规、监管动态

**过滤（技术向）：**
- 算法原理、模型训练
- 神经网络架构
- 技术实现细节
- 参数调优、论文解读

## 输出文件

- `news.json` - 原始新闻数据（JSON 格式）
- `weekly-ai-news.html` - 旧报纸风格 HTML 简报
- `message.txt` - 飞书消息文本（使用 --send 时生成）

## 旧报纸风格特点

- 泛黄纸张纹理背景
- 经典衬线字体（Noto Serif SC）
- 多栏排版（双栏布局）
- 首字下沉装饰
- 头条新闻突出显示
- 复古色调与边框

## 飞书消息格式

自动生成的飞书消息包含：
- 周报标题和期号
- 头条新闻突出显示
- 其他新闻列表（最多5条）
- 来源和日期信息
- HTML文件路径提示

## 自动化建议

添加到 crontab 每周一自动执行：

```bash
# 每周一上午9点自动生成并发送
0 9 * * 1 /usr/local/bin/weekly-ai-news ~/weekly-ai-news 7 --send
```

或在 OpenClaw 中设置定时任务：

```bash
openclaw cron add --name "weekly-ai-news" \
  --schedule "0 9 * * 1" \
  --command "weekly-ai-news ~/weekly-ai-news 7 --send"
```
