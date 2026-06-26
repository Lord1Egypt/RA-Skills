# ZeeLin AI Twitter Creator Briefing Skill

**作者**: ZeeLin
**版本**: 1.0.0
**创建时间**: 2026-03-27

---

## Skill 描述

自动抓取指定AI博主Twitter内容，生成简报并发布到X的完整工作流。

### 核心功能

1. **推文抓取**: 抓取指定AI博主近10天的推文内容
2. **智能整理**: 去重、分类、提炼核心观点
3. **简报生成**: 生成结构化的中英文简报
4. **自动发布**: 提炼英文推文并发布到X
5. **多平台适配**: 支持扩展到小红书、公众号

### 适用场景

- AI领域信息聚合与过滤
- 博主内容追踪与整理
- 社交媒体自动化运营
- 行业趋势分析

---

## 触发条件

当用户提到以下关键词时激活本skill：

- "AI博主简报"、"推特博主简报"、"X博主简报"
- "抓取推文"、"整理Twitter"、"生成简报"
- "博主信息"、"AI大V内容"
- "ZeeLin简报"、"AI简报"
- 提到具体博主名称（如"吴恩达"、"Karpathy"等）+ "推文"

---

## 默认博主列表

### 英文顶级AI博主

- @AndrewYNg - 吴恩达（AI教育家，DeepLearning.AI创始人）
- @drfeifei - 李飞飞（斯坦福AI实验室主任）
- @karpathy - Andrej Karpathy（OpenAI创始成员，AI教育者）
- @ylecun - Yann LeCun（Meta AI首席科学家）

### 中文AI博主（精选）

- @zarazhangrui - 张咋啦（AI前沿分享）
- @dotey - 宝玉（AI工具与实践）
- @op7418 - Orange（AI产品与资讯）
- @ShunyuYao12 - 姚顺雨（AI研究与创业）
- @frxiaobei - 凡人小北（AI Agent实战）
- @FinanceYF5 - AI WILL（AI行业分析师）
- @MANISH1027512 - 古一（AI摄影师，Midjourney专家）
- @joshesye - 行者AI视频（北影节AIGC大奖得主）
- @zstmfhy - AI奶爸（万象AI实验室）
- @bozhou_ai - 泊舟（AI程序员，Vibe编码）
- @CuiMao - 崔毛（AI开发者）
- @RookieRicardoR - 耳朵（软件工程师，AI深度应用）
- @wlzh - M.（AI玩家）
- @cnyzgkc - 木马人（Claude实战）

---

## 配置文件

### 博主配置 (config/creators.yaml)

```yaml
# AI博主配置
creators:
  # 英文顶级博主
  - handle: "AndrewYNg"
    name: "吴恩达"
    tags: ["AI教育", "深度学习", "行业趋势"]
    priority: 1

  - handle: "drfeifei"
    name: "李飞飞"
    tags: ["计算机视觉", "AI研究", "学术界"]
    priority: 1

  - handle: "karpathy"
    name: "Andrej Karpathy"
    tags: ["AI教育", "编程", "Vibe Coding"]
    priority: 1

  - handle: "ylecun"
    name: "Yann LeCun"
    tags: ["Meta AI", "AI研究", "争议观点"]
    priority: 1

  # 中文AI博主
  - handle: "zarazhangrui"
    name: "张咋啦"
    tags: ["AI前沿", "工具分享", "实战"]
    priority: 2

  - handle: "dotey"
    name: "宝玉"
    tags: ["AI工具", "实战经验", "产品思考"]
    priority: 2

  - handle: "op7418"
    name: "Orange"
    tags: ["AI产品", "行业资讯", "OpenAI"]
    priority: 2

  - handle: "ShunyuYao12"
    name: "姚顺雨"
    tags: ["AI研究", "创业", "前沿技术"]
    priority: 2

  - handle: "frxiaobei"
    name: "凡人小北"
    tags: ["AI Agent", "工作流", "实战"]
    priority: 2

  - handle: "FinanceYF5"
    name: "AI WILL"
    tags: ["行业分析", "增长顾问", "AI前沿"]
    priority: 2

  - handle: "MANISH1027512"
    name: "古一"
    tags: ["AI摄影", "Midjourney", "AIGC"]
    priority: 3

  - handle: "joshesye"
    name: "行者AI视频"
    tags: ["AI视频", "AIGC", "教程"]
    priority: 3

  - handle: "zstmfhy"
    name: "AI奶爸"
    tags: ["AI漫画", "视频生成", "教程"]
    priority: 3

  - handle: "bozhou_ai"
    name: "泊舟"
    tags: ["AI编程", "提示词", "工作流"]
    priority: 3

  - handle: "CuiMao"
    name: "崔毛"
    tags: ["AI开发", "技术分享", "开发者"]
    priority: 3

  - handle: "RookieRicardoR"
    name: "耳朵"
    tags: ["AI应用", "跨领域", "深度思考"]
    priority: 3

  - handle: "wlzh"
    name: "M."
    tags: ["AI工具", "内容分享"]
    priority: 3

  - handle: "cnyzgkc"
    name: "木马人"
    tags: ["Claude", "AI实战", "大厂视角"]
    priority: 3

# 抓取配置
fetch:
  days: 10  # 抓取最近10天
  max_tweets_per_creator: 50  # 每个博主最多抓取50条

# 过滤配置
filter:
  min_likes: 5  # 最少点赞数
  min_retweets: 2  # 最少转发数
  exclude_keywords: ["广告", "推广", "AD"]  # 排除关键词

# 发布配置
publish:
  platforms: ["twitter"]  # 发布平台
  max_tweet_length: 280  # 推文最大长度
  include_hashtags: true  # 包含话题标签
  hashtags: ["#AI", "#OpenClaw", "#Agent"]  # 默认话题标签
```

