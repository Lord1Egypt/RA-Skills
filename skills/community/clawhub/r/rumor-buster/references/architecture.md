# Architecture & Sub-Skill Integration

This document describes the technical architecture of Rumor Buster and how sub-skills are integrated.

Load this file when modifying architecture or sub-skill calling mechanisms.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Layer                            │
│  /verify "claim"    /验证 "消息"    detailed report          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Main Skill Layer                         │
│                   rumor-buster (SKILL.md)                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Check Configuration                                │  │
│  │    ├─ No config → Spawn setup sub-skill              │  │
│  │    └─ Has config → Load and proceed                  │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 2. Language Detection                                 │  │
│  │    └─ detect_language() → "zh" | "en"                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 3. Chinese Search                                     │  │
│  │    └─ search_chinese()                                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 4. English Search                                     │  │
│  │    └─ search_english()                                │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 5. Cross-Verification & Scoring                       │  │
│  │    └─ analyze_and_score()                             │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 6. Generate Output                                    │  │
│  │    ├─ Summary Report (default)                       │  │
│  │    └─ Detailed Report (on request)                   │  │
│  └───────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Sub-Skill Layer                           │
│              rumor-buster-setup (sub-skills/setup/)          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Setup Tasks:                                          │  │
│  │ 1. Detect search engines (native + multi + tavily)   │  │
│  │ 2. Interactive Tavily configuration (optional)       │  │
│  │ 3. Generate ~/.rumor-buster-config                   │  │
│  │ 4. Return to main skill                              │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration Management

### Config File Location

```
~/.rumor-buster-config
```

### Config Schema

```json
{
  "setup_completed": true,
  "setup_time": "2026-04-03T08:30:00Z",
  "version": "0.4.0",
  "search_engines": {
    "native": {
      "kimi_search": {
        "available": false,
        "type": "native"
      },
      "web_search": {
        "available": true,
        "type": "native",
        "provider": "brave"
      },
      "web_fetch": {
        "available": true,
        "type": "utility"
      }
    },
    "multi_search_engine": {
      "available": true,
      "chinese": ["sogou", "sogou_wechat", "toutiao"],
      "english": ["duckduckgo", "startpage"]
    },
    "tavily": {
      "available": true,
      "configured": true,
      "api_key": "tvly-xxxxx...",
      "quota": 1000
    }
  },
  "detection_log": {
    "last_detection": "2026-04-03T08:30:00Z",
    "detected_engines": ["web_search", "web_fetch", "sogou", "duckduckgo"]
  }
}
```

---

## Sub-Skill Integration

### Setup Sub-Skill Calling

**Main skill initiates setup via `sessions_spawn`:**

```python
def spawn_setup_subskill(task_description, language="zh"):
    """
    Spawn the setup sub-skill for configuration
    
    Args:
        task_description: Description of setup task
        language: User language ("zh" or "en")
    
    Returns:
        Sub-skill session handle
    """
    return sessions_spawn(
        task=task_description,
        agent_id="rumor-buster-setup",
        runtime="subagent",
        mode="session",
        label=f"rumor-buster-setup-{language}"
    )
```

### When to Spawn Setup

| Scenario | Trigger | Action |
|:---|:---|:---|
| First use | No config file exists | Spawn setup with init task |
| Reconfigure | User says "setup"/"reset" | Spawn setup with reconfig task |
| Corrupted config | Config parse error | Spawn setup with reset task |

### Setup Completion Detection

Main skill polls for config file creation:

```python
def wait_for_setup_completion(timeout=300):
    """
    Wait for setup sub-skill to complete
    
    Returns: True if config created, False if timeout
    """
    import time
    start = time.time()
    
    while time.time() - start < timeout:
        if os.path.exists(CONFIG_FILE):
            return True
        time.sleep(1)
    
    return False
```

---

## Session State Management

### Critical State Variables

```python
# Global session state for verification continuity
verification_state = {
    # Current verification topic
    "current_query": None,
    "current_language": None,
    "verification_timestamp": None,
    
    # Search results
    "chinese_results": None,
    "english_results": None,
    
    # Analysis
    "cross_verification": None,
    "credibility_score": None,
    "source_tracing": None
}
```

### State Update Flow

```
User: /verify "Claim A"
    ↓
[Update state with Claim A]
    ↓
[Perform searches]
    ↓
[Update state with results]
    ↓
Output: Summary for A

User: /verify "Claim B"
    ↓
[Update state with Claim B] ← Overwrites Claim A
    ↓
[Perform searches]
    ↓
[Update state with results]
    ↓
Output: Summary for B

User: detailed report
    ↓
[Read state → Claim B]
    ↓
Output: Detailed report for B ✓
```

