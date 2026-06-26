# Political Commentator - AI Skill

An intelligent political news commentator skill for OpenClaw AI assistant. Helps users collect hot political news, analyze events, and generate multi-format commentary content.

## 🌟 Features

### Stage 1: News Collection
- Fetch hot political news from multiple sources (Taiwan, China, International)
- Support for 20+ news sources including CNA, BBC, CNN, Reuters, Xinhua
- Smart filtering and deduplication
- Relevance ranking by popularity

### Stage 2: Interest Selection
- Interactive selection interface
- Filter by tags: #CrossStrait #Elections #Diplomacy #Economics
- Keyword search support
- User preference memory

### Stage 3: Deep Analysis
- 5W1H analysis framework
- Multi-perspective viewpoint analysis
- Stakeholder interest analysis
- Trend prediction (short/medium/long term)

### Stage 4: Content Output
- 📄 Full commentary articles (1500-3000 words)
- 🎙️ Video/Podcast scripts
- 📱 Social media posts (Twitter/IG/Facebook)
- 📊 Visual analysis cards

### Commentary Styles
- ⚖️ **Neutral/Objective** - Present facts and multiple viewpoints
- 🔍 **Critical Analysis** - In-depth critique with analytical lens
- 😂 **Satirical/Humorous** - Witty commentary with humor
- 📚 **Academic** - Scholarly analysis with theoretical frameworks

## 🚀 Usage

### Trigger Commands
- "Comment on today's political news"
- "What's happening with cross-strait relations?"
- "I want to write about US-China relations"
- "Analyze this news" + paste link

### Workflow
1. AI displays today's news list
2. User selects interesting topics
3. AI performs deep analysis
4. AI generates commentary content
5. User can modify style/format and regenerate

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/political-commentator.git

# The skill will be automatically loaded by OpenClaw
```

## 📁 Project Structure

```
political-commentator/
├── SKILL.md                          # Main skill definition
├── references/
│   ├── news-sources.md               # Complete news source list
│   ├── analysis-framework.md          # Deep analysis framework
│   └── templates/
│       ├── article-template.md        # Long-form article template
│       ├── social-template.md         # Social media template
│       └── script-template.md         # Video script template
├── scripts/
│   └── fetch-news.py                 # News fetching script
└── memory/
    └── user-preferences.json          # User preferences
```

## 🔧 Supported News Sources

### Taiwan
| Source | URL | Notes |
|--------|-----|-------|
| CNA | cna.com.tw | Official news agency, neutral |
| Liberty Times | ltn.com.tw | Pro-green |
| United Daily News | udn.com | Pro-blue |
| SET News | settv.net | Television news |

### China
| Source | URL | Notes |
|--------|-----|-------|
| Xinhua | xinhuanet.com | Official |
| People's Daily | people.com.cn | Official |
| Phoenix News | ifeng.com | Semi-official |

### International
| Source | URL | Notes |
|--------|-----|-------|
| BBC | bbc.com/news/politics | UK |
| CNN | cnn.com/politics | US |
| Reuters | reuters.com | Global |
| Al Jazeera | aljazeera.com | Middle East |

## 📝 Output Formats

### Full Article
```
Title: [Angle] + [Core Event] + [Engaging Hook]

Structure:
- Introduction (150-300 words)
- Background (300-500 words)
- Multiple Perspectives (400-600 words)
- Deep Analysis (500-800 words)
- Trend Prediction (300-500 words)
- Conclusion (150-300 words)
```

### Social Media Post
```
Hook (20-40 chars)
↓
Core Argument (50-80 chars)
↓
Supporting Evidence (50-100 chars)
↓
Call to Action (20-30 chars)
```

### Video Script
```
Hook (0-30s) → Background (1-3min) → 
Perspectives (2-4min) → Analysis (3-5min) → 
Summary (1-2min) → CTA (30-60s)
```

## 🔒 Privacy

- All user preferences are stored locally
- No data is sent to external servers
- News data is fetched in real-time from public sources

## 📄 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.