---

## 工作流程

### 完整流程图

```
开始
  ↓
[步骤1] 加载博主列表
  ↓
[步骤2] 抓取推文内容 (近10天)
  ↓
[步骤3] 内容清洗与去重
  ↓
[步骤4] 分类与评分
  ↓
[步骤5] 生成简报 (Markdown)
  ↓
[步骤6] 提炼英文推文
  ↓
[步骤7] 发布到X
  ↓
[步骤8] 保存归档
  ↓
结束
```

### 详细步骤

#### 步骤1: 加载博主列表

```bash
# 从配置文件加载博主列表
openclaw task load-creators \
  --config config/creators.yaml \
  --output creators-list.json
```

**输出格式**:
```json
{
  "creators": [
    {
      "handle": "karpathy",
      "name": "Andrej Karpathy",
      "tags": ["AI教育", "编程"],
      "priority": 1
    }
  ],
  "total": 18
}
```

#### 步骤2: 抓取推文内容

```bash
# 使用agent-browser或Twitter API抓取推文
openclaw task fetch-tweets \
  --input creators-list.json \
  --days 10 \
  --max-tweets 50 \
  --output raw-tweets.json
```

**抓取策略**:
- 优先抓取高互动推文（点赞>5，转发>2）
- 排除广告和低质量内容
- 保留推文元数据（时间、URL、互动数据）

#### 步骤3: 内容清洗与去重

```bash
# 清洗推文内容
openclaw task clean-tweets \
  --input raw-tweets.json \
  --exclude-keywords "广告,推广,AD" \
  --deduplicate true \
  --output cleaned-tweets.json
```

**清洗规则**:
- 移除重复推文（相似度>90%）
- 移除包含推广关键词的推文
- 规范化文本（去除多余空格、换行）
- 提取关键信息（链接、提及、标签）

#### 步骤4: 分类与评分

```bash
# AI智能分类与评分
openclaw task score-tweets \
  --input cleaned-tweets.json \
  --model claude-3-opus \
  --output scored-tweets.json
```

**分类体系**:
- **技术研究**: 论文、模型、算法
- **工具分享**: 新工具、教程、实战
- **行业资讯**: 公司动态、产品发布
- **观点思考**: 行业观点、趋势预测
- **实战案例**: 应用案例、经验分享

**评分标准** (0-100分):
- 原创性 (30分)
- 实用性 (30分)
- 时效性 (20分)
- 互动数据 (20分)

#### 步骤5: 生成简报

```bash
# 生成结构化简报
openclaw task generate-briefing \
  --input scored-tweets.json \
  --template templates/briefing-template.md \
  --output "reports/x-creator-briefing-$(date +%Y-%m-%d).md"
```

