---
name: rumor-buster
description: Dual-engine fact-checking skill for verifying news, claims, and messages through Chinese + English cross-verification and source tracing. Use when user wants to verify information authenticity, check if a message is true/false, validate news sources, or trace the origin of a claim. Supports /verify and /验证 commands with auto-detection of installed search engines.
version: 0.5.0
license: MIT
author: Harry
---

# Rumor Buster - 双引擎谣言终结者

**Dual-engine fact-checking with Chinese + English cross-verification and source tracing.**

## When to Use This Skill

Use Rumor Buster when the user wants to:
- Verify if a message/news/claim is true or false
- Check the credibility of information
- Trace the origin of a rumor
- Validate sources of news
- Cross-check claims across languages

**Trigger phrases**: 
- `/verify "claim"` or `/验证 "消息"`
- "Is this true?" / "这是真的吗？"
- "Check this" / "验证一下"
- "Rumor buster" / "谣言终结者"

---

## Quick Start

### First-Time Setup

When user first uses `/verify`, check for config:

```python
CONFIG_FILE = "~/.rumor-buster-config"

if not os.path.exists(CONFIG_FILE):
    # Spawn setup sub-skill
    return sessions_spawn(
        task="Initialize Rumor Buster: detect search engines, configure Tavily API (optional), generate config file",
        agent_id="rumor-buster-setup",
        runtime="subagent",
        mode="session"
    )
```

**Setup sub-skill handles**:
1. Detect native search tools (kimi_search, web_search, web_fetch)
2. Detect multi-search-engine availability
3. Configure Tavily API (optional)
4. Generate `~/.rumor-buster-config`

### Basic Usage

```python
def handle_verification(user_input):
    """Main entry point for verification requests"""
    # 1. Detect language
    lang = detect_language(user_input)
    
    # 2. Load config
    config = load_config(CONFIG_FILE)
    
    # 3. Extract query
    query = extract_query(user_input)
    
    # 4. Update session state (CRITICAL!)
    update_verification_state(query, lang)
    
    # 5. Perform verification
    results = perform_verification(query, config, lang)
    
    # 6. Generate summary
    return generate_summary(results, lang)
```

---

## Verification Workflow

### Phase 1: Chinese Search

Search Chinese sources for:
- First appearance of claim
- Spread path in Chinese media
- Official responses

```python
def search_chinese(query, config):
    results = []
    
    # kimi_search (if available)
    if config["native"].get("kimi_search", {}).get("available"):
        results.append(kimi_search(query, limit=10, include_content=True))
    
    # multi-search-engine Chinese engines
    if config["multi_search_engine"].get("available"):
        for engine in config["multi_search_engine"].get("chinese", []):
            results.append(search_with_engine(engine, query))
    
    return aggregate_results(results)
```

### Phase 2: English Search

Search English sources for:
- International perspective
- Fact-checking reports
- Official statements

```python
def search_english(query, config):
    results = []
    
    # Tavily (if configured)
    if config["tavily"].get("available"):
        results.append(tavily_search(
            query,
            api_key=config["tavily"]["api_key"],
            max_results=10
        ))
    
    # multi-search-engine English engines
    for engine in config["multi_search_engine"].get("english", []):
        results.append(search_with_engine(engine, query))
    
    return aggregate_results(results)
```

### Phase 3: Cross-Verification

Compare Chinese and English findings:

```python
def cross_verify(cn_results, en_results):
    comparison = {
        "facts_match": compare_facts(cn_results, en_results),
        "timeline_consistent": compare_timeline(cn_results, en_results),
        "authorities_agree": compare_authorities(cn_results, en_results),
        "consistency_score": calculate_consistency(cn_results, en_results)
    }
    return comparison
```

### Phase 4: Source Tracing

Trace claim back to origin:

```
Original Source → Early Spread → Mainstream Media → Social Media → User
```

### Phase 5: Credibility Scoring

Calculate 0-100% score based on:
- Source reliability (25%)
- Cross-confirmation (25%)
- Evidence quality (20%)
- Authority acknowledgment (20%)
- Consistency (10%)

---

## Session State Management (CRITICAL)

