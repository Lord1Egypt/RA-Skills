# TechRecruiter Pro - 智能技术招聘助手 🎯

**Intelligent Technical Recruiting Assistant**

专门针对**算法工程师**和**研发工程师**的智能化招聘助手。

An intelligent recruiting assistant specialized for **algorithm engineers** and **R&D engineers**.

---

## 🚀 核心功能 / Core Features

| 功能 / Feature | 说明 / Description | 状态 / Status |
|---------------|-------------------|---------------|
| **多平台搜索** / Multi-Platform Search | GitHub/Google Scholar/AMiner/arXiv 候选人搜索 | ✅ 支持 / Supported |
| **画像分析** / Profile Analysis | 整合多平台信息生成完整候选人画像 | ✅ 支持 / Supported |
| **邮件生成** / Email Generation | 基于候选人背景生成个性化招呼邮件 | ✅ 支持 / Supported |
| **Pipeline 管理** / Pipeline Management | 候选人流程管理（需 Feishu Bitable） | ⚠️ 需配置 / Requires Config |

---

## 📦 依赖技能 / Required Skills

**必须配置 / Required**:
- `feishu_bitable` - 候选人数据库 / Candidate database
- `feishu_doc` - JD 和邮件模板管理 / JD and email template management
- `browser` - 网页搜索和数据抓取 / Web search and scraping
- `web_fetch` - 快速获取网页内容 / Fast web content fetching
- `web_search` - 搜索引擎查询 / Search engine queries

**可选 / Optional**:
- `tts` - 语音播报招聘报告 / Voice report (optional)

---

## 🔧 使用方法 / Usage

### 基础搜索 / Basic Search

```
搜索算法工程师候选人，要求：
Search for algorithm engineer candidates, requirements:
- 研究方向：RLHF/PPO/LLM / Research: RLHF/PPO/LLM
- 公司：DeepMind/OpenAI/Meta / Companies: DeepMind/OpenAI/Meta
- 学历：博士 / Education: PhD
- 年龄：95 后 / Age: Born after 1995
```

### 深度分析 / Deep Analysis

```
分析这个候选人的匹配度：
Analyze this candidate's matching score:
- GitHub: github.com/username
- Google Scholar: scholar.google.com/citations?user=xxx
- 目标职位：高级算法工程师 / Target position: Senior Algorithm Engineer
```

### 生成邮件 / Generate Email

```
为候选人生成个性化邮件：
Generate personalized email for candidate:
- 突出他的 RLHF 研究 / Highlight his RLHF research
- 提及他的开源项目 / Mention his open source projects
- 强调我们团队的技术优势 / Emphasize our team's technical strengths
```

---

## 📖 执行逻辑 / Execution Logic

### 任务 1: 多平台候选人搜索

**输入 / Input**:
- 研究方向 / Research area (e.g., RLHF, LLM, Agent)
- 目标公司 / Target companies (e.g., DeepMind, OpenAI)
- 学历要求 / Education requirements (e.g., PhD)
- 其他筛选条件 / Other filters

**执行步骤 / Execution Steps**:

#### Step 1: Google Scholar 搜索

```python
# 搜索 URL 模板 / Search URL Template
url = f"https://scholar.google.com/scholar?q={research_area}+{target_company}"

# 解析逻辑 / Parse Logic
# 1. 提取论文标题、作者、引用数
# 2. 点击作者链接进入个人主页
# 3. 提取 H-index、总引用数、论文列表
# 4. 查找作者主页链接（通常在右上角）

# 错误处理 / Error Handling
# - 遇到验证码：暂停 5 分钟，使用代理 IP
# - 无结果：尝试简化搜索词
# - 页面结构变化：检查 CSS 选择器是否匹配
```

**提取字段 / Extracted Fields**:
- 姓名 / Name
- 单位 / Affiliation
- 研究兴趣 / Research Interests
- 论文数 / Paper Count
- 总引用数 / Total Citations
- H-index
- 个人主页链接 / Homepage URL

#### Step 2: AMiner 搜索

```python
# 搜索 URL 模板 / Search URL Template
url = f"https://www.aminer.cn/search?q={research_area}+{target_company}"

# 解析逻辑 / Parse Logic
# 1. 提取学者卡片（姓名、单位、H-index）
# 2. 点击学者进入详情页
# 3. 提取完整论文列表、合作者网络
# 4. 查找联系方式（邮箱、主页）

# 注意 / Note
# AMiner 无需登录即可浏览，但部分功能需要登录
# AMiner does not require login for browsing, but some features need login
```

