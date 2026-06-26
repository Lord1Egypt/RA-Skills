---
name: x-profile-deep-dive
version: 1.0.0
description: >
  深度分析 X/Twitter 用户画像——通过 tweety-ns 抓取推文、关注和粉丝，
  生成中文深度档案（主题分类、内容风格、社交网络）。
  Use when: (1) 用户说"深挖 @xxx"/"分析这个博主"/"analyze @xxx",
  (2) 用户说"看看他都发了什么"/"这个人什么水平"/"值不值得关注",
  (3) 用户说"扒一扒 @xxx"/"做个 X 账号档案",
  (4) 用户要求了解某个 Twitter 博主的内容、风格、影响力。
  NOT for: 单条推文翻译/讨论（直接处理）、
  X 信息流日报/digest（用 x-digest cron 任务）、
  发推/点赞/互动操作（用浏览器手动）。
  Requires tweety-ns and Twitter cookies.
---

# X Profile Deep Dive

对 X/Twitter 博主进行深度画像分析：数据采集 → LLM 动态分类 → 摘要卡片 + 分类全集输出。

## 前置条件

```bash
# 一次性检查三个条件
pip3 show tweety-ns >/dev/null 2>&1 && echo "✅ tweety-ns" || echo "❌ pip3 install tweety-ns"
[ -f <WORKSPACE>/config/twitter_cookies.json ] && echo "✅ cookies" || echo "❌ cookies 缺失"
[ -d <WORKSPACE>/config/tw_session/ ] && echo "✅ session" || echo "❌ session 目录缺失"
```

Cookies 缺失 → 提示用户通过 CDP 从 openclaw browser 提取。

## 预计耗时

| 阶段 | 耗时 | 说明 |
|------|------|------|
| Phase 1 数据采集 | 1-2 分钟 | tweety-ns API 调用 |
| Phase 1.5 Articles | 2-5 分钟 | 浏览器滚动，视博主文章数量而定 |
| Phase 2-3 分析+分类 | 1-3 分钟 | 视推文数量而定 |
| Phase 4-5 输出 | 1 分钟 | 文件写入+汇报 |
| **总计** | **5-11 分钟** | |

**确认点**：开始前告知用户预计耗时，确认后再开始。

## 完整流程

### Phase 1: 数据采集

运行脚本采集原始数据：

```bash
python3 scripts/x_profile_analyzer.py \
  --handle {handle} \
  --tweet-pages 8 \
  --cookies <WORKSPACE>/config/twitter_cookies.json \
  --output /tmp/x-profile-raw-{handle}.json
```

参数说明：
- `--tweet-pages 8`：默认 8 页（约 160 条推文），可根据需要调整
- `--following-pages 1`：关注列表采样 70 人（通常够用）
- `--follower-pages 1`：粉丝采样 70 人（可能因 elevated auth 失败，非关键）

脚本退出码：1=cookies missing, 2=login failed, 3=user not found

### Phase 1.5: Articles 专项采集 + 外链探索

**tweety-ns 的 tweet pages 可能采不全 X Articles（长文），且博主可能在外部平台有独占内容。此步骤必须执行。**

#### 1.5.1 X Articles 完整采集

用浏览器打开 `x.com/{handle}/articles`，完整滚动收集所有 Article：

1. `browser navigate` → `x.com/{handle}/articles`
2. **逐段滚动**（每次 `scrollBy(0, 1500)`），每段做 snapshot 记录当前可见的 article 标题+日期+URL
3. **累计去重**：X 使用虚拟滚动（virtual scrolling），会回收不在视口的 DOM 节点。**绝不能用最后一次 snapshot 的 article 数量当总数**。必须在脑中/笔记中累计所有已看到的唯一 article
4. 持续滚动直到**不再出现新 article**（连续 2 次滚动无新增 = 到底）
5. 记录总数，与 Phase 1 采到的 Articles 数量对比，补全遗漏

⚠️ **虚拟滚动陷阱**（2026-03-16 教训）：
- X 的 timeline 页面使用虚拟滚动，视口外的 article 元素会被回收
- `document.querySelectorAll('article').length` 只返回当前 DOM 中的数量，不是总数
- 必须逐段滚动 + 手动累计去重，这是唯一可靠的计数方式

#### 1.5.2 外链探索

检查博主 bio 中的外部链接（博客/Substack/Medium/Newsletter/GitHub）：

1. 从 Phase 1 的 profile 数据或 README 中提取 bio 链接
2. 如果有博客/Newsletter → 用 browser 打开，找到长文列表页
3. 对比博客长文列表 vs X Articles 列表，识别**博客独占内容**（博客有但 X 没有的）
4. 对博客独占文章快速评估：深度原创 or 短新闻/聚合帖？主题相关度？
5. 在 README.md 中增加「📎 外部平台」章节，记录博客 URL + 独占内容数量 + 推荐收藏清单

