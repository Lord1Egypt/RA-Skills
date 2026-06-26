# 🚀 TechRecruiter Pro 发布说明

## 技能信息

**名称**: TechRecruiter Pro  
**版本**: 1.0.0  
**分类**: Productivity / Recruiting  
**许可证**: MIT

## 简介

**英文**: 
Intelligent recruiting assistant for technical talents. Search candidates across 9 platforms (GitHub, Google Scholar, AMiner, arXiv, LinkedIn, Reddit, Discord, Hugging Face, X). Features smart profile analysis, personalized email generation, and pipeline management.

**中文**:
专门针对技术人员的智能化招聘助手。支持 9 大平台搜索（GitHub、Google Scholar、AMiner、arXiv、LinkedIn、Reddit、Discord、Hugging Face、X）。具备智能画像分析、个性化邮件生成和 Pipeline 管理功能。

## 核心功能

1. **9 大平台搜索**
   - AMiner, Google Scholar, GitHub, arXiv
   - LinkedIn, Reddit, Discord
   - Hugging Face, X (Twitter)

2. **智能画像分析**
   - 技术能力评估
   - 学术影响力分析
   - 匹配度评分 (0-100)

3. **个性化邮件生成**
   - 基于论文/项目定制
   - 多模板支持
   - 中英双语

4. **Pipeline 管理**
   - 状态追踪
   - 自动跟进
   - 报告导出

## 使用示例

```python
# 搜索候选人
recruiter.search_candidates(
    keywords=["RLHF", "LLM"],
    target_companies=["DeepMind", "OpenAI"],
    min_citations=100
)

# 分析候选人
profile = recruiter.analyze_profile(
    github_url="https://github.com/xxx",
    scholar_url="https://scholar.google.com/xxx"
)

# 生成邮件
email = recruiter.generate_email(profile, job_desc)
```

## 技术栈

- Python 3.8+
- requests, beautifulsoup4, lxml
- 飞书集成 (Bitable, Doc, Chat)

## 依赖

```
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
```

## 配置

需要配置 API Token（可选）：
- GitHub API Token
- LinkedIn API Key
- Twitter Bearer Token
- Hugging Face Token

## 测试

```bash
python3 -m pytest tests/ -v
python3 examples/all_platforms_example.py
```

## 文档

- README.md (英文)
- README_zh-CN.md (中文)
- QUICKSTART.md (快速上手)
- docs/ (详细指南)

## 创新点

1. **ClawHub 首个招聘技能** - 填补市场空白
2. **9 平台集成** - 全方位覆盖
3. **AI 驱动分析** - 智能匹配度评分
4. **个性化邮件** - 基于论文/项目定制
5. **完整文档** - 中英双语

## 目标用户

- HR/招聘团队
- 技术负责人
- 创业公司创始人
- 猎头顾问

## 竞争优势

| 特性 | TechRecruiter Pro | 传统招聘工具 |
|-----|------------------|-------------|
| 平台覆盖 | 9 个 | 1-2 个 |
| 智能化 | AI 驱动 | 手动筛选 |
| 个性化 | 自动定制 | 通用模板 |
| 价格 | 免费 | 昂贵订阅 |
| 集成 | 飞书/Slack | 独立系统 |

## 发布计划

- **v1.0.0** (2026-03-03): 初始版本
- **v1.1.0** (Q2 2026): LinkedIn API 集成
- **v1.2.0** (Q3 2026): AI 匹配度优化
- **v2.0.0** (Q4 2026): 完整 ATS 系统

## 联系方式

- **作者**: 虾哥 AI Assistant
- **邮箱**: support@openclaw.ai
- **GitHub**: https://github.com/openclaw/skills

## 许可证

MIT License - 开源免费使用

---

**发布日期**: 2026-03-03  
**版本**: 1.0.0  
**状态**: Ready to Publish