**提取字段 / Extracted Fields**:
- 姓名 / Name
- 当前单位 / Current Affiliation
- 历史单位 / Historical Affiliations
- H-index
- G-index
- 论文数 / Paper Count
- 被引数 / Citation Count
- 研究兴趣 / Research Interests
- 合作者网络 / Co-author Network

#### Step 3: GitHub 搜索

```python
# 搜索 URL 模板 / Search URL Template
url = f"https://github.com/search?q={research_area}&type=repositories&sort=stars"

# 解析逻辑 / Parse Logic
# 1. 提取高星项目（stars > 100）
# 2. 查看项目贡献者列表
# 3. 点击主要贡献者进入个人主页
# 4. 提取贡献记录、技术栈、Followers 数

# 高级搜索 / Advanced Search
# 按公司搜索：user:{company}+{research_area}
# 按技术栈搜索：language:python+topic:rlhf
```

**提取字段 / Extracted Fields**:
- 用户名 / Username
- 头像 / Avatar
- Followers 数
- 贡献图 / Contribution Graph
- 主要项目 / Top Projects
- 技术栈 / Tech Stack
- 个人简介 / Bio
- 邮箱（如有）/ Email (if available)

#### Step 4: arXiv 搜索

```python
# 搜索 URL 模板 / Search URL Template
url = f"https://arxiv.org/search/?query={research_area}+{author_name}&searchtype=author"

# 解析逻辑 / Parse Logic
# 1. 提取论文列表（标题、摘要、提交日期）
# 2. 识别第一作者/通讯作者论文
# 3. 提取合作者信息
# 4. 分析研究方向演变

# 高级用法 / Advanced Usage
# 结合多个关键词：query=RLHF+LLM+agent
# 按时间排序：sortorder=-submitted_date
```

**提取字段 / Extracted Fields**:
- 论文标题 / Paper Title
- 作者列表 / Author List
- 提交日期 / Submission Date
- 摘要 / Abstract
- 研究方向 / Research Areas
- 合作者 / Co-authors

---

### 任务 2: 候选人画像分析

**输入 / Input**:
- 候选人链接列表 / Candidate profile links
- 目标职位 JD / Target job description

**执行步骤 / Execution Steps**:

#### Step 1: 信息整合

```python
# 整合多平台信息 / Integrate multi-platform information
candidate_profile = {
    "name": "候选人姓名 / Candidate Name",
    "current_company": "当前公司 / Current Company",
    "current_position": "当前职位 / Current Position",
    "education": [
        {
            "school": "学校 / School",
            "degree": "学位 / Degree",
            "year": "毕业年份 / Graduation Year"
        }
    ],
    "research_areas": ["研究方向 1", "研究方向 2"],
    "papers": {
        "count": 15,
        "top_papers": [
            {
                "title": "论文标题",
                "venue": "会议/期刊名称",
                "year": 2025,
                "citations": 150,
                "role": "第一作者/通讯作者"
            }
        ]
    },
    "citations": {
        "total": 2500,
        "h_index": 18
    },
    "github": {
        "username": "GitHub 用户名",
        "followers": 500,
        "repos": [
            {
                "name": "项目名",
                "stars": 1200,
                "language": "Python",
                "role": "主要贡献者"
            }
        ]
    },
    "skills": ["PyTorch", "RLHF", "LLM", "Multi-agent"],
    "contact": {
        "email": "邮箱",
        "homepage": "个人主页",
        "linkedin": "LinkedIn",
        "twitter": "Twitter"
    }
}
```

#### Step 2: 匹配度评分

```python
# 匹配度评分逻辑 / Matching Score Logic
def calculate_match_score(candidate, jd):
    score = 0
    max_score = 100
    
    # 1. 研究方向匹配 (30 分)
    # Research area match (30 points)
    research_match = len(set(candidate.research_areas) & set(jd.required_areas))
    score += min(30, research_match * 10)
    
    # 2. 学术影响力 (25 分)
    # Academic impact (25 points)
    if candidate.h_index >= jd.min_h_index:
        score += 15
    if candidate.total_citations >= jd.min_citations:
        score += 10
    
    # 3. 工程能力 (20 分)
    # Engineering ability (20 points)
    if candidate.github_followers >= 100:
        score += 10
    if any(repo.stars >= 500 for repo in candidate.github_repos):
        score += 10
    
    # 4. 公司背景 (15 分)
    # Company background (15 points)
    if candidate.current_company in jd.target_companies:
        score += 15
    
    # 5. 学历背景 (10 分)
    # Education background (10 points)
    if candidate.degree in ["PhD", "Master"]:
        score += 10
    
    return min(score, max_score)
```

