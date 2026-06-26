---
name: public-relations-manager
display_name: Public Relations Manager
version: 1.0.0
author: ZhenStaff
category: productivity
tags:
  - pr
  - public-relations
  - media-relations
  - press-release
  - content-calendar
  - media-pitch
  - marketing
  - communications
license: MIT
homepage: https://github.com/ZhenRobotics/openclaw-public-relations-manager
repository: https://github.com/ZhenRobotics/openclaw-public-relations-manager
---

# Public Relations Manager 📰

> AI-Powered Public Relations Assistant for OpenClaw

**Version**: 1.0.0 | **Status**: Production Ready ✅

---

## 📋 Description

Public Relations Manager is a comprehensive AI-powered public relations assistant that helps PR professionals, marketers, and founders manage their media relations, create compelling content, and plan strategic campaigns.

**Perfect for**:
- 🎯 PR Professionals - Manage media databases and outreach efficiently
- 🚀 Startups - Announce funding rounds and product launches professionally
- 📢 Marketing Teams - Coordinate content calendars and multi-channel campaigns

---

## ✨ Core Features

### 1. 🎯 Media Matching Engine
Intelligently match your story with the right journalists and media outlets using a 4-dimensional AI scoring algorithm:

- **Category Match (40%)**: Direct + related category alignment
- **Influence Level (30%)**: Top-tier vs mid-tier vs niche outlets
- **Relationship (15%)**: Response rate + interaction history
- **Relevance (15%)**: Audience fit + outlet characteristics

**Recommendation Levels**:
- 🟢 **Highly Recommended** (80-100): Perfect fit, pitch immediately
- 🟡 **Recommended** (65-79): Strong match, good opportunity
- 🟠 **Maybe** (50-64): Possible fit, consider context
- 🔴 **Not Suitable** (<50): Poor match, skip

### 2. 📰 Press Release Generation
Generate professional press releases for:
- 📱 **Product Launches**: Feature announcements, new releases
- 💰 **Funding Rounds**: Series A/B/C, seed rounds
- 🤝 **Partnerships**: Strategic alliances, integrations

Each template includes:
- Professional headline generation
- Structured body paragraphs
- Quote formatting
- Company boilerplate
- Contact information module

### 3. ✉️ Media Pitch Creation
Create personalized media pitches with:
- **Custom subject lines** tailored to journalist interests
- **Journalist-specific personalization** based on their beat
- **Exclusive offer support** for unique story opportunities
- **Follow-up templates** for continued engagement

### 4. 📅 Campaign Planning
Plan comprehensive PR campaigns with:
- **Multi-week content calendars** (4-8 weeks)
- **Content scheduling** by date and type
- **Deadline tracking** for upcoming and overdue items
- **AI-powered content suggestions** based on campaign goals

---

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install openclaw-public-relations-manager
```

### From ClawHub
```bash
clawhub install public-relations-manager
```

### From GitHub Source
```bash
git clone https://github.com/ZhenRobotics/openclaw-public-relations-manager
cd openclaw-public-relations-manager
pip install -e .
```

---

## 🚀 Quick Start

```python
from pr_manager import PRManager, MediaCategory

# Initialize PR Manager
pr = PRManager()

# Load sample media database (5 outlets + 5 journalists)
from pr_manager.data import load_sample_media_database
outlets, journalists = load_sample_media_database()
for outlet in outlets:
    pr.add_media_outlet(outlet)
for journalist in journalists:
    pr.add_journalist(journalist)

# Match a story to relevant media
result = pr.match_story_to_media(
    story_title="Company Raises $10M Series A",
    story_categories=[MediaCategory.TECH, MediaCategory.STARTUP],
    min_score=60.0
)

print(f"Found {len(result.matches)} relevant media contacts")
for match in result.get_top_matches(5):
    print(f"{match.target_name}: {match.overall_score}/100")
```

---

## 📝 Usage Examples

### Example 1: Generate Press Release

```python
# Generate a product launch press release
press_release = pr.generate_product_launch_pr(
    company_name="YourCompany",
    product_name="YourProduct",
    key_benefit="streamline team collaboration",
    problem_solved="the challenge of remote coordination",
    key_features=[
        "Real-time collaboration",
        "AI-powered automation",
        "Enterprise security"
    ],
    availability="available immediately",
    pricing="Starting at $99/month",
    quotes=[
        {
            "speaker": "CEO Name",
            "title": "CEO",
            "company": "YourCompany",
            "text": "This is a game-changer for our industry."
        }
    ],
    boilerplate="About YourCompany: Leading software provider...",
    contact_info={"Name": "PR Team", "Email": "pr@company.com"},
    location="San Francisco, CA"
)

# Save as markdown
with open("press_release.md", "w") as f:
    f.write(press_release.to_markdown())
```

### Example 2: Quick Match and Pitch Workflow

```python
# Match story to journalists and generate pitches in one step
results = pr.quick_match_and_pitch(
    story_title="AI Startup Disrupts Industry",
    story_categories=[MediaCategory.TECH, MediaCategory.STARTUP],
    story_hook="Company launches breakthrough AI technology",
    story_details="The platform automates complex workflows...",
    why_relevant="This aligns with your AI coverage.",
    top_n=5
)

