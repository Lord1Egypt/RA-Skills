---
name: skill-recommender-pro
description: Intelligent skill recommendations for OpenClaw. Analyzes installed skills using rule-based filtering and pattern matching. Suggests complementary skills, alternatives, and gap-fillers. Supports multi-language output.
version: 1.0.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎯", "requires": {"bins": ["python3"]}}}
---

# Skill Recommender Pro

Intelligent skill recommendation engine for OpenClaw. Goes beyond simple search to provide personalized, context-aware recommendations.

## What Makes This Better

| Feature | Other Recommenders | skill-recommender-pro |
|---------|-------------------|----------------------|
| Basic search | ✅ | ✅ |
| Installed skills analysis | ❌ | ✅ |
| Complementary recommendations | ❌ | ✅ |
| Alternative suggestions | ❌ | ✅ |
| Personalized by role | ❌ | ✅ |
| Semantic analysis | ❌ | ✅ (agent-assisted) |
| Multi-language | ❌ | ✅ |

## Trigger Conditions

- "Recommend skills for me" / "推荐skills给我"
- "What skills should I install?" / "我应该安装什么skills？"
- "Find alternatives to X" / "找X的替代品"
- "Compare X and Y skills" / "对比X和Y这两个skill"
- "What's missing in my setup?" / "我的配置缺少什么？"
- "Best skills for developers" / "开发者最佳skills"
- "skill-recommender-pro"

---

## Step 1: Analyze User's Current Setup

First, understand what the user already has:

```bash
# Get installed skills
clawhub list 2>/dev/null || echo "No skills installed"
```

### Analysis Script

```python
python3 << 'PYEOF'
import json
import subprocess
import os

def get_installed_skills():
    """Get list of installed skills"""
    try:
        result = subprocess.run(
            ["clawhub", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
    except:
        pass
    return []

def categorize_skills(skills):
    """Categorize installed skills by function"""
    categories = {
        "development": ["github", "git", "code", "debug", "test"],
        "research": ["search", "research", "analyze", "summarize"],
        "productivity": ["calendar", "email", "task", "note", "todo"],
        "media": ["image", "video", "audio", "tts", "ocr"],
        "data": ["csv", "json", "database", "sql", "api"],
        "ai": ["llm", "model", "train", "embedding"],
        "devops": ["docker", "deploy", "ci", "cd", "cloud"]
    }
    
    user_categories = {}
    for skill in skills:
        skill_lower = skill.lower()
        for category, keywords in categories.items():
            if any(kw in skill_lower for kw in keywords):
                user_categories.setdefault(category, []).append(skill)
    
    return user_categories

def identify_gaps(installed, categories):
    """Identify missing categories that could be useful"""
    all_categories = set(categories.keys())
    user_categories = set(installed.keys())
    gaps = all_categories - user_categories
    return list(gaps)

installed = get_installed_skills()
categories = categorize_skills(installed)
gaps = identify_gaps(categories, {})

print(f"Installed skills: {len(installed)}")
print(f"Categories covered: {list(categories.keys())}")
print(f"Potential gaps: {gaps}")
PYEOF
```

---

## Step 2: Generate Recommendations

Based on analysis, generate personalized recommendations:

### Recommendation Types

```
1. Complementary Skills
   - Skills that work well with what you have
   - Example: If you have china-doc-ocr, recommend china-summarizer

2. Alternative Skills
   - Better options for same functionality
   - Based on downloads, ratings, freshness

3. Gap Filling
   - Skills for missing categories
   - Based on your apparent role/needs

4. Trending Skills
   - Popular skills in the community
   - Recent high-growth skills
```

### Search & Recommend

```bash
# For each gap, search for top skills
for category in research productivity devops; do
  echo "🔍 Searching for $category skills..."
  clawhub search "$category" 2>&1 | head -5
done
```

### Generate Report

```python
python3 << 'PYEOF'
import json

def generate_recommendations(installed, gaps, lang="en"):
    """Generate personalized recommendations"""
    
    recommendations = {
        "complementary": [],
        "alternatives": [],
        "gap_fillers": [],
        "trending": []
    }
    
    # Complementary pairs
    COMPLEMENTARY_MAP = {
        "china-doc-ocr": ["china-summarizer", "china-tts"],
        "china-tts": ["china-video-gen", "china-image-gen"],
        "research-orchestrator": ["skill-advisor", "web-search"],
        "skill-studio": ["skill-advisor", "research-orchestrator"]
    }
    
    for skill in installed:
        if skill in COMPLEMENTARY_MAP:
            for rec in COMPLEMENTARY_MAP[skill]:
                if rec not in installed:
                    recommendations["complementary"].append({
                        "skill": rec,
                        "reason": f"Works well with {skill}"
                    })
    
    return recommendations

# Example
installed = ["china-doc-ocr", "china-tts", "skill-studio"]
gaps = ["research", "devops"]
recs = generate_recommendations(installed, gaps, "zh")

print(json.dumps(recs, indent=2, ensure_ascii=False))
PYEOF
```

---

## Step 3: Output Recommendation Report

### Chinese Report Format