**评分标准 / Scoring Criteria**:

| 分数 / Score | 等级 / Level | 建议 / Recommendation |
|-------------|------------|---------------------|
| 90-100 | S 级 / S-Tier | 最优先触达 / Highest priority |
| 80-89 | A 级 / A-Tier | 优先触达 / High priority |
| 70-79 | B 级 / B-Tier | 正常跟进 / Normal follow-up |
| 60-69 | C 级 / C-Tier | 保持联系 / Keep in touch |
| <60 | 不匹配 / Not Match | 暂不触达 / Do not contact |

---

### 任务 3: 个性化邮件生成

**输入 / Input**:
- 候选人完整画像 / Complete candidate profile
- 公司信息 / Company information
- 职位信息 / Job information

**执行步骤 / Execution Steps**:

#### Step 1: 提取个性化元素

```python
# 提取个性化元素 / Extract personalization elements
personalization = {
    "paper": candidate.top_paper.title,  # 最相关的论文
    "project": candidate.top_github_repo.name,  # 最相关的项目
    "technique": candidate.skills[0],  # 最匹配的技术
    "company": candidate.current_company,  # 当前公司
    "research": candidate.research_areas[0],  # 主要研究方向
}
```

#### Step 2: 生成邮件模板

```markdown
主题 / Subject: [{公司名 / Company}] {职位 / Position} 机会 - 看到您的{研究方向 / Research}工作很感兴趣

正文 / Body:

{称呼 / Dear} {候选人姓名 / Name},

您好！/ Hello!

我是{公司名 / Company}的{招聘负责人 / Hiring Manager}。
I'm {Hiring Manager} from {Company}.

【个性化开场 / Personalized Opening】

我最近拜读了您的论文《{论文标题 / Paper Title}》({年份 / Year})，
I recently read your paper "{Paper Title}" ({Year}),

特别是您提出的{方法/技术 / Method/Technique}让我印象深刻。
I was particularly impressed by your {Method/Technique}.

您在{GitHub 项目 / GitHub Project}中的实现也非常精彩，
Your implementation in {GitHub Project} is also impressive,

特别是{具体功能 / Specific Feature}的设计。
especially the design of {Specific Feature}.

【职位介绍 / Position Introduction】

我们正在招募{职位 / Position}，主要负责{工作内容 / Responsibilities}。
We are hiring a {Position} to work on {Responsibilities}.

这个岗位需要{技能要求 / Skills Required}，与您的背景非常匹配。
This role requires {Skills Required}, which matches your background very well.

【团队亮点 / Team Highlights】

- 技术团队：{团队介绍 / Team Description}
- 研究方向：{研究方向 / Research Direction}
- 资源支持：{资源介绍 / Resources}

【下一步 / Next Steps】

如果您对这个机会感兴趣，我们可以安排一个 30 分钟的电话沟通。
If you're interested, we can schedule a 30-minute call.

您看{时间选项 / Time Options}哪个时间方便？
Would {Time Options} work for you?

期待您的回复！/ Looking forward to your reply!

{签名 / Signature}
{联系方式 / Contact Info}
```

#### Step 3: 邮件优化建议

**最佳实践 / Best Practices**:

1. **个性化程度 > 80%** / Personalization > 80%
   - 至少提及 1 篇论文 / Mention at least 1 paper
   - 至少提及 1 个项目 / Mention at least 1 project
   - 展示你懂他的技术 / Show you understand their work

2. **长度控制 / Length Control**
   - 中文：200-400 字 / Chinese: 200-400 characters
   - 英文：100-200 词 / English: 100-200 words

3. **语气 / Tone**
   - 专业但友好 / Professional but friendly
   - 避免过度吹捧 / Avoid excessive flattery
   - 强调双向选择 / Emphasize mutual fit

4. **跟进策略 / Follow-up Strategy**
   - 第 1 封：初次联系 / Initial contact
   - 第 2 封（3-5 天后）：温和提醒 / Gentle reminder
   - 第 3 封（再 5 天后）：最后确认 / Final check
   - 最多 3 次 / Maximum 3 attempts

---

### 任务 4: Pipeline 管理（需 Feishu Bitable）

