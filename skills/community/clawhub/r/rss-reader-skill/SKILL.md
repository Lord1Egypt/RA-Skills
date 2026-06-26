---
name: rss-reader
description: >
  RSS 订阅 + AI 汇总分析 + 飞书推送。
  定时拉取新文章，AI 生成每日资讯汇总报告（热门话题、关键趋势、推荐阅读），推送到飞书。
  当用户提到"RSS"、"订阅"、"RSS阅读器"、"文章订阅"、"资讯订阅"、"资讯汇总"时使用此 Skill。
  首次使用自动添加 18 个精选订阅源（中文 + 国外 AI + 科技媒体）。
---

# RSS Reader + AI Summary

> 📰 RSS 订阅 + AI 汇总分析 + 飞书推送
> 
> 首次使用自动添加 18 个精选订阅源，自动生成每日资讯汇总报告！

---

## ⚠️ 首次使用必读

**🚨 重要：此 Skill 默认无法使用，必须配置 API Key！**

在使用此 Skill 之前，**必须配置以下环境变量**：

### 1️⃣ AI 汇总 API（必需）

**默认不支持任何 API，必须手动配置！**

用于生成每日资讯汇总报告（热门话题、关键趋势、推荐阅读）。

#### 推荐方案：智谱 AI（国内稳定）

```bash
# 1. 获取 API Key：https://open.bigmodel.cn/
# 2. 在 Gateway 配置中添加：
export OPENAI_API_KEY="你的智谱API Key"
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
```

#### 备选方案：OpenAI

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

**💡 智谱 AI 优势：**
- ✅ 国内访问稳定
- ✅ 价格便宜（glm-4-flash: 0.1元/百万tokens）
- ✅ 中文效果好
- ✅ 免费额度充足

**获取智谱 API Key：** https://open.bigmodel.cn/

---

### 2️⃣ 飞书推送（可选）

用于推送每日汇总报告到飞书群。

```bash
# 国内版
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 国际版（Lark）
export FEISHU_WEBHOOK_URL="https://open.larksuite.com/open-apis/bot/v2/hook/xxx"
```

**获取飞书 Webhook：**
1. 在飞书群中添加「自定义机器人」
2. 复制 Webhook 地址

---

### 3️⃣ 配置方法

在 Gateway 配置文件 `~/.openclaw/gateway/.env` 中添加：

```bash
# AI 汇总（智谱）
OPENAI_API_KEY=你的API Key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# 飞书推送（可选）
FEISHU_WEBHOOK_URL=你的Webhook地址
```

然后重启 Gateway：
```bash
openclaw gateway restart
```

---

## 📖 使用方法

### 命令列表

```bash
# 订阅管理
订阅 <url> [名称]     添加 RSS 订阅
取消订阅 <url>        取消订阅
订阅列表              查看所有订阅

# 刷新和汇总
立即刷新              检查新文章 + 自动生成汇总报告
汇总                  手动生成汇总报告
```

### 示例

```bash
# 添加订阅
订阅 https://www.ruanyifeng.com/blog/atom.xml 阮一峰

# 查看订阅列表
订阅列表

# 刷新并生成汇总报告
立即刷新

# 手动生成汇总报告
汇总
```

---

## ✨ 核心功能

### 1️⃣ 自动添加订阅源

首次使用自动添加 **18 个精选订阅源**：

**中文源（8 个）：**
- 阮一峰博客、V2EX、少数派、36氪、虎嗅、InfoQ 中文、IT之家、开源中国

**国外 AI（4 个）：**
- Anthropic Blog、OpenAI Blog、Google DeepMind、Google AI Blog

**国外科技媒体（4 个）：**
- TechCrunch、The Verge、Wired、Ars Technica

**国外开发者（3 个）：**
- GitHub Blog、Hacker News、Product Hunt

**国外商业（2 个）：**
- Harvard Business Review、The Economist

---

### 2️⃣ 每日资讯汇总报告 ⭐

每次刷新后自动生成 AI 分析报告，包含：

**📊 报告内容：**
- 🔥 **热门话题**：3-5 个最热门的科技话题
- 💡 **关键趋势**：2-3 条技术/行业趋势分析
- 📌 **推荐阅读**：3-5 篇最值得阅读的文章
- 🎯 **一句话总结**：今天的主要资讯概括
- 📚 **原文链接**：所有文章的原始链接列表

