---
name: web-fetch
description: |
  网页数据采集技能。静态页用 requests+BeautifulSoup，JS 渲染页用 Playwright，自动尊重 robots.txt、轮换 User-Agent、限速，输出结构化 JSON/CSV。覆盖垂直领域采集、反爬应对、数据清洗与质量校验。适用于市场调研、竞品监控、公开数据聚合。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - scraping
  - 爬虫
  - web
  - 数据采集
  - playwright
---

# web-fetch — 网页数据采集台

_从"一次性 fragilescript"到"可恢复、结构化、守规矩"的采集流程。_

## 选型决策树（先选对工具，再写代码）

| 场景 | 工具 | 说明 |
|------|------|------|
| 静态 HTML（新闻/博客/Wiki/政府数据） | `requests` + `BeautifulSoup` + `lxml` | 快、轻、免费 |
| JS 渲染 SPA（React/Vue/Angular） | `Playwright`（真实 Chromium） | 等 JS 渲染后取 DOM |
| 大规模/分布式 | `Scrapy` | 内置并发、节流、管道 |
| 不想管浏览器基础设施 | 托管抓取 API | 远端跑 Chromium，返回渲染 HTML |

**黄金法则：先查目标站有没有公开 API**——更快、更稳、更合规。

## 标准工作流

### 1. 合规前置
```python
from urllib.robotparser import RobotFileParser
rp = RobotFileParser(); rp.set_url("https://example.com/robots.txt"); rp.read()
if not rp.can_fetch("*", url):  # 尊重 robots.txt
    ... # 换源或放弃
```
- 限速（同域请求间隔随机 1–3s）、不压垮服务器
- 只采公开数据，避开个人隐私/版权内容

### 2. 请求层（反爬基础）
- 真实 UA 轮换、Referer、合理 headers
- 会话复用（requests.Session）
- 异常重试 + 退避（网络/4xx/5xx）

### 3. 解析层
- CSS 选择器 / XPath 提取目标字段
- 结构化：每条记录 = 一个 dict，字段命名规范

### 4. 清洗与校验
- 数值范围校验（price>0）、文本长度限制、时间格式验证
- 用 pandas 批量去重、规整

### 5. 结构化输出
- JSON（嵌套）或 CSV（扁平），落盘到工作目录

## 脚本用法

```bash
# 静态页：提取所有 <a> 链接与标题
python scripts/scrape.py "https://news.ycombinator.com/" --select "span.titleline>a" --attr href --text

# 自定义字段（CSS 选择器 -> 字段名）
python scripts/scrape.py "https://example.com/products" \
  --field "title:.product-card h2" --field "price:.price"

# JS 渲染页（Playwright）
python scripts/scrape.py "https://spa.example.com/" --js --wait ".product-card"

# 输出到文件
python scripts/scrape.py "URL" --field "x:y" --out result.json

# 跳过 robots 检查（仅当你已获授权）
python scripts/scrape.py "URL" --no-robots
```

## 反爬应对（分级）
1. 轮换 UA + 随机延迟 + 会话管理 → 解决大部分基础拦截
2. Playwright + stealth 补丁 → 绕过 navigator.webdriver 等指纹检测
3. 住宅代理轮换 → 突破 IP 级封锁
4. 行为拟真（非均匀 timing、真实交互）→ 现代反爬看"行为"而非"速度"

## 自我进化学习系统

本技能用 `scripts/learner.py` 记录每次采集成败与高频失败模式（封禁类型、选择器失效等）：

```bash
python scripts/learner.py record <技能目录> --capability 反爬绕过 --note "目标站需Playwright+stealth"
python scripts/learner.py record <技能目录> --capability 选择器解析 --fail --error 选择器失效 --note "改版后 .price 变 .cost"
python scripts/learner.py insight <技能目录>
python scripts/learner.py reflect <技能目录>
```

记忆落盘 `learned_patterns.json`，跨会话积累，使本技能越用越抗变、越用越准。

## 安全边界
- 严守 robots.txt 与目标站 ToS；不采集个人信息、密级数据、版权内容。
- 默认限速，避免对目标站造成过大负载。
- 不将采集能力用于绕过付费墙或大规模攻击性抓取。