**简报结构**:
```markdown
# X AI Creator Briefing - 2026-03-27

## 📊 本期概览

- 监控博主：18位
- 抓取推文：245条
- 高信号内容：32条
- 核心主题：5个

---

## 🔥 高信号主线

### 1. Vibe Coding到真实部署的DevOps落差
**来源**: @karpathy
**核心观点**: ...
**推文链接**: https://x.com/karpathy/status/...

---

## 📌 按博主分类

### @karpathy (Andrej Karpathy)
**标签**: AI教育、编程、Vibe Coding

#### ⭐ 高光推文 (3条)
1. **[Vibe Coding的本质]**
   - 发布时间: 2026-03-25
   - 互动数据: 👍 2.3K | 🔄 856 | 💬 234
   - 核心观点: Vibe coding不是偷懒，而是...

---

## 📚 资源推荐

### 工具/产品
- [新工具] OpenAI新功能...
- [教程] Karpathy的...

### 论文/文章
- [论文] ...
- [文章] ...

---

## 📊 数据统计

| 博主 | 推文数 | 高信号 | 主要话题 |
|------|--------|--------|----------|
| @karpathy | 15 | 8 | Vibe Coding |
| @zarazhangrui | 12 | 6 | AI工具 |
...

---

## ⚠️ 未抓到内容的博主

- @AndrewYNg (近10天无公开推文)
- @drfeifei (近10天无公开推文)
- @ShunyuYao12 (近10天无公开推文)

---

*生成时间: 2026-03-27*
*下次更新: 2026-03-28*
```

#### 步骤6: 提炼英文推文

```bash
# 提炼英文推文（280字符以内）
openclaw task refine-tweet \
  --input "reports/x-creator-briefing-2026-03-27.md" \
  --max-length 280 \
  --language en \
  --output tweet-refined.md
```

**推文模板**:
```
📊 AI Creator Briefing - [Date]

Top 3 Updates:
1. @karpathy: Vibe coding → DevOps reality gap
2. @zarazhangrui: Product ideas from play + talking
3. @dotey/op7418: OpenAI/Anthropic product shifts

🔗 Full briefing: [链接]

#AI #OpenClaw #Agent
```

#### 步骤7: 发布到X

```bash
# 发布到X（使用zeelin-twitter-web-autopost skill）
openclaw task tweet \
  --file tweet-refined.md \
  --platform twitter \
  --include-hashtags true
```

#### 步骤8: 保存归档

```bash
# 归档简报
openclaw task archive \
  --source "reports/x-creator-briefing-2026-03-27.md" \
  --destination "archive/briefings/2026/03/"
```

---

## 使用方法

### 方法1: 一键执行（推荐）

```bash
# 执行完整流程
openclaw skill run zeelin-x-creator-briefing \
  --config config/creators.yaml \
  --days 10 \
  --publish true
```

### 方法2: 分步执行

```bash
# 步骤1: 抓取推文
openclaw task fetch-tweets --config config/creators.yaml

# 步骤2: 生成简报
openclaw task generate-briefing --input raw-tweets.json

# 步骤3: 发布到X
openclaw task tweet --file briefing.md --publish true
```

### 方法3: 定时任务

```bash
# 每天早上8点执行
openclaw cron add "AI Creator Briefing" "0 8 * * * openclaw skill run zeelin-x-creator-briefing --config config/creators.yaml --publish true"
```

---

## 高级功能

### 1. 自定义博主列表

```bash
# 使用自定义博主列表
openclaw skill run zeelin-x-creator-briefing \
  --creators karpathy,zarazhangrui,dotey \
  --days 7 \
  --publish true
```

### 2. 中英文双语简报

```bash
# 生成中英文双语版本
openclaw skill run zeelin-x-creator-briefing \
  --languages zh,en \
  --output-format bilingual
```

### 3. 多平台发布

```bash
# 发布到多个平台
openclaw skill run zeelin-x-creator-briefing \
  --publish-to twitter,xiaohongshu,zhihu \
  --platform-config config/platforms.yaml
```

### 4. 自定义过滤规则

```bash
# 使用自定义过滤规则
openclaw skill run zeelin-x-creator-briefing \
  --filter-min-likes 10 \
  --filter-min-retweets 5 \
  --filter-exclude "广告,推广,AD"
```

---

## 扩展功能

### 扩展1: 生成中文长文版本

```bash
# 压缩成媒体报道风格的中文长文
openclaw task generate-article \
  --input "reports/x-creator-briefing-2026-03-27.md" \
  --style media-report \
  --output "articles/ai-creator-weekly-2026-03-27.md"
```

**文章结构**:
- 标题：《AI博主本周都在关注什么？Karpathy谈Vibe Coding，张咋啦分享产品灵感》
- 导语：本周核心趋势总结
- 正文：按主题深度展开
- 结语：下周关注点预测

### 扩展2: 小红书版本

```bash
# 生成小红书版本
openclaw task generate-xiaohongshu \
  --input "reports/x-creator-briefing-2026-03-27.md" \
  --style xiaohongshu \
  --output "xiaohongshu/ai-creator-briefing-2026-03-27.md"
```

