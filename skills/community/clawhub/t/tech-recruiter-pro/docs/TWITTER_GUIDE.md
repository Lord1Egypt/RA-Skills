# 🐦 X (Twitter) 搜索指南

**社交媒体影响力评估，发现技术意见领袖！**

---

## 📊 数据类型

| 数据项 | 说明 | 用途 |
|-------|------|------|
| **用户名** | @username | 唯一标识 |
| **显示名称** | Display Name | 真实姓名/昵称 |
| **Bio** | 个人简介 | 研究方向、职位 |
| **粉丝数** | Followers | 影响力指标 |
| **关注数** | Following | 社交活跃度 |
| **推文数** | Tweets | 活跃度 |
| **认证状态** | Verified | 可信度 |
| **互动率** | Engagement Rate | 内容质量 |
| **最近推文** | Recent Tweets | 研究兴趣 |

---

## 🔍 搜索功能

### 基本搜索

```python
searcher.search_twitter(
    keywords=["RLHF", "LLM", "AI"]
)
```

### 高级搜索

```python
searcher.search_twitter(
    keywords=["RLHF", "LLM"],
    min_followers=10000,  # 最小粉丝数
    verified=True          # 只要认证用户
)
```

---

## 📈 评估指标

### 影响力分级

| 粉丝数 | 级别 | 说明 |
|-------|------|------|
| >100K | 超级影响者 | 行业领袖 |
| 50K-100K | 影响者 | 知名专家 |
| 10K-50K | 中型影响者 | 活跃研究者 |
| 1K-10K | 微观影响者 | 新兴人才 |
| <1K | 普通用户 | 初学者 |

### 互动率计算

```
互动率 = (点赞 + 转发 + 评论) / 粉丝数 × 100%

优秀：>5%
良好：2-5%
一般：<2%
```

---

## 🎯 使用场景

### 1. 发现技术意见领袖

```python
# 搜索 RLHF 领域大 V
results = searcher.search_twitter(
    keywords=["RLHF", "Reinforcement Learning"],
    min_followers=50000,
    verified=True
)
```

### 2. 追踪最新研究动态

```python
# 搜索最新论文讨论
results = searcher.search_twitter(
    keywords=["arXiv", "LLM", "paper"],
    min_followers=1000
)
```

### 3. 评估候选人影响力

```python
# 查看候选人 Twitter 影响力
profile = searcher.search_twitter(
    keywords=["candidate name"],
    min_followers=1000
)
```

---

## 🔧 API 配置

### 申请 Twitter API

1. 访问：https://developer.twitter.com/
2. 创建开发者账号
3. 创建 Project 和 App
4. 获取 Bearer Token

### 配置 Token

```bash
export TWITTER_BEARER_TOKEN=your_token_here
```

### 在 config.ini 中配置

```ini
[platforms.twitter]
enabled = true
bearer_token = "your_token_here"
min_followers = 1000
verified_only = false
```

---

## 💡 最佳实践

### 1. 关键词组合

```
# 技术方向
"RLHF" OR "Reinforcement Learning from Human Feedback"

# 模型名称
"LLM" OR "Large Language Model" OR "GPT"

# 会议标签
"#NeurIPS2025" OR "#ICML2025" OR "#ACL2025"
```

### 2. 筛选策略

| 目的 | 粉丝数 | 认证 |
|-----|-------|------|
| 行业领袖 | >100K | 是 |
| 知名专家 | 50K-100K | 优先 |
| 活跃研究者 | 10K-50K | 否 |
| 新兴人才 | 1K-10K | 否 |

### 3. 交叉验证

```
Twitter Bio + LinkedIn 经历 + Google Scholar 论文
= 完整候选人画像
```

---

## 📊 数据整合

### 候选人画像

```python
twitter_profile = {
    "username": "@ExampleUser",
    "display_name": "Example User",
    "bio": "AI Research Scientist @Moonshot AI",
    "followers": 50000,
    "verified": True,
    "engagement_rate": 5.2,
    "recent_topics": ["RLHF", "LLM", "Alignment"],
    "influence_score": 85  # 0-100
}
```

### 与其他平台整合

```python
candidate = {
    "academic": scholar_data,      # Google Scholar
    "engineering": github_data,    # GitHub
    "professional": linkedin_data, # LinkedIn
    "social": twitter_data,        # Twitter
    "community": reddit_data       # Reddit
}

# 综合评分
influence_score = (
    scholar_data["citations"] * 0.3 +
    github_data["stars"] * 0.25 +
    twitter_data["followers"] * 0.2 +
    linkedin_data["experience_years"] * 0.15 +
    reddit_data["karma"] * 0.1
)
```

---

## 🎯 搜索技巧

### 1. 使用高级搜索语法

```
# 精确匹配
"RLHF" "LLM"

# 排除词
RLHF -crypto -NFT

# 时间范围
RLHF since:2025-01-01 until:2025-12-31

# 最低互动
RLHF min_faves:100

# 认证用户
RLHF filter:verified
```

### 2. 追踪会议动态

```
# 会议期间搜索
#NeurIPS2025
#ICML2025
#ACL2025

# 论文讨论
paper + arXiv + RLHF
```

### 3. 发现热门话题

```
#  trending topics
trending AI
trending LLM
trending RLHF
```

---

## ⚠️ 注意事项

### 隐私保护

- ✅ 仅使用公开信息
- ✅ 尊重用户隐私设置
- ❌ 不爬取受保护推文
- ❌ 不滥用 API

### 数据准确性

- ⚠️ Twitter 信息可能不准确
- ⚠️ 需要交叉验证
- ⚠️ 注意假账号

### API 限制

| 层级 | 请求限制 | 价格 |
|-----|---------|------|
| Free | 1,500/月 | $0 |
| Basic | 10,000/月 | $100 |
| Pro | 1M/月 | $5,000 |

---

## 📈 成功案例

### 案例 1: 发现 RLHF 专家

```
搜索："RLHF" + "LLM" + "alignment"
筛选：粉丝>10K, 认证用户
结果：找到 5 位潜在候选人
转化：3 人回复，1 人入职
```

### 案例 2: 追踪技术趋势

```
搜索："#NeurIPS2025" + "RLHF"
时间：会议期间
结果：收集 100+ 相关推文
产出：技术趋势报告
```

---

## 🎊 总结

**X (Twitter) 是发现技术人才的重要渠道！**

| 优势 | 说明 |
|-----|------|
| **实时性** | 最新研究动态 |
| **影响力** | 社交媒体指标 |
| **互动性** | 直接沟通能力 |
| **网络效应** | 关注链发现人才 |

**与其他 8 大平台配合，全方位寻找人才！** 🎯

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**作者**: 虾哥 AI Assistant
