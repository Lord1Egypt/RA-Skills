# 🌐 TechRecruiter Pro 9 大平台总览

**全方位、多维度寻找技术人才！**

---

## 📊 平台总览

| # | 平台 | 类型 | 核心数据 | 优先级 |
|---|------|------|---------|-------|
| 1 | **AMiner** | 学术 | 论文、引用、H-index | ⭐⭐⭐⭐⭐ |
| 2 | **Google Scholar** | 学术 | 论文、引用、研究方向 | ⭐⭐⭐⭐⭐ |
| 3 | **GitHub** | 工程 | 代码、项目、Stars | ⭐⭐⭐⭐⭐ |
| 4 | **arXiv** | 学术 | 最新论文、预印本 | ⭐⭐⭐⭐ |
| 5 | **LinkedIn** | 职业 | 经历、技能、教育 | ⭐⭐⭐⭐⭐ |
| 6 | **Reddit** | 社区 | 讨论、Karma、专业度 | ⭐⭐⭐ |
| 7 | **Discord** | 社区 | 实时交流、协作 | ⭐⭐⭐ |
| 8 | **Hugging Face** | 工程 | 模型、数据集、Spaces | ⭐⭐⭐⭐⭐ |
| 9 | **X (Twitter)** | 社交 | 影响力、动态、网络 | ⭐⭐⭐⭐ |

---

## 🎯 平台分类

### 学术平台 (3 个)

| 平台 | 特点 | 适用人群 |
|-----|------|---------|
| **AMiner** | 中文友好、学者全 | 学术界研究员 |
| **Google Scholar** | 权威、引用准 | 所有研究人员 |
| **arXiv** | 最新、前沿 | 前沿研究者 |

**组合使用**: 验证学术背景 + 追踪最新研究

---

### 工程平台 (2 个)

| 平台 | 特点 | 适用人群 |
|-----|------|---------|
| **GitHub** | 代码可见、项目全 | 工程师/开发者 |
| **Hugging Face** | AI 模型集中 | AI/ML 工程师 |

**组合使用**: 评估工程能力 + AI 专业度

---

### 职业平台 (1 个)

| 平台 | 特点 | 适用人群 |
|-----|------|---------|
| **LinkedIn** | 职业经历、技能标签 | 工业界人才 |

**单独使用**: 了解职业轨迹

---

### 社区平台 (2 个)

| 平台 | 特点 | 适用人群 |
|-----|------|---------|
| **Reddit** | 深度讨论、Karma | 社区活跃者 |
| **Discord** | 实时交流、协作 | 社区参与者 |

**组合使用**: 评估社区影响力

---

### 社交平台 (1 个)

| 平台 | 特点 | 适用人群 |
|-----|------|---------|
| **X (Twitter)** | 实时动态、影响力 | 意见领袖 |

**单独使用**: 发现技术大 V

---

## 🔍 搜索策略

### 学术型人才

```
AMiner + Google Scholar + arXiv + GitHub
```

**适用**: 研究员、科学家、博士后

**评估维度**:
- 论文数量/质量
- 引用数/H-index
- 最新研究方向
- 代码开源能力

---

### 工程型人才

```
GitHub + Hugging Face + LinkedIn + Reddit
```

**适用**: 工程师、开发者、技术专家

**评估维度**:
- 代码质量/项目
- 模型/数据集
- 职业经历
- 社区贡献

---

### 综合型人才

```
全部 9 个平台
```

**适用**: 技术负责人、首席科学家、CTO

**评估维度**:
- 学术影响力
- 工程能力
- 职业背景
- 社区影响
- 社交媒体

---

## 📊 数据整合

### 候选人画像

```python
candidate_profile = {
    # 学术指标 (30%)
    "papers": scholar_data["paper_count"],
    "citations": scholar_data["total_citations"],
    "h_index": aminer_data["h_index"],
    
    # 工程能力 (25%)
    "github_repos": github_data["public_repos"],
    "github_stars": github_data["total_stars"],
    "hf_models": hf_data["models_count"],
    
    # 职业背景 (20%)
    "current_company": linkedin_data["current_company"],
    "experience_years": linkedin_data["experience_years"],
    "education": linkedin_data["education"],
    
    # 社区影响 (15%)
    "reddit_karma": reddit_data["karma"],
    "discord_activity": discord_data["activity"],
    
    # 社交媒体 (10%)
    "twitter_followers": twitter_data["followers"],
    "twitter_verified": twitter_data["verified"]
}

# 综合评分
overall_score = (
    academic_score * 0.30 +
    engineering_score * 0.25 +
    professional_score * 0.20 +
    community_score * 0.15 +
    social_score * 0.10
)
```

