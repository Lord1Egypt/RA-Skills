# TechRecruiter Pro 🎯

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw/skills/tree/main/skills/tech-recruiter-pro)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![ClawHub](https://img.shields.io/badge/ClawHub-ready-orange.svg)](https://www.clawhub.ai/)

**[English](README.md) | 简体中文**

专门针对**技术人员**（算法工程师 + 研发工程师）的智能化招聘助手。

## 🚀 核心功能

### 1. 多平台候选人搜索

| 平台 | 数据源 | 状态 |
|------|-------|------|
| **AMiner** | 学者档案、论文、H-index | ✅ |
| **Google Scholar** | 论文、引用、研究方向 | ✅ |
| **GitHub** | 仓库、代码质量、技术栈 | ✅ |
| **arXiv** | 最新论文、研究趋势 | ✅ |
| **顶会** | NeurIPS/ICML/CVPR/ACL 论文 | ✅ |
| **LinkedIn** | 职业经历、技能 | ⚠️ 需 API |
| **X (Twitter)** | 技术影响力、动态 | ⚠️ 需 API |

### 2. 智能画像分析

- **技术能力评估**: GitHub 代码质量、项目复杂度
- **学术影响力**: 论文数、引用数、H-index
- **社区贡献**: 开源项目、技术博客、演讲
- **匹配度评分**: 根据 JD 自动打分 (0-100)

### 3. 个性化邮件生成

基于以下信息定制：
- ✅ GitHub 项目经历
- ✅ Google Scholar 论文
- ✅ AMiner 研究轨迹
- ✅ 与职位的匹配点

### 4. 候选人 Pipeline 管理

```
发现 → 初筛 → 已联系 → 面试中 → Offer → 已入职
```

## 📦 安装

```bash
# 克隆或下载技能
cd /path/to/your/skills
git clone https://github.com/openclaw/skills.git

# 或通过 ClawHub 安装（即将上线）
npx clawhub@latest install tech-recruiter-pro
```

### 依赖

```bash
pip install requests beautifulsoup4 lxml
```

### 可选（增强功能）

```bash
# GitHub API（提高请求限制）
export GITHUB_TOKEN=your_token

# LinkedIn API
export LINKEDIN_API_KEY=your_key
export LINKEDIN_API_SECRET=your_secret

# Twitter API v2
export TWITTER_BEARER_TOKEN=your_token
```

## 🔧 配置

编辑 `config/config.ini`：

```ini
[search]
default_min_citations = 50
default_min_h_index = 10
max_results_per_search = 100

[platforms.github]
enabled = true
api_token = ""  # 可选

[platforms.google_scholar]
enabled = true
request_delay = 2  # 避免频率限制

[email]
default_language = zh-CN
company_name = "你的公司"
contact_email = "recruiting@company.com"
```

## 🚀 快速开始

### 1. 搜索候选人

```python
from recruiter import TechRecruiterPro

recruiter = TechRecruiterPro()

candidates = recruiter.search_candidates(
    keywords=["RLHF", "PPO", "LLM"],
    target_companies=["DeepMind", "OpenAI", "Moonshot"],
    min_citations=100,
    min_h_index=10
)

print(f"找到 {len(candidates)} 位候选人")
```

### 2. 分析候选人画像

```python
profile = recruiter.analyze_profile(
    github_url="https://github.com/username",
    scholar_url="https://scholar.google.com/citations?user=xxx",
    aminer_url="https://www.aminer.cn/profile/xxx"
)

print(f"姓名：{profile.name}")
print(f"匹配度：{profile.match_score}")
print(f"论文数：{profile.paper_count}")
print(f"总引用：{profile.total_citations}")
print(f"H-index: {profile.h_index}")
```

### 3. 生成个性化邮件

```python
job_desc = {
    "company": "某某 AI",
    "position": "高级算法工程师",
    "research_direction": "大模型对齐",
    "responsibility_1": "负责 RLHF 算法研发",
    "responsibility_2": "优化大规模训练",
    "skill_1": "深度强化学习",
    "skill_2": "PyTorch/JAX"
}

email = recruiter.generate_email(profile, job_desc)
print(email)
```

### 4. 管理 Pipeline

```python
# 更新候选人状态
profile.status = "已联系"
profile.next_followup = "2026-03-10"

# 保存到数据库
recruiter.save_candidate(profile)

# 导出报告
recruiter.export_report("recruiting_report_20260303.md")
```

## 📊 使用示例

### 示例 1: 搜索 AI 研究员

```python
# 搜索 RLHF 方向研究员
candidates = recruiter.search_candidates(
    keywords=["RLHF", "PPO", "LLM Alignment"],
    target_companies=["DeepMind", "OpenAI", "Anthropic"],
    min_citations=200,
    min_h_index=15
)

# 筛选高优先级
high_priority = [c for c in candidates if c.match_score >= 80]
print(f"高优先级：{len(high_priority)}")
```

### 示例 2: 深度画像分析

```python
# 从多源分析
profile = recruiter.analyze_profile(
    github_url="https://github.com/username",
    scholar_url="https://scholar.google.com/citations?user=xxx",
    aminer_url="https://www.aminer.cn/profile/xxx"
)

# 获取详细分析
analysis = recruiter.get_detailed_analysis(profile)
print(analysis)
```

### 示例 3: 生成定制邮件

```python
email = recruiter.generate_email(
    candidate=profile,
    job_description=job_desc,
    template_type="initial_outreach"
)

# 亮点：
# - 提及候选人的顶级论文
# - 引用 GitHub 项目
# - 强调职位匹配点
```

## 📧 邮件模板

### 初次联系

```
主题：[{公司名}] {职位} 机会 - 看到您的{研究方向}工作很感兴趣

{name}您好，

我最近拜读了您的论文《{paper_title}》({year})，
特别是您提出的{method_highlight}让我印象深刻。

您在 GitHub 项目 {github_project} 中的实现也非常精彩。

我们正在招募 {position}，主要负责{research_direction}...

如果您感兴趣，我们可以安排 30 分钟电话沟通...

祝好，
{recruiter_name}
```

### 跟进模板

- **跟进 1**: 初次联系后 3-5 天
- **跟进 2**: 第一次跟进后 5-7 天（最后尝试）

### 面试邀请

包含面试流程、时间安排、准备建议。

## 🗄️ 数据结构

### 候选人画像

```json
{
  "姓名": "Yifan Bai",
  "当前公司": "Moonshot AI",
  "职位": "Research Scientist",
  "研究方向": ["LLM", "RLHF", "Agentic AI"],
  "论文数": 15,
  "总引用": 2500,
  "H-index": 18,
  "GitHub": "https://github.com/xxx",
  "Google Scholar": "https://scholar.google.com/xxx",
  "AMiner": "https://www.aminer.cn/profile/xxx",
  "匹配度": 92,
  "状态": "初筛通过",
  "优先级": "高"
}
```

## 📈 效果追踪

| 指标 | 计算公式 | 目标 |
|------|---------|------|
| 回复率 | 回复数/发送数 | >30% |
| 面试率 | 面试数/回复数 | >50% |
| Offer 率 | Offer 数/面试数 | >30% |
| 接受率 | 接受数/Offer 数 | >70% |
| 平均招聘周期 | 发现→入职天数 | <45 天 |

## 🔌 集成

### 飞书 (Lark)

```python
# 保存到飞书多维表格
from feishu_bitable import save_candidate

save_candidate(
    app_token="xxx",
    table_id="yyy",
    fields=profile.to_dict()
)
```

### 导出格式

- Markdown (`.md`)
- CSV (`.csv`)
- JSON (`.json`)

## ⚠️ 合规与道德

### 法律合规

- ✅ 仅使用公开信息
- ✅ 遵守 GDPR/隐私法规
- ✅ 提供 opt-out 选项
- ❌ 不使用非法渠道
- ❌ 不购买候选人数据

### 最佳实践

- 尊重候选人意愿
- 不频繁骚扰（最多 3 次跟进）
- 诚实介绍职位
- 保护候选人隐私

## 🧪 测试

```bash
# 运行测试
python -m pytest tests/

# 运行示例
python examples/search_example.py
python examples/analysis_example.py
python examples/email_example.py
```

## 📚 文档

- [快速上手指南](QUICKSTART.md)
- [API 参考](docs/API.md)
- [配置指南](docs/CONFIGURATION.md)
- [最佳实践](docs/BEST_PRACTICES.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 仓库
2. 创建功能分支
3. 进行修改
4. 添加测试
5. 提交 PR

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- [AMiner](https://www.aminer.cn/) - 学者搜索平台
- [Google Scholar](https://scholar.google.com/) - 学术论文
- [GitHub](https://github.com/) - 代码仓库
- [arXiv](https://arxiv.org/) - 预印本论文

## 📞 支持

- **Issues**: https://github.com/openclaw/skills/issues
- **Discussions**: https://github.com/openclaw/skills/discussions
- **邮箱**: support@openclaw.ai

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**作者**: 虾哥 AI Assistant