### Why This Matters

Without proper state management:
```
User: /verify "Claim A"
User: /verify "Claim B"
User: detailed report
System: [Detailed report for A] ← WRONG! Should be B
```

---

## Language Handling

### Auto-Detection

```python
def detect_language(text):
    """
    Detect if text is primarily Chinese or English
    
    Returns: "zh" or "en"
    """
    import re
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    total_chars = len(text.strip())
    
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return "zh"
    return "en"
```

### Language Persistence

Once detected, language persists for the verification:

```python
def handle_verification(user_input):
    # Detect language from user input
    lang = detect_language(user_input)
    verification_state["current_language"] = lang
    
    # All subsequent output uses this language
    # until a new verification starts
```

---

## Search Engine Abstraction

### Unified Search Interface

```python
class SearchEngine:
    """Abstract base for search engines"""
    
    def search(self, query, **kwargs):
        raise NotImplementedError
    
    def is_available(self):
        raise NotImplementedError


class KimiSearch(SearchEngine):
    def search(self, query, limit=10):
        return kimi_search(query, limit=limit, include_content=True)
    
    def is_available(self):
        # Check config
        pass


class TavilySearch(SearchEngine):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def search(self, query, max_results=10):
        return tavily_search(query, api_key=self.api_key, max_results=max_results)
```

### Engine Selection Based on Config

```python
def get_available_engines(config):
    """
    Get list of available search engines based on config
    
    Returns: Dict of engine_name -> engine_instance
    """
    engines = {}
    
    # Native engines
    for name, info in config.get("native", {}).items():
        if info.get("available"):
            engines[name] = create_engine(name, info)
    
    # Multi-search-engine
    if config.get("multi_search_engine", {}).get("available"):
        for engine_name in config["multi_search_engine"].get("chinese", []):
            engines[f"multi:{engine_name}"] = MultiSearchEngine(engine_name)
        for engine_name in config["multi_search_engine"].get("english", []):
            engines[f"multi:{engine_name}"] = MultiSearchEngine(engine_name)
    
    # Tavily
    if config.get("tavily", {}).get("available"):
        engines["tavily"] = TavilySearch(config["tavily"]["api_key"])
    
    return engines
```

---

## Error Handling Strategy

### Graceful Degradation

If a search engine fails, continue with others:

```python
def search_with_fallback(query, engines):
    """
    Search with multiple engines, handling failures gracefully
    
    Returns: Aggregated results from successful engines
    """
    results = []
    failed_engines = []
    
    for name, engine in engines.items():
        try:
            result = engine.search(query)
            results.append(result)
        except Exception as e:
            failed_engines.append((name, str(e)))
            logger.warning(f"Engine {name} failed: {e}")
    
    if failed_engines:
        logger.info(f"Some engines failed: {failed_engines}")
    
    if not results:
        raise AllEnginesFailed("No search engines available")
    
    return aggregate_results(results), failed_engines
```

### User Notification

If engines fail, inform user but continue:

```markdown
⚠️ 注意：部分搜索引擎暂时不可用（kimi_search）。
使用可用引擎继续验证...

# 🔍 谣言终结者 - 验证概要
...
```

---

## Rate Limiting & Quotas

### Tavily Quota Tracking

```python
def check_tavily_quota(api_key):
    """
    Check remaining Tavily quota
    
    Returns: Number of remaining queries
    """
    # Tavily doesn't provide direct API for quota
    # Track usage locally or infer from error messages
    pass
```

### Usage Optimization

- Cache results for identical queries within session
- Prioritize free/cheap engines first
- Use Tavily only for complex queries

---

## Testing Architecture

### Mock Mode

For testing without hitting real APIs:

```python
MOCK_SEARCH_RESULTS = {
    "test query": {
        "chinese": [...],
        "english": [...]
    }
}

def search_mock(query, lang):
    return MOCK_SEARCH_RESULTS.get(query, {}).get(lang, [])
```

### Unit Testing

Test individual components:
- Language detection
- Credibility scoring
- Source tracing
- Config parsing

---

## Future Extensions

### Potential Additions

1. **Browser Integration**: Use `browser` tool for dynamic content
2. **Image Verification**: Reverse image search
3. **Video Verification**: Frame extraction and analysis
4. **Social Media APIs**: Direct Twitter/Weibo search
5. **LLM Summarization**: Use AI to summarize findings
6. **Database Storage**: Save verification history

### Extension Points

```python
# Plugin system for additional verifiers
verifiers = [
    TextVerifier(),
    ImageVerifier(),  # Future
    VideoVerifier(),  # Future
    SocialVerifier()  # Future
]
```