# Review and send to top 5 matched journalists
for journalist, pitch in results:
    print(f"\nTo: {journalist.email}")
    print(f"Subject: {pitch.subject_line}")
    print(pitch.to_email())
```

### Example 3: Plan PR Campaign

```python
from datetime import date, timedelta

# Create a 6-week product launch campaign
campaign = pr.create_campaign(
    name="Product Launch Q2",
    goal="product_launch",
    description="Comprehensive launch campaign",
    start_date=date.today() + timedelta(days=14),
    duration_weeks=6,
    target_categories=[MediaCategory.TECH, MediaCategory.BUSINESS],
    key_messages=[
        "Revolutionary AI technology",
        "10x productivity improvement",
        "Enterprise-ready security"
    ],
    budget=75000
)

# Get AI-suggested content for the campaign
planner = pr.calendar_planner
suggestions = planner.suggest_campaign_content(campaign)

for suggestion in suggestions:
    print(f"{suggestion['title']} - {suggestion['content_type'].value}")
```

---

## 📊 Sample Database

The skill includes realistic sample data:

**Media Outlets** (5):
- 🚀 TechCrunch - Top-tier tech coverage
- 📰 The Wall Street Journal - Business/finance authority
- 💼 VentureBeat - Mid-tier tech news
- 💰 Forbes - Business and entrepreneurship
- 🔍 The Information - Tech insider coverage

**Journalists** (5):
- Profiles with beat coverage, contact info, response rates
- Recent article lists
- Influence level classification

---

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_pr_manager.py
```

All 6 core tests pass with 100% success rate:
- ✅ Media matching engine
- ✅ Press release generation
- ✅ Media pitch creation
- ✅ Content calendar planning
- ✅ Quick workflows
- ✅ Database management

---

## 🔧 Parameters & Configuration

### MediaCategory Enum
```python
MediaCategory.TECH        # Technology
MediaCategory.STARTUP     # Startups & entrepreneurship
MediaCategory.BUSINESS    # General business
MediaCategory.FINANCE     # Finance & investment
MediaCategory.CONSUMER    # Consumer products
MediaCategory.ENTERPRISE  # Enterprise software
MediaCategory.LIFESTYLE   # Lifestyle & culture
MediaCategory.HEALTH      # Healthcare & wellness
```

### InfluenceLevel Enum
```python
InfluenceLevel.TOP_TIER   # Major outlets (NYT, WSJ, TechCrunch)
InfluenceLevel.MID_TIER   # Industry publications
InfluenceLevel.NICHE      # Specialized blogs/newsletters
InfluenceLevel.EMERGING   # New/growing platforms
```

---

## 🗺️ Roadmap

### v1.1 (Planned)
- 📊 Analytics dashboard for campaign performance
- 📧 Email integration for automated sending
- 📈 Media coverage tracking
- 💬 Sentiment analysis

### v1.2 (Planned)
- 🔌 CRM integrations (HubSpot, Salesforce)
- 🌍 Multi-language support
- 📦 Press kit generation
- 🔔 Media monitoring alerts

### v2.0 (Future)
- 🤖 AI-powered newsjacking suggestions
- 🔍 Competitive PR intelligence
- ⏰ Automated follow-up scheduling
- 💵 ROI measurement tools

---

## 📚 Resources

- **GitHub**: https://github.com/ZhenRobotics/openclaw-public-relations-manager
- **PyPI**: https://pypi.org/project/openclaw-public-relations-manager/
- **Documentation**: [README.md](https://github.com/ZhenRobotics/openclaw-public-relations-manager/blob/main/README.md)
- **Contributing**: [CONTRIBUTING.md](https://github.com/ZhenRobotics/openclaw-public-relations-manager/blob/main/CONTRIBUTING.md)
- **Issues**: https://github.com/ZhenRobotics/openclaw-public-relations-manager/issues

---

## 🤝 Support

- **Email**: code@zhenrobot.com
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and community support

---

## 📄 License

MIT License - Open source and free to use

---

## 👥 Credits

**Author**: Justin Wang
**Co-Author**: Claude Sonnet 4.5
**Organization**: ZhenRobotics

---

## 📊 Technical Details

- **Language**: Python 3.10+
- **Platforms**: Linux, macOS, Windows
- **Dependencies**: pydantic>=2.5.0, python-dateutil>=2.8.0
- **Code Size**: 4,078 lines across 27 modules
- **Test Coverage**: 6 comprehensive tests (100% pass rate)
- **Architecture**: Modular design with clear separation of concerns

---

## 🎯 Best Practices

### For PR Professionals
1. Build your media database gradually
2. Track journalist response rates
3. Personalize every pitch
4. Follow up strategically

### For Startups
1. Prepare boilerplate and quotes in advance
2. Time announcements strategically
3. Build relationships before you need them
4. Measure and iterate

### For Marketing Teams
1. Plan campaigns 4-6 weeks ahead
2. Align messaging across channels
3. Track all media interactions
4. Maintain consistent brand voice

---

**🎊 Ready to transform your PR workflow? Install now and start managing media relations like a pro!**

```bash
clawhub install public-relations-manager
```