**示例报告：**

```
# 📊 每日资讯汇总

## 🔥 热门话题
1. Apple 宣布下调中国区 App Store 佣金率
2. 小红书率先向AI托管账号出手
3. AWE 2026携重磅阵容，MOVA全面披露芯片战略

## 💡 关键趋势
1. 科技产品佣金调整趋势明显
2. 社交媒体对AI的监管与应对
3. 芯片技术的快速发展与应用

## 📌 推荐阅读
1. Apple 宣布下调中国区 App Store 佣金率
2. 小红书率先向AI托管账号出手
3. AWE 2026携重磅阵容，MOVA全面披露芯片战略

## 🎯 一句话总结
今日科技资讯聚焦于科技产品佣金调整、社交媒体AI监管以及芯片技术发展。

---

## 📚 原文链接

1. [一日一技｜在镜头前翻翻页，你就得到了一本电子书](https://sspai.com/post/106935)
2. [314 周年庆：少数派软件、会员、栏目限时优惠](https://sspai.com/post/107091)
3. [派早报：Apple 宣布下调中国区 App Store 佣金率](https://sspai.com/post/107158)
...（最多 20 个链接）
```

---

### 3️⃣ 飞书推送

- ✅ 自动推送每日汇总报告到飞书群
- ✅ 美化的消息卡片
- ✅ 支持国内版和国际版（Lark）

---

### 4️⃣ 定时刷新

建议配置 OpenClaw 定时任务，每 2 小时自动刷新：

```bash
openclaw cron add \
  --name "rss-refresh" \
  --every "2h" \
  --session main \
  --system-event "[RSS刷新] 请立即执行：python3 ~/.agents/skills/rss-reader/rss_reader.py 立即刷新。执行完后回复 NO_REPLY。不要删除任何 cron 任务。"
```

---

## 🔧 技术细节

### 工作流程

1. **刷新订阅**：检查所有 RSS 源的新文章
2. **记录文章**：保存文章标题、链接、来源
3. **AI 分析**：调用智谱 AI 生成汇总报告
4. **推送飞书**：发送汇总报告 + 原文链接

### 与传统 RSS 阅读器的区别

| 功能 | 传统 RSS | RSS Reader Skill |
|------|----------|------------------|
| 订阅管理 | ✅ | ✅ |
| 定时刷新 | ✅ | ✅ |
| 单篇摘要 | ✅ | ❌（已移除） |
| AI 汇总分析 | ❌ | ✅ ⭐ |
| 趋势分析 | ❌ | ✅ ⭐ |
| 推荐阅读 | ❌ | ✅ ⭐ |
| 原文链接 | ❌ | ✅ ⭐ |
| 飞书推送 | ❌ | ✅ ⭐ |

**设计理念：**
- ❌ 不做单篇摘要（避免大量 API 调用和错误信息）
- ✅ 只做汇总分析（一次 API 调用，生成高质量报告）
- ✅ 提供原文链接（用户可自行选择阅读）

---

## 🚨 常见问题

### 1. 提示 "未配置 OPENAI_API_KEY"

**原因：** 未配置 AI API Key

**解决：**
```bash
# 获取智谱 API Key：https://open.bigmodel.cn/
export OPENAI_API_KEY="你的Key"
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"

# 重启 Gateway
openclaw gateway restart
```

### 2. 生成报告失败

**可能原因：**
- API Key 无效或过期
- API 余额不足
- 网络问题

**解决：**
1. 检查 API Key 是否正确
2. 检查 API 余额（智谱控制台）
3. 尝试使用 OpenAI 备选方案

### 3. 飞书推送失败

**可能原因：**
- Webhook 地址错误
- 机器人被移除

**解决：**
1. 检查 Webhook 地址
2. 在飞书群中重新添加机器人

### 4. 某些订阅源无法访问

**可能原因：**
- 网络限制（部分国外源）
- RSS 地址失效

**解决：**
1. 取消订阅失效源：`取消订阅 <url>`
2. 手动添加新的订阅源

---

## 📦 依赖

**Python 包：**
- `feedparser>=6.0.0` - RSS 解析
- `requests>=2.28.0` - HTTP 请求

**安装：**
```bash
pip3 install -r requirements.txt
```

---

## 📄 协议

MIT License

---

## 🙏 致谢