**注意 / Note**: 此功能需要配置 Feishu Bitable

**Bitable 表结构 / Bitable Table Structure**:

| 字段 / Field | 类型 / Type | 说明 / Description |
|-------------|------------|-------------------|
| 姓名 / Name | 文本 / Text | 候选人姓名 / Candidate name |
| 当前公司 / Current Company | 文本 / Text | 当前工作单位 / Current employer |
| 职位 / Position | 文本 / Text | 当前职位 / Current position |
| 研究方向 / Research Areas | 多行文本 / Long Text | 研究领域列表 / Research areas |
| 邮箱 / Email | 文本 / Text | 联系邮箱 / Contact email |
| GitHub | URL | GitHub 主页 / GitHub profile |
| Google Scholar | URL | Scholar 主页 / Scholar profile |
| 论文数 / Paper Count | 数字 / Number | 发表论文数量 / Number of papers |
| 总引用 / Total Citations | 数字 / Number | 总引用次数 / Total citations |
| H-index | 数字 / Number | H 指数 / H-index |
| 匹配度 / Match Score | 数字 / Number | 0-100 分 / 0-100 score |
| 状态 / Status | 单选 / Single Select | 发现/初筛/联系/面试/Offer/入职 |
| 优先级 / Priority | 单选 / Single Select | 高/中/低 / High/Medium/Low |
| 最后联系 / Last Contact | 日期 / Date | 最后联系日期 / Last contact date |
| 下次跟进 / Next Follow-up | 日期 / Date | 下次跟进日期 / Next follow-up date |
| 备注 / Notes | 多行文本 / Long Text | 补充信息 / Additional notes |

**状态流转 / Status Flow**:

```
发现 / Discover
  ↓
初筛 / Screening (匹配度 >= 70)
  ↓
联系 / Contacted (已发送邮件)
  ↓
面试 / Interview (候选人同意面试)
  ↓
Offer / Offer (通过面试)
  ↓
入职 / Hired (接受 Offer)
```

**使用示例 / Usage Examples**:

```
# 查看候选人 Pipeline
查看候选人 Pipeline 状态 / View candidate pipeline status

# 更新状态
更新候选人 [姓名] 状态为"已联系" / Update candidate [name] status to "Contacted"

# 安排面试
安排面试：候选人 [姓名]，[日期] [时间] / Schedule interview: [name], [date] [time]

# 导出报告
导出本周招聘报告 / Export weekly recruiting report
```

---

## ⚠️ 注意事项 / Important Notes

### 合规性 / Compliance

- ✅ **遵守 GDPR/隐私法规** / Comply with GDPR/privacy regulations
- ✅ **仅收集公开信息** / Only collect publicly available information
- ✅ **尊重候选人隐私** / Respect candidate privacy
- ✅ **提供 opt-out 选项** / Provide opt-out option

### 数据存储 / Data Storage

**存储内容 / Stored Data**:
- 候选人姓名、公司、职位 / Candidate name, company, position
- 联系方式（邮箱、GitHub、LinkedIn 等）/ Contact info (email, GitHub, LinkedIn, etc.)
- 学术指标（论文数、引用数、H-index）/ Academic metrics (paper count, citations, H-index)

**不存储 / Not Stored**:
- ❌ 身份证号、银行卡号等敏感信息 / ID numbers, bank card numbers, etc.
- ❌ 私人聊天记录 / Private chat records
- ❌ 未公开的个人信息 / Non-public personal information

**数据删除 / Data Deletion**:
- 可随时删除候选人记录 / Candidate records can be deleted anytime
- 删除命令：`删除候选人 [姓名]` / Delete command: `Delete candidate [name]`

### API 使用 / API Usage

| 平台 / Platform | 推荐方式 / Recommended | 限制 / Limits |
|----------------|----------------------|--------------|
| **GitHub** | 官方 API (带 Token) / Official API (with Token) | 未认证：60 次/小时 / Unauthenticated: 60/hr |
| **Google Scholar** | 手动搜索 + 缓存 / Manual search + cache | 频繁访问可能触发验证码 / May trigger captcha |
| **AMiner** | 网页搜索 / Web search | 无官方 API / No official API |
| **LinkedIn** | 官方 API (需审核) / Official API (requires approval) | 禁止 scraping / Scraping prohibited |
| **Twitter/X** | 官方 API v2 / Official API v2 | 免费层：1500 次/月 / Free tier: 1500/mo |