```
┌─────────────────────────────────────────────────────────┐
│  🎯 个性化Skill推荐                                      │
│  基于你已安装的 5 个skills                                │
└─────────────────────────────────────────────────────────┘

━━━ 📋 推荐报告 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 你的Skills概况
├─ 已安装: china-doc-ocr, china-tts, skill-studio...
├─ 覆盖领域: 文档处理, 语音, 开发工具
└─ 潜在缺口: 研究分析, DevOps

🔥 互补推荐（与你现有skills配合使用）
├─ china-summarizer - 与china-doc-ocr配合，OCR后自动总结
├─ research-orchestrator - 与skill-studio配合，创建研究类skills
└─ skill-advisor - 安装前评估skills安全性

⭐ 热门推荐（社区最受欢迎）
├─ capability-evolver (35K+ downloads) - Agent自我进化
├─ gog (14K+ downloads) - Google Workspace集成
└─ agent-browser (11K+ downloads) - 浏览器自动化

🎯 填补缺口（你可能需要的领域）
├─ 研究分析: research-orchestrator, summarize
├─ DevOps: docker-manager, deploy-helper
└─ 生产力: calendar, email-integration

💡 安装建议
clawhub install china-summarizer research-orchestrator skill-advisor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### English Report Format

```
┌─────────────────────────────────────────────────────────┐
│  🎯 Personalized Skill Recommendations                  │
│  Based on your 5 installed skills                       │
└─────────────────────────────────────────────────────────┘

━━━ 📋 Recommendation Report ━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Your Skills Overview
├─ Installed: china-doc-ocr, china-tts, skill-studio...
├─ Categories: Document Processing, Voice, Dev Tools
└─ Potential Gaps: Research, DevOps

🔥 Complementary (Works with your existing skills)
├─ china-summarizer - Pair with china-doc-ocr for OCR+summary
├─ research-orchestrator - Pair with skill-studio for research
└─ skill-advisor - Pre-install security assessment

⭐ Popular (Community Favorites)
├─ capability-evolver (35K+ downloads) - Agent self-improvement
├─ gog (14K+ downloads) - Google Workspace integration
└─ agent-browser (11K+ downloads) - Browser automation

🎯 Gap Fillers (Areas you might need)
├─ Research: research-orchestrator, summarize
├─ DevOps: docker-manager, deploy-helper
└─ Productivity: calendar, email-integration

💡 Install Suggestion
clawhub install china-summarizer research-orchestrator skill-advisor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4: Compare Skills (When User Asks)

When user wants to compare skills:

```bash
# Get details for each skill
clawhub inspect skill-a
clawhub inspect skill-b

# Compare and recommend
```

### Comparison Report

```
━━━ 📊 Skill对比: skill-a vs skill-b ━━━━━━━━━━━━━━━━━

| 维度 | skill-a | skill-b |
|------|---------|---------|
| 下载量 | 1,000 | 5,000 |
| 更新时间 | 3天前 | 30天前 |
| 功能 | 基础搜索 | 高级分析 |
| 复杂度 | 简单 | 中等 |

🎯 推荐: skill-b（更活跃，功能更全）
```

---

## Key Differentiators

### 1. Context-Aware
- Analyzes what user already has
- Doesn't recommend duplicates
- Suggests complementary skills

### 2. Personalized
- Adapts to user's apparent role
- Developer vs Researcher vs Content Creator
- Different recommendations for each

### 3. Multi-Source Data
- Downloads & popularity
- Freshness & maintenance
- Community sentiment
- Dependency complexity

### 4. Actionable Output
- Ready-to-install commands
- Clear reasoning for each recommendation
- Prioritized list

---

## Smart Inference Engine

### Hybrid Approach: Rules + LLM Analysis

**Layer 1: Rule-Based (Fast)**
```python
# Quick filtering using keyword matching
PAIR_RULES = [
    {"source": ["ocr", "document", "pdf"], "target": ["summarize", "translate"]},
    {"source": ["tts", "voice", "speech"], "target": ["video", "image"]},
    {"source": ["search", "research"], "target": ["summarize", "report"]},
]
```

**Layer 2: Semantic Analysis (Agent-Assisted)**

The agent can enhance recommendations using its own reasoning:

```
Agent analyzes:
1. Skill descriptions for semantic relationships
2. Functional dependencies between skills
3. User's apparent use case
4. Complementary workflow patterns
```

### How It Works

```
User: "推荐skills给我"
        ↓
Step 1: Get installed skills (clawhub list)
        ↓
Step 2: Fetch candidate skills from ClawHub API
        ↓
Step 3: Rule-based filtering (fast, removes obvious non-matches)
        ↓
Step 4: Agent semantic analysis (understands context)
        ↓
Step 5: Generate personalized recommendations
```

### Semantic Understanding

| Scenario | Rule-Based | Agent-Assisted |
|----------|------------|----------------|
| china-doc-ocr + china-summarizer | ✅ Detected | ✅ Detected |
| skill-studio + research-orchestrator | ❌ Missed | ✅ Detected (both help create) |
| china-tts + china-video-gen | ✅ Detected | ✅ Detected |
| skill-advisor + any skill | ❌ Missed | ✅ Detected (advises before install) |

**The agent provides semantic understanding beyond keyword matching.**

---

## Multi-Language Support

Output language automatically matches user's conversation language:
- User writes in Chinese → Output Chinese report
- User writes in English → Output English report
- User specifies "用英文输出" / "Output in Japanese" → Output in specified language

Supported: Chinese, English, Japanese, Korean, and 50+ languages

---

## Error Handling

```
No skills installed     → "Let's start with basics: install X, Y, Z"
ClawHub API error       → "Using cached recommendations..."
Parse error             → "Showing best-effort results"
```

---

## Notes

- Recommendations update based on real-time ClawHub data
- Complementary relationships inferred dynamically from skill descriptions
- Multi-dimensional classification for accurate categorization
- Privacy: Only reads installed skill names and public metadata
- No access to config files, tokens, or sensitive data
- Supports 50+ languages for output

---

## Limitations (Honest)

- **Inference accuracy**: Depends on quality of skill descriptions on ClawHub
- **New skills**: May not have enough metadata for accurate classification
- **Edge cases**: Some skills don't fit neatly into categories
- **API dependency**: Requires ClawHub API for real-time data
