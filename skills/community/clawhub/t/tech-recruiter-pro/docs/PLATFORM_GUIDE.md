# 🌐 TechRecruiter Pro 全平台搜索指南

**支持 8 大平台，全方位寻找技术人才！**

---

## 📊 平台总览

| # | 平台 | 数据类型 | 适用场景 | 优先级 |
|---|------|---------|---------|-------|
| 1 | **AMiner** | 学者档案、论文、引用 | 学术型人才 | ⭐⭐⭐⭐⭐ |
| 2 | **Google Scholar** | 论文、引用、H-index | 研究型候选人 | ⭐⭐⭐⭐⭐ |
| 3 | **GitHub** | 代码仓库、项目 | 工程师/开发者 | ⭐⭐⭐⭐⭐ |
| 4 | **arXiv** | 最新论文 | 前沿研究者 | ⭐⭐⭐⭐ |
| 5 | **LinkedIn** | 职业经历、技能 | 工业界人才 | ⭐⭐⭐⭐⭐ |
| 6 | **Reddit** | 技术讨论、影响力 | 社区活跃者 | ⭐⭐⭐ |
| 7 | **Discord** | 技术社区、实时交流 | 社区参与者 | ⭐⭐⭐ |
| 8 | **Hugging Face** | 模型、数据集 | AI/ML 工程师 | ⭐⭐⭐⭐⭐ |

---

## 🔍 各平台详解

### 1. AMiner (清华大学)

**网址**: https://www.aminer.cn/

**数据类型**:
- 学者基本信息
- 论文列表
- 引用统计
- H-index/G-index
- 合作网络
- 研究兴趣

**适用场景**:
- 寻找学术界研究员
- 验证学术背景
- 查找高引用学者

**搜索示例**:
```python
searcher.search_aminer(
    keywords=["RLHF", "LLM"],
    affiliation="Moonshot"
)
```

**优势**:
- ✅ 中文支持好
- ✅ 学者数据全
- ✅ 免费使用

**局限**:
- ⚠️ 工业界人士覆盖少

---

### 2. Google Scholar

**网址**: https://scholar.google.com/

**数据类型**:
- 论文列表
- 引用数
- H-index
- I10-index
- 研究方向

**适用场景**:
- 学术影响力评估
- 论文质量分析
- 研究轨迹追踪

**搜索示例**:
```python
searcher.search_google_scholar(
    author_name="Yifan Bai",
    keywords=["LLM"]
)
```

**优势**:
- ✅ 数据最权威
- ✅ 覆盖全面
- ✅ 引用追踪准确

**局限**:
- ⚠️ 需要手动验证作者
- ⚠️ 有反爬机制

---

### 3. GitHub

**网址**: https://github.com/

**数据类型**:
- 代码仓库
- 贡献记录
- Stars/Forks
- 技术栈
- 项目影响力

**适用场景**:
- 工程师技能评估
- 代码质量审查
- 开源贡献度分析

**搜索示例**:
```python
searcher.search_github(
    keywords=["RLHF", "PPO"],
    language="Python",
    min_stars=100
)
```

**优势**:
- ✅ 代码可见
- ✅ 技能直观
- ✅ 项目质量可评估

**局限**:
- ⚠️ 需要 API token 提高限制

---

### 4. arXiv

**网址**: https://arxiv.org/

**数据类型**:
- 最新论文
- 研究领域
- 合作者
- 提交时间

**适用场景**:
- 追踪最新研究
- 发现新兴研究者
- 前沿技术调研

**搜索示例**:
```python
searcher.search_arxiv(
    keywords=["Kimi", "K2"],
    date_range="20250101-20251231"
)
```

**优势**:
- ✅ 最新研究
- ✅ 免费访问
- ✅ 覆盖广

**局限**:
- ⚠️ 预印本未同行评审

---

### 5. LinkedIn (新增 ⭐)

**网址**: https://www.linkedin.com/

**数据类型**:
- 职业经历
- 教育背景
- 技能标签
- 人脉网络
- 推荐信

**适用场景**:
- 工业界人才搜索
- 职业轨迹分析
- 技能匹配度评估

**搜索示例**:
```python
searcher.search_linkedin(
    keywords=["RLHF", "LLM"],
    current_company="Moonshot AI",
    title="Research Scientist"
)
```

**优势**:
- ✅ 职业信息全
- ✅ 技能标签化
- ✅ 人脉可见

**局限**:
- ⚠️ 需要 API 或手动搜索
- ⚠️ 部分信息需连接可见

---

### 6. Reddit (新增 ⭐)

**网址**: https://www.reddit.com/

**数据类型**:
- 技术讨论
- 帖子/评论
- Karma 分数
- 专业领域

**适用场景**:
- 社区影响力评估
- 技术热情判断
- 软技能观察