**速率限制建议 / Rate Limit Recommendations**:
- 同一平台请求间隔 >= 2 秒 / Interval >= 2 seconds between requests
- 遇到验证码立即暂停 / Pause immediately on captcha
- 使用缓存减少重复请求 / Use cache to reduce duplicate requests

---

## 📊 效果追踪 / Metrics

| 指标 / Metric | 计算方式 / Calculation | 目标 / Target |
|--------------|----------------------|--------------|
| 回复率 / Reply Rate | 回复数/发送数 / Replies sent | >30% |
| 面试率 / Interview Rate | 面试数/回复数 / Interviews replies | >50% |
| Offer 率 / Offer Rate | Offer 数/面试数 / Offers interviews | >30% |
| 接受率 / Acceptance Rate | 接受数/Offer 数 / Accepts offers | >70% |
| 平均招聘周期 / Avg Hiring Cycle | 发现→入职天数 / Days discover to hire | <45 天 / days |

---

## 🔒 安全声明 / Security Declaration

**本 Skill 不会 / This Skill Will NOT**:
- ❌ 将数据发送到未经授权的第三方 / Send data to unauthorized third parties
- ❌ 存储候选人敏感信息（身份证号、银行卡等）/ Store sensitive info (ID, bank cards, etc.)
- ❌ 绕过平台认证机制 / Bypass platform authentication
- ❌ 违反网站 robots.txt 协议 / Violate website robots.txt

**使用前请确认 / Before Using, Confirm**:
- ✅ 你有权收集和使用这些候选人数据 / You have the right to collect and use this data
- ✅ 你的使用场景符合当地法律法规 / Your use case complies with local laws
- ✅ 你已告知候选人数据使用目的（如需要）/ You've informed candidates about data usage (if required)

---

## 📚 示例 / Examples

### 示例 1: 搜索 RLHF 方向候选人

```
输入 / Input:
搜索 RLHF 方向的算法工程师，目标公司：Moonshot/DeepSeek/DeepMind
Search for RLHF algorithm engineers, target companies: Moonshot/DeepSeek/DeepMind

执行 / Execution:
1. Google Scholar 搜索 "RLHF + Moonshot/DeepSeek/DeepMind"
2. AMiner 搜索 "RLHF + 强化学习"
3. GitHub 搜索 "RLHF + PPO + language:python"
4. arXiv 搜索 "RLHF + LLM"

输出 / Output:
找到 15 位候选人，S 级 3 人，A 级 5 人，B 级 7 人
Found 15 candidates: 3 S-tier, 5 A-tier, 7 B-tier
```

### 示例 2: 分析候选人匹配度

```
输入 / Input:
分析这个候选人：
- GitHub: github.com/yifan-bai
- Google Scholar: scholar.google.com/citations?user=xxx
目标职位：高级算法工程师（RLHF 方向）

执行 / Execution:
1. 抓取 GitHub 项目、贡献记录
2. 抓取 Scholar 论文、引用数
3. 计算匹配度评分
4. 生成完整画像

输出 / Output:
候选人：Yifan Bai
当前公司：Moonshot AI
匹配度：95/100 (S 级)
核心优势：RLHF 研究 + 开源项目 + 顶会论文
建议：最优先触达
```

### 示例 3: 生成个性化邮件

```
输入 / Input:
为 Yifan Bai 生成个性化邮件，突出他的 RLHF 研究

输出 / Output:
主题：[公司名] 高级算法工程师机会 - 看到您的 RLHF 研究很感兴趣

正文:
Bai 你好，

我最近拜读了您的论文《Kimi K2: Open Agentic Intelligence》(2025)，
特别是您提出的 MuonClip optimizer 让我印象深刻。
您在 OpenRLHF 项目中的实现也非常精彩，
特别是分布式 PPO 训练的设计。

我们正在招募高级算法工程师，主要负责 LLM 对齐和 RLHF 优化。
这个岗位需要深入的 RLHF 经验和强大的工程能力，与您的背景非常匹配。

...
```

---

**版本 / Version**: 1.0.2  
**作者 / Author**: 虾哥 AI Assistant / Shrimp Brother AI  
**最后更新 / Last Updated**: 2026-03-04  
**许可证 / License**: MIT

---

*注意：本 Skill 的部分功能需要配合 Feishu Bitable 使用，请确保已配置相关权限。*
*Note: Some features of this Skill require Feishu Bitable integration, please ensure proper permissions are configured.*