---

## 🎯 使用场景

### 场景 1: 寻找 RLHF 专家

```python
# 1. 学术搜索
scholar_results = searcher.search_google_scholar(
    keywords=["RLHF", "PPO", "LLM Alignment"]
)

# 2. 工程能力
github_results = searcher.search_github(
    keywords=["RLHF", "PPO"],
    min_stars=100
)

# 3. 职业背景
linkedin_results = searcher.search_linkedin(
    keywords=["RLHF"],
    current_company="DeepMind"
)

# 4. 社区影响
reddit_results = searcher.search_reddit(
    keywords=["RLHF"],
    subreddits=["MachineLearning"]
)

# 5. 社交媒体
twitter_results = searcher.search_twitter(
    keywords=["RLHF", "LLM"],
    min_followers=10000
)
```

---

### 场景 2: 评估候选人

```python
# 1. 验证学术背景
scholar_profile = searcher.search_google_scholar(
    author_name="Yifan Bai"
)

# 2. 检查代码能力
github_profile = searcher.search_github(
    keywords=[],  # 直接搜索用户
    username="yifanbai"
)

# 3. 查看职业经历
linkedin_profile = searcher.search_linkedin(
    keywords=[],
    name="Yifan Bai"
)

# 4. 评估社区影响
twitter_profile = searcher.search_twitter(
    keywords=[],
    username="@yifanbai"
)
```

---

### 场景 3: 发现新兴人才

```python
# 1. 最新论文作者
arxiv_results = searcher.search_arxiv(
    keywords=["LLM", "RLHF"],
    date_range="20260101-20260303"
)

# 2. Hugging Face 新星
hf_results = searcher.search_huggingface(
    keywords=["RLHF"],
    min_likes=50  # 低门槛
)

# 3. Twitter 新兴声音
twitter_results = searcher.search_twitter(
    keywords=["RLHF", "LLM"],
    min_followers=1000,  # 低门槛
    verified=False
)
```

---

## 📈 最佳实践

### 1. 多平台交叉验证

```
LinkedIn 经历 + GitHub 代码 + Google Scholar 论文
= 可信的候选人画像
```

### 2. 权重分配

| 平台类型 | 权重 | 说明 |
|---------|------|------|
| 学术 | 30% | 论文/引用 |
| 工程 | 25% | 代码/模型 |
| 职业 | 20% | 经历/技能 |
| 社区 | 15% | 讨论/贡献 |
| 社交 | 10% | 影响力 |

### 3. 搜索顺序

```
1. Google Scholar (验证学术)
2. GitHub (评估工程)
3. LinkedIn (了解职业)
4. Hugging Face (AI 专业度)
5. Reddit/Discord (社区)
6. Twitter (影响力)
```

---

## 🔧 API 配置总览

| 平台 | API | 必需 | 申请地址 |
|-----|-----|------|---------|
| AMiner | 无 | ❌ | 直接使用 |
| Google Scholar | 无 | ❌ | 直接使用 |
| GitHub | OAuth | ⚠️ 可选 | GitHub Settings |
| arXiv | 无 | ❌ | 直接使用 |
| LinkedIn | OAuth | ⚠️ 推荐 | LinkedIn Developers |
| Reddit | OAuth | ⚠️ 推荐 | Reddit Apps |
| Discord | Bot Token | ⚠️ 推荐 | Discord Developers |
| Hugging Face | Token | ⚠️ 推荐 | HF Settings |
| X (Twitter) | Bearer Token | ⚠️ 推荐 | Twitter Developers |

---

## 📊 平台对比

| 维度 | 覆盖度 | 准确性 | 实时性 | 难度 |
|-----|-------|-------|-------|------|
| AMiner | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 简单 |
| Google Scholar | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 简单 |
| GitHub | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 简单 |
| arXiv | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 简单 |
| LinkedIn | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中等 |
| Reddit | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 中等 |
| Discord | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 困难 |
| Hugging Face | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 简单 |
| X (Twitter) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 中等 |

---

## 🎊 总结

**9 大平台，全方位覆盖技术人才！**

| 类别 | 平台数 | 平台 |
|-----|-------|------|
| 学术 | 3 | AMiner, Google Scholar, arXiv |
| 工程 | 2 | GitHub, Hugging Face |
| 职业 | 1 | LinkedIn |
| 社区 | 2 | Reddit, Discord |
| 社交 | 1 | X (Twitter) |

**一站式解决技术人才招聘！** 🎯

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**作者**: 虾哥 AI Assistant