**Must maintain current verification topic:**

```python
verification_state = {
    "current_query": None,
    "current_language": None,
    "chinese_results": None,
    "english_results": None,
    "analysis": None
}

def update_verification_state(query, lang):
    """Update state when new verification starts"""
    verification_state["current_query"] = query
    verification_state["current_language"] = lang
    verification_state["timestamp"] = datetime.now()
    # Reset other fields
    verification_state["chinese_results"] = None
    verification_state["english_results"] = None
    verification_state["analysis"] = None
```

**Why this matters:**
```
User: /verify "Claim A"
System: [Summary for A]
User: /verify "Claim B"  
System: [Summary for B]
User: detailed report  ← MUST return B, not A!
```

Load `references/architecture.md` for complete state management details.

---

## Output Format

### Summary Report (Default)

```markdown
# 🔍 Rumor Buster - Verification Summary

**Claim**: "{query}"

## 📊 Credibility Score: {score}% - {verdict}

| Dimension | Result |
|:---|:---|
| **Source** | {source} |
| **Confirmation** | {confirmation} |
| **Evidence** | {evidence} |
| **Consistency** | {consistency} |

## 📝 One-Sentence Conclusion
{conclusion}

## 🔗 Information Source
- **Origin**: {origin}
- **Published**: {time}
- **Spread Path**: {path}

---
💡 Reply "detailed report" to view the complete verification process...
```

### Detailed Report

User replies "detailed report" → Output full analysis including:
- Complete search results from all engines
- Source timeline and spread path
- Cross-verification analysis table
- Detailed risk assessment

Load `references/output-templates.md` for complete templates.

---

## Language Support

### Auto-Detection

```python
def detect_language(text):
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return "zh"
    return "en"
```

### Bilingual Output

All output respects detected language:
- Summary report language
- Detailed report language
- Interactive prompts

---

## Reconfiguration

User can trigger reconfiguration:
- `setup` / `设置`
- `reset` / `重新设置`
- `/rumor-buster setup`

**Handler:**
```python
def handle_reconfig(user_input):
    lang = detect_language(user_input)
    return sessions_spawn(
        task=f"Reconfigure Rumor Buster (language: {lang})",
        agent_id="rumor-buster-setup",
        runtime="subagent",
        mode="session"
    )
```

---

## Reference Files

Load these files when implementing specific features:

| File | Content | When to Load |
|:---|:---|:---|
| `references/verification-guide.md` | Complete verification workflow | Implementing verification logic |
| `references/output-templates.md` | Output format templates | Formatting results |
| `references/architecture.md` | System architecture & sub-skill integration | Modifying architecture |

---

## Configuration Schema

```json
{
  "setup_completed": true,
  "version": "0.5.0",
  "search_engines": {
    "native": {
      "kimi_search": {"available": false},
      "web_search": {"available": true, "provider": "brave"},
      "web_fetch": {"available": true}
    },
    "multi_search_engine": {
      "available": true,
      "chinese": ["sogou", "toutiao"],
      "english": ["duckduckgo", "startpage"]
    },
    "tavily": {
      "available": true,
      "api_key": "tvly-xxxxx",
      "quota": 1000
    }
  }
}
```

---

## File Structure

```
rumor-buster/
├── SKILL.md                      # This file - core workflow
├── LICENSE                       # MIT license
├── scripts/
│   └── tavily_search.py         # Tavily search script
├── sub-skills/
│   └── setup/
│       ├── SKILL.md             # Setup sub-skill documentation
│       └── setup.py             # Setup implementation
└── references/                   # Detailed documentation
    ├── verification-guide.md    # Complete workflow
    ├── output-templates.md      # Output formats
    └── architecture.md          # System architecture
```

---

## Best Practices

1. **Always update session state** when starting new verification
2. **Cross-verify** - never rely on single source
3. **Check dates** - old news often resurfaces
4. **Trace to origin** - don't stop at aggregators
5. **Handle errors gracefully** - continue if one engine fails
6. **Respect rate limits** - especially Tavily (1000/month free)

---

*Rumor Buster - Cross-verify, trace sources, seek truth.*
