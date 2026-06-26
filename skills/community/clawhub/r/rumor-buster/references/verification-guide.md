# Verification Workflow Guide

This document describes the complete verification workflow for Rumor Buster.

Load this file when implementing or modifying the verification logic.

---

## Overview

Rumor Buster performs **dual-engine verification**:
1. Chinese aggregated search
2. English deep search
3. Cross-verification analysis
4. Source tracing
5. Credibility scoring

---

## Phase 1: Chinese Aggregated Search

### Purpose
Gather information from Chinese-language sources to establish:
- First known appearance of the claim
- How it spread in Chinese media/social networks
- Official responses (if any)

### Search Strategy

```python
def search_chinese(query, config):
    """
    Perform Chinese aggregated search
    
    Args:
        query: User's verification query
        config: Loaded search engine configuration
    
    Returns:
        Aggregated results from all available Chinese engines
    """
    results = []
    
    # 1. kimi_search (if available)
    if config["native"].get("kimi_search", {}).get("available"):
        results.append(kimi_search(query, limit=10, include_content=True))
    
    # 2. multi-search-engine Chinese engines
    if config["multi_search_engine"].get("available"):
        for engine in config["multi_search_engine"].get("chinese", []):
            results.append(search_with_engine(engine, query))
    
    # 3. web_search as fallback
    if config["native"].get("web_search", {}).get("available"):
        results.append(web_search(query + " site:zh", count=10))
    
    return aggregate_results(results)
```

### Source Tracing (Chinese)

For each unique claim found:
1. Identify earliest publication date
2. Trace back to original source
3. Document spread path:
   ```
   Original Source → Major Media → Social Media → User
   ```

### Key Information to Extract

- **Origin**: First known publisher
- **Date**: First publication timestamp
- **Authority**: Is the source authoritative?
- **Evidence**: What evidence supports the claim?
- **Counter-evidence**: Any debunking or contradictory reports?

---

## Phase 2: English Deep Search

### Purpose
Gather international perspective and verify against:
- International news agencies
- Official government statements
- Academic/think tank analysis
- Fact-checking organizations

### Search Strategy

```python
def search_english(query, config):
    """
    Perform English deep search
    
    Args:
        query: User's verification query (translated if needed)
        config: Loaded search engine configuration
    
    Returns:
        Aggregated results from all available English engines
    """
    results = []
    
    # 1. Tavily (if configured) - AI-enhanced search
    if config["tavily"].get("available"):
        results.append(tavily_search(
            query, 
            api_key=config["tavily"]["api_key"],
            max_results=10,
            search_depth="comprehensive"
        ))
    
    # 2. multi-search-engine English engines
    if config["multi_search_engine"].get("available"):
        for engine in config["multi_search_engine"].get("english", []):
            results.append(search_with_engine(engine, query))
    
    # 3. web_search as fallback
    if config["native"].get("web_search", {}).get("available"):
        results.append(web_search(query, count=10))
    
    return aggregate_results(results)
```

### Source Tracing (English)

1. Identify international first reports
2. Check for fact-checks:
   - Snopes
   - FactCheck.org
   - Reuters Fact Check
   - AFP Fact Check
3. Document official statements
4. Note consensus or disagreement

---

## Phase 3: Cross-Verification Analysis

### Comparison Matrix

Compare Chinese and English findings across dimensions:

| Dimension | Chinese Finding | English Finding | Match? |
|:---|:---|:---|:---:|
| **Event Occurred** | Yes/No/Unclear | Yes/No/Unclear | ✅/❌ |
| **Key Details** | Detail A | Detail B | ✅/❌ |
| **Official Stance** | Stance X | Stance Y | ✅/❌ |
| **Timeline** | Time T1 | Time T2 | ✅/❌ |

### Consistency Scoring

```python
def calculate_consistency(cn_results, en_results):
    """
    Calculate cross-language consistency score
    
    Returns score 0-100 and detailed analysis
    """
    factors = {
        "basic_facts_match": 30,  # Core facts agree
        "details_align": 25,      # Specifics match
        "timeline_consistent": 20, # Dates/times align
        "authorities_agree": 25   # Official sources agree
    }
    
    score = 0
    analysis = []
    
    for factor, weight in factors.items():
        if check_factor(cn_results, en_results, factor):
            score += weight
            analysis.append(f"✅ {factor}")
        else:
            analysis.append(f"❌ {factor}")
    
    return score, analysis
```