感谢以下项目：
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS 解析
- [智谱 AI](https://open.bigmodel.cn/) - AI 分析服务

---

## 📮 反馈

如有问题或建议，请访问：
- GitHub Issues: [项目地址]
- ClawHub: https://clawhub.com

---

**⚠️ 再次提醒：此 Skill 默认不可用，必须配置 API Key！**
# 1. 在飞书群添加「自定义机器人」
# 2. 复制 Webhook 地址
# 3. 在 Gateway 配置中添加：
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

**获取飞书 Webhook：**
1. 打开飞书群聊
2. 点击群设置 → 群机器人 → 添加机器人
3. 选择「自定义机器人」
4. 复制 Webhook 地址

---

### 3️⃣ 重启 Gateway

配置完成后，**必须重启 Gateway**：

```bash
openclaw gateway restart
```

---

## 🚫 常见错误

### ❌ 401 错误：令牌已过期或验证不正确

**原因：** 未配置 API Key 或 API Key 无效

**解决：**
1. 确认已在 `~/.openclaw/gateway/.env` 中配置 `OPENAI_API_KEY`
2. 确认 API Key 正确且未过期
3. 重启 Gateway：`openclaw gateway restart`

---

## 功能

| 功能 | 说明 |
|------|------|
| 订阅管理 | 添加/删除/查看 RSS 订阅 |
| 自动刷新 | 定时拉取新文章（每 2 小时） |
| AI 摘要 | 智谱 AI 生成文章摘要 |
| **每日汇总** | **AI 分析所有文章，生成趋势报告** |
| 飞书推送 | 新文章 + 汇总报告自动推送 |
| 默认订阅 | 首次使用自动添加 18 个精选源 |

---

## 默认订阅源

首次使用自动添加 **18 个精选订阅源**：

### 中文源（7 个）

| 名称 | 分类 | RSS 地址 |
|------|------|---------|
| 阮一峰博客 | 技术 | https://www.ruanyifeng.com/blog/atom.xml |
| V2EX | 社区 | https://www.v2ex.com/index.xml |
| 少数派 | 科技 | https://sspai.com/feed |
| 36氪 | 商业 | https://36kr.com/feed |
| 虎嗅 | 商业 | https://www.huxiu.com/rss/0.xml |
| InfoQ 中文 | 技术 | https://www.infoq.cn/feed |
| 开源中国 | 技术 | https://www.oschina.net/news/rss |

### 国外源 - AI（4 个）

| 名称 | 分类 | RSS 地址 |
|------|------|---------|
| Anthropic Blog | AI | https://www.anthropic.com/news/rss |
| OpenAI Blog | AI | https://openai.com/blog/rss.xml |
| Google DeepMind | AI | https://deepmind.google/discover/blog/rss/ |
| Google AI Blog | AI | https://blog.google/technology/ai/rss/ |

### 国外源 - 科技媒体（4 个）

| 名称 | 分类 | RSS 地址 |
|------|------|---------|
| TechCrunch | Tech | https://techcrunch.com/feed/ |
| The Verge | Tech | https://www.theverge.com/rss/index.xml |
| Wired | Tech | https://www.wired.com/feed/rss |
| Ars Technica | Tech | https://arstechnica.com/feed/ |

### 国外源 - 开发者（3 个）

| 名称 | 分类 | RSS 地址 |
|------|------|---------|
| GitHub Blog | Dev | https://github.blog/feed/ |
| Hacker News | Dev | https://hnrss.org/frontpage |
| Product Hunt | Product | https://www.producthunt.com/feed |

---

## 命令

### 1️⃣ 订阅管理

```bash
# 添加订阅
订阅 <url> [名称]

# 取消订阅
取消订阅 <url>

# 查看订阅列表
订阅列表
```

### 2️⃣ 刷新和汇总

```bash
# 立即刷新 + 自动生成汇总报告
立即刷新

# 手动生成汇总报告
汇总
```

---

## 使用示例

### 示例 1：首次使用

```bash
# 1. 配置 API Key（必须）
export OPENAI_API_KEY="your-zhipu-api-key"
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 2. 重启 Gateway
openclaw gateway restart

# 3. 运行 Skill（自动添加 18 个默认订阅）
python3 ~/.agents/skills/rss-reader/rss_reader.py 订阅列表
```

### 示例 2：添加自定义订阅

```bash
python3 ~/.agents/skills/rss-reader/rss_reader.py 订阅 https://example.com/feed.xml "我的博客"
```

### 示例 3：刷新并生成汇总

```bash
python3 ~/.agents/skills/rss-reader/rss_reader.py 立即刷新

# 输出：
# 🔄 开始刷新 18 个订阅...
# 📡 检查：阮一峰博客
#   📄 发现 3 篇新文章
#   ✅ 已推送到飞书
# ...
# ✅ 刷新完成，发现 30 篇新文章
# 
# 📊 正在生成汇总分析报告...
# ✅ 汇总分析报告生成成功
# ✅ 汇总报告已推送到飞书
```

---

## 汇总分析报告示例

```markdown
# 📊 每日资讯汇总（2024-03-13）

## 🔥 热门话题
- **AI Agent 生态** - OpenAI、Claude、Gemini 相继推出 Agent 功能
- **开源模型崛起** - Llama 3、Mistral 等开源模型性能逼近闭源
- **AI 编程工具** - Cursor、Copilot、Codeium 竞争激烈

## 💡 关键趋势
1. **AI Agent 正在从玩具变工具** - 越来越多的企业开始用 Agent 自动化工作流
2. **开源模型质量提升** - 本地部署 AI 成为可能，隐私和成本优势明显
3. **AI 辅助编程成为标配** - 不用 AI 编程工具的程序员将落后

## 📌 推荐阅读
1. **OpenAI 推出 Agent SDK** - 企业级 Agent 开发平台
2. **Llama 3 性能评测** - 开源模型的新标杆
3. **Cursor vs Copilot 深度对比** - AI 编程工具选型指南

## 🎯 一句话总结
AI Agent 和开源模型是今天的主旋律，编程工具的 AI 化已成定局。
```

---

## 定时任务

默认已配置每 2 小时自动刷新：

```bash
# 查看定时任务
openclaw cron list

# 手动触发
openclaw cron run rss-refresh
```

---

## 文件结构

```
~/.agents/skills/rss-reader/
├── SKILL.md              # Skill 说明文档
├── rss_reader.py         # 主脚本
├── requirements.txt      # 依赖（feedparser, requests）
├── README.md             # 使用说明
└── data/
    ├── subscriptions.json    # 订阅列表
    └── articles.json         # 已读文章记录
```

---

## 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `OPENAI_API_KEY` | ✅ 必需 | 智谱/OpenAI API Key |
| `OPENAI_BASE_URL` | 推荐 | API 地址（默认智谱） |
| `FEISHU_WEBHOOK_URL` | 可选 | 飞书推送 Webhook |

---

## 常见问题

### Q1: 为什么没有 AI 摘要？

**A:** 未配置 API Key。请按上述步骤配置 `OPENAI_API_KEY`。

### Q2: 为什么推送失败？

**A:** 未配置飞书 Webhook 或 Webhook 地址错误。请检查 `FEISHU_WEBHOOK_URL`。

### Q3: 某些订阅源解析失败？

**A:** 部分 RSS 源可能无法访问或格式不标准。可以取消订阅该源：

```bash
python3 ~/.agents/skills/rss-reader/rss_reader.py 取消订阅 <url>
```

### Q4: 如何清空已读记录？

```bash
echo '{}' > ~/.agents/skills/rss-reader/data/articles.json
```

---

## 更新日志

### v1.1.0 (2024-03-13)
- ✨ 新增每日汇总分析功能
- ✨ 刷新后自动生成并推送汇总报告
- 🔧 改进批量摘要逻辑
- 📝 更新文档，强调必须配置 API Key

### v1.0.0 (2024-03-13)
- 🎉 初始版本
- ✅ RSS 订阅管理
- ✅ AI 摘要（智谱/OpenAI）
- ✅ 飞书推送
- ✅ 18 个默认订阅源
- ✅ 定时任务（每 2 小时）

---

## 技术栈

- **语言：** Python 3
- **RSS 解析：** feedparser
- **HTTP 请求：** requests
- **AI 模型：** 智谱 glm-4-flash（推荐）/ OpenAI gpt-4o-mini
- **推送：** 飞书 Webhook

---

## 反馈与支持

如有问题或建议，请联系 Skill 作者或在 ClawHub 提交 Issue。

---

**享受智能资讯聚合！📰✨**