**小红书风格**:
- 标题：🔥AI圈本周大事件！Karpathy又双叒叕发新观点了！
- 正文：emoji丰富，段落简短
- 标签：#AI #人工智能 #Karpathy #科技前沿

### 扩展3: 公众号版本

```bash
# 生成公众号版本
openclaw task generate-wechat \
  --input "reports/x-creator-briefing-2026-03-27.md" \
  --style wechat-official \
  --output "wechat/ai-creator-weekly-2026-03-27.md"
```

**公众号风格**:
- 标题：《AI博主周报 | Karpathy谈Vibe Coding，张咋啦分享产品灵感来源》
- 导语：本周AI圈发生了什么？
- 正文：深度分析，配图建议
- 结语：互动提问

---

## 定时任务配置

### Cron配置示例

```cron
# 每天早上8点执行
0 8 * * * openclaw skill run zeelin-x-creator-briefing --config config/creators.yaml --publish true

# 每周一早上9点生成周报
0 9 * * 1 openclaw skill run zeelin-x-creator-briefing --config config/creators.yaml --days 7 --report-type weekly

# 每月1号生成月报
0 10 1 * * openclaw skill run zeelin-x-creator-briefing --config config/creators.yaml --days 30 --report-type monthly
```

---

## 文件结构

```
~/.openclaw/workspace/skills/zeelin-x-creator-briefing/
├── SKILL.md                          # 本文件
├── config/
│   ├── creators.yaml                 # 博主配置
│   ├── platforms.yaml                # 平台配置
│   └── filters.yaml                  # 过滤规则配置
├── templates/
│   ├── briefing-template.md          # 简报模板
│   ├── tweet-template.txt            # 推文模板
│   ├── article-template.md           # 文章模板
│   └── xiaohongshu-template.md       # 小红书模板
├── scripts/
│   ├── fetch-tweets.sh               # 抓取脚本
│   ├── clean-tweets.sh               # 清洗脚本
│   ├── score-tweets.sh               # 评分脚本
│   ├── generate-briefing.sh          # 生成简报脚本
│   └── publish.sh                    # 发布脚本
├── reports/
│   └── x-creator-briefing-YYYY-MM-DD.md  # 简报输出
├── archive/
│   └── briefings/
│       └── YYYY/
│           └── MM/
└── logs/
    └── zeelin-x-creator-briefing.log
```

---

## 依赖技能

本skill依赖以下OpenClaw技能：

1. **agent-browser**: 浏览器自动化，用于抓取Twitter内容
2. **zeelin-twitter-web-autopost**: Twitter自动发布
3. **zeelin-writing**: 文章生成
4. **zeelin-xiaohongshu-autopost**: 小红书自动发布（可选）
5. **zeelin-zhihu-autopost**: 知乎自动发布（可选）

---

## 注意事项

### 账号安全

- ⚠️ 避免频繁请求Twitter API，可能触发限流
- ⚠️ 控制抓取频率，建议每小时不超过100次请求
- ⚠️ 使用代理池分散请求，降低封号风险
- ⚠️ 发布推文时，避免短时间内大量操作

### 内容质量

- ✅ 定期检查过滤规则，优化内容质量
- ✅ 人工审核高信号内容，确保准确性
- ✅ 定期更新博主列表，移除不活跃账号
- ✅ 关注用户反馈，调整评分标准

### 性能优化

- 💡 使用增量抓取，只抓取新内容
- 💡 缓存博主信息，减少重复请求
- 💡 并行抓取多个博主，提升效率
- 💡 定期清理旧数据，节省存储空间

---

## 更新日志

### v1.0.0 (2026-03-27)

**初始版本发布**

**功能**:
- ✅ 支持18位AI博主
- ✅ 抓取近10天推文
- ✅ 生成结构化简报
- ✅ 自动发布到X
- ✅ 支持中英文双语

**已知问题**:
- 部分博主可能抓取不到内容（隐私设置或未发推）
- 推文链接可能失效（博主删除或设为私密）

**下一步计划**:
- [ ] 添加图片和视频抓取
- [ ] 支持Thread抓取
- [ ] 添加AI摘要生成
- [ ] 支持自定义评分权重
- [ ] 添加数据可视化

---

## 技术支持

**问题反馈**: 在OpenClaw Discord社区提issue
**功能建议**: 欢迎提出改进建议
**贡献代码**: 欢迎提交PR

---

*SKILL.md 创建时间: 2026-03-27*
*最后更新: 2026-03-27*
*维护者: ZeeLin*
