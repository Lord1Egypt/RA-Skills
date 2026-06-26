---
name: wechat-article-digest
description: 微信公众号文章抓取、分类与日报生成。当用户发送公众号文章链接（mp.weixin.qq.com）、说"文章日报"、"今日阅读"、"归类一下"、"整理文章"、"帮我看看这篇文章"时触发。也用于用户日常转发文章链接时自动抓取摘要和分类。
allowed-tools: [exec, web_fetch, read, write, edit]
---

# 微信公众号文章日报

## 核心流程

### 1. 抓取文章内容

用户发送 `mp.weixin.qq.com/s/` 链接时：

```
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15" \
  "链接" \
  | python3 -c "
import sys, re
html = sys.stdin.read()
# 提取标题
t = re.search(r'var msg_title = \"(.*?)\";', html)
title = t.group(1) if t else ''
# 提取公号名
n = re.search(r'var nickname = \"(.*?)\";', html)
name = n.group(1) if n else ''
# 提取正文
m = re.search(r'id=\"js_content\"[^>]*>(.*?)</div>', html, re.DOTALL)
body = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else ''
print(f'TITLE:{title}')
print(f'NAME:{name}')
print(f'BODY:{body}')
"
```

如果标题和正文都为空，用 web_fetch 作为备选。

### 2. 分类标签体系

每篇文章分配 1-2 个标签：

- 🤖 AI/科技 — AI、大模型、技术产品
- 💰 商业/创业 — 创业、商业模式、融资
- 📈 职场/管理 — 职场经验、团队管理、效率
- 📊 行业分析 — 行业趋势、市场分析、竞品
- 🧠 个人成长 — 学习方法、思维方式、认知
- 💰 投资/理财 — 股市、基金、财务规划
- 🌍 宏观/政策 — 经济政策、国际局势
- 🎯 产品/设计 — 产品思维、用户体验
- 📖 读书/文化 — 书评、文化、人文
- 🔧 工具/效率 — 工具推荐、自动化、工作流
- ❤️ 健康/生活 — 健康、生活、情感

### 3. 单篇响应格式

用户发单篇链接时，立即响应：

```
📌 [标题]
📁 公号：[名称] | 标签：[标签]
📝 摘要：[1-2句话提炼核心观点]
```

同时将文章信息追加到 `memory/YYYY-MM-DD.md`。

### 4. 日报生成格式

当触发日报汇总时（定时任务或用户说"文章日报"），读取当天 memory 文件，生成：

```
📰 今日阅读日报 — YYYY-MM-DD

共 N 篇文章

[标签emoji] [标签名]（X篇）
├ 📌 标题1 — 公号名 | 一句话摘要
├ 📌 标题2 — 公号名 | 一句话摘要
└ ...

[标签emoji] [标签名]（X篇）
└ ...

💡 今日要点：
- [从所有文章中提炼 2-3 个值得关注的观点]
```

如果当天没有文章，回复 NO_REPLY。

### 5. 记录格式

在 `memory/YYYY-MM-DD.md` 中以如下格式记录每篇文章：

```markdown
## 公众号文章

- [标签emoji] **标题** — 公号名
  > 摘要内容
  > 链接：https://mp.weixin.qq.com/s/xxx
```

## 注意事项

- 正文超过 5000 字时，摘要控制在 3 句话以内，突出核心观点
- 如果抓取失败，告知用户并建议复制文字或截图
- 分类标签可扩展，遇到无法归类的文章放在「📌 其他」下