**搜索示例**:
```python
searcher.search_reddit(
    keywords=["RLHF", "LLM"],
    subreddits=["MachineLearning", "reinforcementlearning"],
    min_karma=1000
)
```

**相关 Subreddit**:
- r/MachineLearning
- r/reinforcementlearning
- r/LocalLLaMA
- r/artificial
- r/deeplearning

**优势**:
- ✅ 真实兴趣展现
- ✅ 社区参与度
- ✅ 沟通能力观察

**局限**:
- ⚠️ 匿名用户多
- ⚠️ 需要 PRAW API

---

### 7. Discord (新增 ⭐)

**网址**: https://discord.com/

**数据类型**:
- 服务器成员
- 活跃度
- 技术讨论
- 项目协作

**适用场景**:
- 社区参与度
- 实时交流能力
- 团队协作观察

**搜索示例**:
```python
searcher.search_discord(
    keywords=["AI", "ML"],
    servers=["AI Research Hub", "Machine Learning"]
)
```

**相关服务器**:
- AI Research Hub
- Machine Learning
- Hugging Face
- LLM Research

**优势**:
- ✅ 实时互动
- ✅ 项目协作可见
- ✅ 社区活跃度高

**局限**:
- ⚠️ 需要加入服务器
- ⚠️ 隐私设置限制

---

### 8. Hugging Face (新增 ⭐)

**网址**: https://huggingface.co/

**数据类型**:
- 模型仓库
- 数据集
- Spaces 项目
- 点赞数
- 下载量

**适用场景**:
- AI/ML 工程师评估
- 模型质量分析
- 开源贡献度

**搜索示例**:
```python
searcher.search_huggingface(
    keywords=["RLHF", "LLM"],
    model_type="transformer",
    min_likes=100
)
```

**优势**:
- ✅ AI 模型集中
- ✅ 代码+模型可见
- ✅ 社区认可度

**局限**:
- ⚠️ 主要 AI 领域

---

## 🎯 平台组合策略

### 学术型人才

```
AMiner + Google Scholar + arXiv + GitHub
```

**适用**: 研究员、科学家、博士后

---

### 工程型人才

```
GitHub + Hugging Face + LinkedIn + Reddit
```

**适用**: 工程师、开发者、技术专家

---

### 综合型人才

```
全部 8 个平台
```

**适用**: 技术负责人、首席科学家、CTO

---

## 📊 数据整合

### 候选人画像整合

```python
profile = {
    # 学术指标
    "papers": scholar_data["paper_count"],
    "citations": scholar_data["total_citations"],
    "h_index": aminer_data["h_index"],
    
    # 工程能力
    "github_repos": github_data["public_repos"],
    "hf_models": hf_data["models_count"],
    
    # 职业信息
    "current_company": linkedin_data["current_company"],
    "experience": linkedin_data["experience"],
    
    # 社区影响
    "reddit_karma": reddit_data["karma"],
    "discord_activity": discord_data["activity"]
}
```

---

## 🔧 API 配置

### LinkedIn

```bash
export LINKEDIN_API_KEY=your_key
export LINKEDIN_API_SECRET=your_secret
```

申请：https://www.linkedin.com/developers/

### Reddit (PRAW)

```bash
export REDDIT_CLIENT_ID=your_id
export REDDIT_CLIENT_SECRET=your_secret
```

申请：https://www.reddit.com/prefs/apps

### Discord

```bash
export DISCORD_BOT_TOKEN=your_token
```

申请：https://discord.com/developers/applications

### Hugging Face

```bash
export HUGGINGFACE_TOKEN=your_token
```

申请：https://huggingface.co/settings/tokens

---

## 📈 最佳实践

### 1. 多平台交叉验证

```
LinkedIn 职业经历 + GitHub 代码 + Google Scholar 论文
= 完整候选人画像
```

### 2. 权重分配

| 平台 | 权重 | 说明 |
|-----|------|------|
| Google Scholar | 30% | 学术影响力 |
| GitHub | 25% | 工程能力 |
| LinkedIn | 20% | 职业背景 |
| Hugging Face | 15% | AI 专业度 |
| 其他 | 10% | 社区影响 |

### 3. 搜索顺序

```
1. Google Scholar (验证学术背景)
2. GitHub (评估代码能力)
3. LinkedIn (了解职业轨迹)
4. Hugging Face (AI 专业度)
5. Reddit/Discord (社区参与)
```

---

## 🎊 总结

**8 大平台，全方位覆盖！**

| 维度 | 平台 |
|-----|------|
| **学术** | AMiner, Google Scholar, arXiv |
| **工程** | GitHub, Hugging Face |
| **职业** | LinkedIn |
| **社区** | Reddit, Discord |

**一站式解决技术人才招聘！** 🎯

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**作者**: 虾哥 AI Assistant