### Phase 2: 数据分析

读取输出的 JSON，用 Python 提取关键统计信息（参考 [data-analysis.md](references/data-analysis.md)）：
- 推文总数、时间跨度、发帖频率
- 互动中位数（likes/retweets/views）
- 语言分布、原创 vs 转推比例
- 高互动推文 Top 10

**确认点（大 V 场景）**：推文 >500 条时，告知用户分析范围（如"分析最近 160 条，覆盖约 X 天"），确认是否需要扩大采样。

### Phase 3: LLM 动态分类

**核心步骤**——不使用预设分类，而是根据推文内容动态生成分类。

1. 扫描所有推文全文，识别 3-6 个主题分类
2. 每个分类需要：名称（中文）、一句话描述、包含哪些推文
3. 分类原则：
   - 按内容主题而非形式分（不要"长文"/"短文"这种分法，除非某人确实有独特的长文系列）
   - **X Articles（长文）优先处理**：如果博主有 X Articles，先从 Phase 1.5 的完整 Articles 列表中提取，确保每篇 Article 全文都被收录到对应主题分类中。Articles 是博主最有深度的内容，不能遗漏
   - 如果某人有明显的长篇深度文章（>2000字），单独分一类「深度长文」
   - 每个分类至少 3 条推文，否则合并到相近分类
   - 一条推文只归入一个最匹配的分类
4. 对每条推文的分类排序：按 likes 降序

### Phase 4: 生成输出文件

输出结构为一个目录，包含摘要卡片 + 分类全集：

```
collections/x-profiles/@{handle}/
├── README.md          ← 摘要卡片 + 目录导航表
├── {category-1}.md    ← 第一个主题分类（推文全文）
├── {category-2}.md    ← 第二个主题分类
├── ...
└── network.md         ← 社交网络分析
```

#### README.md 格式

参考 [readme-template.md](references/readme-template.md)。包含：
- 📂 内容全集导航表（分类名 + 数量 + 一句话说明）
- 一句话概括
- 基本信息表
- 内容风格
- 高互动推文 Top 10（一行摘要 + 链接）
- 核心话题 Top 5
- 互动圈
- 关注列表分析（兴趣图谱）
- 与我们的关联度（⭐评分）
- 趋势判断

#### 分类文件格式

每个分类文件：
```markdown
# {分类名}

> {分类描述}

共 N 条推文

---

## [X,XXX❤️ X,XXX🔁 X,XXX,XXX👁] YYYY-MM-DD

[原文链接](url)

{推文全文，原样保留，不做任何压缩或摘要}

**附带链接**: {如果有}

---
```

**关键原则：推文全文原样保留，不做压缩。**

#### network.md 格式

参考 [network-template.md](references/network-template.md)。包含：
- 关注列表分类表格（Handle / 名称 / 粉丝 / 简介）
- 网络特征分析

### Phase 5: 验证 + 汇报

**自检**：
- 所有分类文件中的推文总数 = Phase 1 采集总数（不遗漏）
- X Articles 全量收录（Phase 1.5 计数 = 分类文件中 Articles 数）
- 每个分类 ≥3 条推文

完成后向用户汇报：
- 输出目录位置和文件结构
- 几个关键发现/亮点
- **数据完整性校验**：
  - X Articles 总数（Phase 1.5 实际计数） vs 分类文件中收录的 Articles 数量 → 必须一致
  - 如果有博客等外部平台，报告独占内容数量和推荐收藏清单
  - 采样覆盖范围说明（如"最近 N 条推文，约 X 天；Articles 全量 M 篇"）

## 注意事项

- **调用频率**：tweety-ns 保守使用，单次分析 < 5 个 API 调用
- **Cookie 过期**：如果登录失败（exit code 2），提示用户刷新 cookies
- **t.co 链接**：国内网络无法解析 t.co 短链接，推文全文已在数据中，不需要追踪外链
- **Python 版本**：系统 Python 3.14 可能有 SSL 兼容问题，确保 tweety-ns 对应的 httpx 版本兼容
- **followers API**：部分用户的 followers 数据会返回 "elevated authorization" 错误，这是非关键数据，跳过即可

---

## 下一步建议（条件触发）

画像完成后，根据结果判断是否推荐下一步。

| 触发条件 | 推荐 |
|---------|------|
| 博主有高质量内容值得长期追踪 | 「这个博主值得加入 X 信息源列表。要加到 x-info-sources 吗？」 |
| 博主的某些推文/文章值得收藏 | 「有几条内容值得单独收藏，用 content-collector 存一下？」 |
| 画像发现博主的方法论可用于公众号选题 | 「这个博主的观点可以做一期公众号文章，用 wemp-ops 写？」 |