---

## Phase 4: Source Tracing

### Complete Timeline Reconstruction

```
[Time T-3] Original event occurs (if applicable)
    ↓
[Time T-2] First report (identify earliest source)
    ↓
[Time T-1] Early spread (who picked it up first?)
    ↓
[Time T-0] Reaches mainstream/social media
    ↓
[Time T+1] Fact-checks/debunking (if applicable)
    ↓
[Time T+2] Current status
```

### Spread Path Mapping

Visualize how information traveled:
```
Original Source (e.g., Iranian state media)
    ↓
Regional Media (e.g., Mehr News Agency)
    ↓
International Media (e.g., Reuters, AP)
    ↓
Chinese Media (e.g., 观察者网)
    ↓
Social Media (e.g., WeChat, Weibo)
    ↓
User's Source (where they encountered it)
```

---

## Phase 5: Credibility Scoring

### Multi-Factor Scoring

Final score combines:

```python
def calculate_credibility(analysis):
    """
    Calculate overall credibility score
    
    Returns: Score (0-100) and verdict category
    """
    weights = {
        "source_reliability": 25,    # How reliable are the sources?
        "cross_confirmation": 25,     # Do multiple sources agree?
        "evidence_quality": 20,       # Quality of supporting evidence
        "authority_acknowledgment": 20, # Official/authoritative confirmation
        "consistency": 10             # Internal consistency of claim
    }
    
    score = sum(
        analysis[factor] * weight 
        for factor, weight in weights.items()
    )
    
    verdict = categorize_score(score)
    
    return score, verdict
```

### Score Categories

| Score | Category | Action |
|:---:|:---|:---|
| 90-100 | Verified | High confidence, can rely on |
| 70-89 | Likely True | Generally reliable, minor caveats |
| 50-69 | Unverified | Insufficient evidence, wait for more |
| 30-49 | Misleading | Partially true but problematic |
| 10-29 | Likely False | Probably false, significant issues |
| 0-9 | False | Debunked, do not share |

---

## Session State Management

### Critical: Maintain Current Topic

```python
# Session-level state
current_verification = {
    "query": None,
    "timestamp": None,
    "cn_results": None,
    "en_results": None,
    "analysis": None,
    "language": None  # "zh" or "en"
}

def verify(query):
    """Main verification entry point"""
    # Update current verification
    current_verification["query"] = query
    current_verification["timestamp"] = datetime.now()
    current_verification["language"] = detect_language(query)
    
    # Perform verification
    results = perform_verification(query)
    current_verification.update(results)
    
    return generate_summary(current_verification)

def detailed_report():
    """Generate detailed report for current verification"""
    if not current_verification["query"]:
        return "请先进行验证请求"
    
    return generate_detailed_report(current_verification)
```

### Why This Matters

Users may verify multiple messages in one session:
```
User: /verify "Message A"
System: [Summary for A]
        💡 Reply "detailed report" for [Message A]...

User: /verify "Message B"
System: [Summary for B]
        💡 Reply "detailed report" for [Message B]...

User: detailed report  ← Must return B, not A!
```

---

## Language Detection

### Automatic Language Switching

```python
def detect_language(text):
    """
    Detect language of user input
    
    Returns: "zh" for Chinese, "en" for English
    """
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return "zh"
    return "en"
```

### Multi-Language Support

All output should respect `current_verification["language"]`:
- Summary report language
- Detailed report language
- Interactive prompts language

---

## Error Handling

### Search Engine Failures

If an engine fails:
1. Log the error
2. Continue with other engines
3. Note the limitation in output

```python
def safe_search(search_func, query, fallback_msg):
    try:
        return search_func(query)
    except Exception as e:
        logger.warning(f"Search failed: {e}")
        return {"error": str(e), "fallback": fallback_msg}
```

### Rate Limiting

Respect API quotas:
- Tavily: 1000 queries/month (free tier)
- web_search: Check provider limits
- Implement backoff on 429 errors

---

## Best Practices

1. **Always cross-verify**: Never rely on single source
2. **Check dates**: Old news often resurfaces as "new"
3. **Trace to origin**: Don't stop at aggregator sites
4. **Note limitations**: Be transparent about search scope
5. **Update session state**: Always track current verification topic
6. **Respect rate limits**: Don't overwhelm APIs
