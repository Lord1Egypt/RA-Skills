# TechRecruiter Pro 🎯

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw/skills/tree/main/skills/tech-recruiter-pro)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![ClawHub](https://img.shields.io/badge/ClawHub-ready-orange.svg)](https://www.clawhub.ai/)

**English | [简体中文](README_zh-CN.md)**

Intelligent recruiting assistant specifically designed for **technical talents** (Algorithm Engineers + R&D Engineers).

## 🚀 Features

### 1. Multi-Platform Candidate Search

| Platform | Data Sources | Status |
|----------|-------------|--------|
| **AMiner** | Scholar profiles, papers, H-index | ✅ |
| **Google Scholar** | Publications, citations, research areas | ✅ |
| **GitHub** | Repositories, code quality, tech stack | ✅ |
| **arXiv** | Latest papers, research trends | ✅ |
| **Conference** | NeurIPS/ICML/CVPR/ACL papers | ✅ |
| **LinkedIn** | Career history, skills, education | ✅ |
| **Reddit** | Tech communities, discussions | ✅ |
| **Discord** | AI/ML servers, user activity | ✅ |
| **Hugging Face** | Models, datasets, code | ✅ |
| **X (Twitter)** | Tech influence, social media | ✅ |

### 2. Smart Profile Analysis

- **Technical Assessment**: GitHub code quality, project complexity
- **Academic Impact**: Paper count, citations, H-index
- **Community Contribution**: Open source, tech blogs, talks
- **Matching Score**: Auto-calculate fit (0-100) based on JD

### 3. Personalized Email Generation

Generate customized outreach emails based on:
- ✅ GitHub project experience
- ✅ Google Scholar publications
- ✅ AMiner research trajectory
- ✅ Job matching points

### 4. Candidate Pipeline Management

```
Sourced → Screened → Contacted → Interviewing → Offer → Hired
```

## 📦 Installation

```bash
# Clone or download the skill
cd /path/to/your/skills
git clone https://github.com/openclaw/skills.git

# Or install via ClawHub (coming soon)
npx clawhub@latest install tech-recruiter-pro
```

### Dependencies

```bash
pip install requests beautifulsoup4 lxml
```

### Optional (Enhanced Features)

```bash
# GitHub API (for higher rate limits)
export GITHUB_TOKEN=your_token

# LinkedIn API
export LINKEDIN_API_KEY=your_key
export LINKEDIN_API_SECRET=your_secret

# Twitter API v2
export TWITTER_BEARER_TOKEN=your_token
```

## 🔧 Configuration

Edit `config/config.ini`:

```ini
[search]
default_min_citations = 50
default_min_h_index = 10
max_results_per_search = 100

[platforms.github]
enabled = true
api_token = ""  # Optional

[platforms.google_scholar]
enabled = true
request_delay = 2  # Avoid rate limiting

[email]
default_language = zh-CN
company_name = "Your Company"
contact_email = "recruiting@company.com"
```

## 🚀 Quick Start

### 1. Search Candidates

```python
from recruiter import TechRecruiterPro

recruiter = TechRecruiterPro()

candidates = recruiter.search_candidates(
    keywords=["RLHF", "PPO", "LLM"],
    target_companies=["DeepMind", "OpenAI", "Moonshot"],
    min_citations=100,
    min_h_index=10
)

print(f"Found {len(candidates)} candidates")
```

### 2. Analyze Profile

```python
profile = recruiter.analyze_profile(
    github_url="https://github.com/username",
    scholar_url="https://scholar.google.com/citations?user=xxx",
    aminer_url="https://www.aminer.cn/profile/xxx"
)

print(f"Name: {profile.name}")
print(f"Match Score: {profile.match_score}")
print(f"Papers: {profile.paper_count}")
print(f"Citations: {profile.total_citations}")
print(f"H-index: {profile.h_index}")
```

### 3. Generate Personalized Email

```python
job_desc = {
    "company": "Your AI Company",
    "position": "Senior Algorithm Engineer",
    "research_direction": "LLM Alignment",
    "responsibility_1": "Lead RLHF algorithm development",
    "responsibility_2": "Optimize large-scale training",
    "skill_1": "Deep reinforcement learning",
    "skill_2": "PyTorch/JAX"
}

email = recruiter.generate_email(profile, job_desc)
print(email)
```

### 4. Manage Pipeline

```python
# Update candidate status
profile.status = "Contacted"
profile.next_followup = "2026-03-10"

# Save to database
recruiter.save_candidate(profile)

# Export report
recruiter.export_report("recruiting_report_20260303.md")
```

## 📊 Usage Examples

### Example 1: Source AI Researchers

```python
# Search for RLHF researchers
candidates = recruiter.search_candidates(
    keywords=["RLHF", "PPO", "LLM Alignment"],
    target_companies=["DeepMind", "OpenAI", "Anthropic"],
    min_citations=200,
    min_h_index=15
)

# Filter high priority
high_priority = [c for c in candidates if c.match_score >= 80]
print(f"High priority: {len(high_priority)}")
```

### Example 2: Deep Profile Analysis

```python
# Analyze from multiple sources
profile = recruiter.analyze_profile(
    github_url="https://github.com/username",
    scholar_url="https://scholar.google.com/citations?user=xxx",
    aminer_url="https://www.aminer.cn/profile/xxx"
)

# Get detailed analysis
analysis = recruiter.get_detailed_analysis(profile)
print(analysis)
```

### Example 3: Generate Customized Email

```python
email = recruiter.generate_email(
    candidate=profile,
    job_description=job_desc,
    template_type="initial_outreach"
)

# Highlights:
# - Mentions candidate's top paper
# - References GitHub projects
# - Emphasizes job matching points
```

## 📧 Email Templates

### Initial Outreach

```
Subject: [{company}] {position} Opportunity - Interested in Your {research_area} Work

Dear {name},

I recently read your paper "{paper_title}" ({year}), and I was particularly 
impressed by your {method_highlight}.

Your implementation in {github_project} is also excellent, especially the 
{project_highlight} design.

We are recruiting for {position} at {company}, focusing on {research_direction}.
This role requires {key_skill_1}, {key_skill_2}, which matches your background well.

Would you be available for a 30-minute call next week?

Best regards,
{recruiter_name}
```

### Follow-up Templates

- **Follow-up 1**: 3-5 days after initial contact
- **Follow-up 2**: 5-7 days after first follow-up (final attempt)

### Interview Invitation

Includes interview process, scheduling, and preparation tips.

## 🗄️ Data Structure

### Candidate Profile

```json
{
  "name": "Yifan Bai",
  "current_company": "Moonshot AI",
  "position": "Research Scientist",
  "research_areas": ["LLM", "RLHF", "Agentic AI"],
  "paper_count": 15,
  "total_citations": 2500,
  "h_index": 18,
  "github": "https://github.com/xxx",
  "google_scholar": "https://scholar.google.com/xxx",
  "aminer": "https://www.aminer.cn/profile/xxx",
  "match_score": 92,
  "status": "Screened",
  "priority": "High"
}
```

## 📈 Metrics Tracking

| Metric | Formula | Target |
|--------|---------|--------|
| Reply Rate | Replies / Sent | >30% |
| Interview Rate | Interviews / Replies | >50% |
| Offer Rate | Offers / Interviews | >30% |
| Acceptance Rate | Accepts / Offers | >70% |
| Avg Time to Hire | Days (Source → Hire) | <45 |

## 🔌 Integrations

### Feishu (Lark)

```python
# Save to Feishu Bitable
from feishu_bitable import save_candidate

save_candidate(
    app_token="xxx",
    table_id="yyy",
    fields=profile.to_dict()
)
```

### Export Formats

- Markdown (`.md`)
- CSV (`.csv`)
- JSON (`.json`)

## ⚠️ Compliance & Ethics

### Legal Compliance

- ✅ Use only public information
- ✅ Comply with GDPR/privacy laws
- ✅ Provide opt-out option
- ❌ No illegal data sources
- ❌ No purchasing candidate data

### Best Practices

- Respect candidate preferences
- Don't spam (max 3 follow-ups)
- Be honest about the role
- Protect candidate privacy

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run examples
python examples/search_example.py
python examples/analysis_example.py
python examples/email_example.py
```

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md)
- [API Reference](docs/API.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Best Practices](docs/BEST_PRACTICES.md)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [AMiner](https://www.aminer.cn/) - Scholar search platform
- [Google Scholar](https://scholar.google.com/) - Academic papers
- [GitHub](https://github.com/) - Code repositories
- [arXiv](https://arxiv.org/) - Preprint papers

## 📞 Support

- **Issues**: https://github.com/openclaw/skills/issues
- **Discussions**: https://github.com/openclaw/skills/discussions
- **Email**: support@openclaw.ai

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-03  
**Author**: 虾哥 AI Assistant
