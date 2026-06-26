---
name: WheelSpotter
version: 1.0.0
description: A wheel-spotting scout that finds reusable solutions before you build from scratch. Cost-controlled intelligent search with complexity-aware filtering, intent-based platform selection, and form consistency checks.
author: YourName
license: MIT
dependency:
  python:
    - requests>=2.31.0
    - pydantic>=2.0.0
triggers:
  - "is there an existing"
  - "looking for library"
  - "any existing solution"
  - "before implementing"
  - "avoid reinventing"
  - "is there a library for"
  - "find a tool that"
  - "need a package for"
  - "spot a wheel"
  - "find wheels"
---

# WheelSpotter (v1.0)

> 🎯 **WheelSpotter** — Your wheel-spotting scout. Spots reusable solutions before you build from scratch.

**Core principle**: Solutions must be directly integrable—not flashy but unusable toys.

---

## When to Use

### ✅ Trigger Scenarios

Load this skill when the user expresses these intents:

| Pattern | Example |
|---------|---------|
| Looking for existing solutions | "Is there an existing PDF parsing library?" |
| Avoiding duplicate work | "I don't want to reinvent the wheel..." |
| Tech stack consultation | "What's a good Python data visualization library?" |
| Quick integration needs | "I need an OCR API I can use right away" |
| Pre-implementation research | "Implementing JWT auth—any existing solutions?" |
| Wheel spotting | "Spot any wheels for image processing?" |

**Keyword matches**: `is there`, `existing`, `wheel`, `library`, `framework`, `API`, `tool`, `solution`, `spot`

### ❌ Do NOT Trigger

| Scenario | Reason | Suggestion |
|----------|--------|------------|
| User wants to build themselves | "I want to write my own..." | Assist with coding directly |
| Highly customized requirements | "I need something that does X, Y, Z all at once..." | Suggest breaking down and searching separately |
| Learning purposes | "I want to learn how to implement..." | Provide tutorials instead |
| Tech stack already decided | "I'm using React to build..." | Move to development guidance |

---

## Design Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Problem-Oriented** | Precisely solve "finding integrable wheels" | Sources classified by output form, exclude chatbots |
| **Closed-Loop Delivery** | Clear "usable/unusable" conclusion with action | Results include `pip install` commands or self-build recommendation |
| **High Adaptability** | Dynamic strategy based on complexity and intent | Complexity grading + intent-adaptive source selection |
| **Progressive Improvement** | System gets smarter with each use | Feedback loops, result caching, vector memory |
| **Transferable Leverage** | Core capabilities reusable elsewhere | Funnel engine, cost monitor as independent modules |
| **Cost Red Line** | Search cost must be lower than self-build cost | Budget caps, tiered abandonment, early termination |

---

## Prerequisites

```bash
pip install -r requirements.txt
```

**Environment**:
- Python 3.8+
- Internet access for API calls
- GitHub Token (optional, increases API limit to 5000 req/hour)

---

## Input/Output Specification

### Input Format

```python
# Method 1: Natural language (parsed by agent)
user_input = "I need a Python library to process Excel files"

# Method 2: Structured input (optional)
{
    "requirement": "process Excel files",
    "tech_stack": ["Python"],
    "intent": "library",
    "constraints": {
        "license": "MIT",
        "min_stars": 100,
        "last_updated": "12m"
    }
}
```

### Output Format

```json
{
    "status": "found",
    "recommendations": [
        {
            "name": "openpyxl",
            "source": "pypi",
            "url": "https://openpyxl.readthedocs.io/",
            "match_score": 0.92,
            "integration_score": 0.95,
            "action": "pip install openpyxl",
            "license": "MIT",
            "stars": 1200,
            "last_updated": "2 months ago",
            "warnings": [],
            "advice": "Recommended, mature and stable"
        }
    ],
    "fallback": null,
    "cost": {
        "tokens_used": 420,
        "time_seconds": 3.2,
        "estimated_time_saved": "~4 hours"
    }
}
```

**Status values**:
- `found`: Suitable solutions found
- `not_found`: Recommend self-build
- `needs_clarification`: Requirement unclear, need follow-up
- `error`: Search failed, return error info

---

## Core Workflow

```
User Input
  ↓
[M0] Complexity Grading (~30 tokens)
  ↓
[M1] Intent Classification (~60 tokens)
  ↓
[Optional] Clarification (1-2 rounds if needed)
  ↓
[M2] Extract Keywords + Tech Entities (~150 tokens)
  ↓
[Search] Activate platforms by intent, parallel API calls
  ↓
[Hard Filter] Deprecated/activity/form matching
  ↓
[LLM Refinement] Multi-dimensional eval for ≤5 candidates (~300 tokens)
  ↓
Output recommendations + action commands + cost report
```

---

## Implementation Details

### Step 1: Complexity Grading (M0)

**Prompt Template**:
```
You are a development complexity assessment expert. Evaluate the requirement:
- L1: Simple function/tool, solvable with dozens of lines
- L2: Medium module, requires interface design
- L3: Complex system, involves multiple components

Requirement: {requirement}
Output JSON only: { "complexity": "L2", "reason": "..." }
```

**Impact on Search Strategy**:

| Complexity | Token Cap | Time Cap | Sources | Star Threshold |
|------------|-----------|----------|---------|----------------|
| L1 Simple | 300 | 8s | 2-3 | ≥10 |
| L2 Medium | 600 | 12s | 3-5 | ≥50 |
| L3 Complex | 800 | 15s | Full | ≥100 |

### Step 2: Intent Classification (M1)

**Prompt Template**:
```
Analyze the requirement, determine desired output form (multiple allowed):
- library: Library/framework integrable into code
- service: Callable external API/service
- tool: Standalone executable tool/CLI
- reference: Code template/example/architecture reference
- assistant: Conversational assistant (usually not a wheel, use cautiously)

Requirement: {requirement}
Output JSON only: { "intent": [...], "reason": "..." }
```

**Important**: If intent only contains `assistant`, return guidance without triggering search.

### Step 3: Platform Selection Matrix

| Intent | Activate Sources | Do NOT Search |
|--------|------------------|---------------|
| library | GitHub, npm, PyPI, Maven, Crates.io | Conversational skill marketplaces |
| service | MCP Hubs, HuggingFace API, RapidAPI | Pure code repos |
| tool | GitHub Releases, Docker Hub, npm -g | Pure library platforms |
| reference | Stack Overflow, GitHub Gist, Official docs | Distribution platforms |

### Step 4: Hard Filtering Rules

```python
def hard_filter(candidate, complexity, intent):
    """Adaptive hard filtering"""
    
    # 1. Archived/Deprecated check
    if candidate.archived or candidate.deprecated:
        return False, "Archived or deprecated"
    
    # 2. Dynamic star threshold
    thresholds = {"L1": 10, "L2": 50, "L3": 100}
    if candidate.stars < thresholds[complexity]:
        return False, f"Insufficient stars ({candidate.stars} < {thresholds[complexity]})"
    
    # 3. Update time check
    if months_since_update > 24:
        return False, "Not updated in 24+ months"
    
    # 4. Form consistency check
    if intent == "library" and not has_package_indicator(candidate):
        return False, "Form mismatch: no library indicators"
    
    return True, "Passed"
```

### Step 5: LLM Refinement

**Multi-dimensional Scoring**:
```
Final Score = Semantic Similarity × 0.5 
            + Integration Feasibility × 0.3 
            + Activity Normalization × 0.2
```

**Refinement Prompt**:
```
You are a technical solution evaluator. Assess this candidate:

Requirement: {requirement}
Candidate: {candidate}

Evaluation dimensions:
1. Semantic match (0-1): Does it truly solve the need?
2. Integration feasibility (0-1): Can user try within 1 hour?
3. Activity score (0-1): Based on stars, update frequency
4. License compatibility: Common open source license?
5. Known issues: Major bugs or security vulnerabilities?

Output JSON:
{
    "semantic_score": 0.9,
    "integration_score": 0.85,
    "activity_score": 0.7,
    "final_score": 0.83,
    "license_ok": true,
    "warnings": [],
    "advice": "Recommended, but note..."
}
```

---

## Search Script

See [scripts/search.py](scripts/search.py) for the standalone implementation.

**Usage**:
```bash
# Basic usage
python scripts/search.py --query "python pdf parser" --complexity L2 --intent library

# Multiple platforms
python scripts/search.py -q "python excel read write" -c L2 -i library -p github,pypi

# With GitHub token (recommended)
python scripts/search.py -q "react charting library" -c L3 --token $GITHUB_TOKEN
```

**Parameters**:
| Parameter | Short | Description | Default |
|-----------|-------|-------------|---------|
| `--query` | `-q` | Search keywords (required) | - |
| `--complexity` | `-c` | L1/L2/L3 | L2 |
| `--intent` | `-i` | library/service/tool/reference | library |
| `--platforms` | `-p` | Comma-separated platforms | github |
| `--limit` | `-l` | Max results per platform | 20 |
| `--token` | `-t` | GitHub token (optional) | - |
| `--output` | `-o` | Output file (optional) | stdout |

---

## Error Handling

| Error Condition | Strategy | User Message |
|-----------------|----------|--------------|
| GitHub API rate limit (403) | Fallback to web search or prompt for token | "GitHub API limit reached. Please retry later or configure a GitHub token." |
| Network timeout (>10s) | Retry once, return partial results on failure | "Some platforms timed out. Returning available results." |
| No matching intent | Don't trigger search, guide user to clarify | "Your requirement may need custom development. Continue searching?" |
| JSON parse failure | Log error, return raw response | "Failed to parse search results. Please check raw data." |
| All platforms failed | Return graceful degradation | "Search service temporarily unavailable. Please retry later or research manually." |

---

## Cost Control

### Three-Tier Budget System

| Level | Token Cap | Time Cap | Strategy |
|-------|-----------|----------|----------|
| L1 Simple | 300 | 8s | Quick abandonment, recommend self-build if not found |
| L2 Medium | 600 | 12s | Moderate resources |
| L3 Complex | 800 | 15s | Full resources by intent matrix |

### Early Termination Conditions

- Hard filter yields 0 candidates → Immediately output "not found, recommend self-build"
- Intent is only `assistant` → Don't trigger search
- High-match result found (score > 0.9) → Early termination

### Graceful Degradation

```
⚠️ Search cost approaching or exceeding self-build cost (estimated self-build: X hours).

Found partial matches:
- [Project Name] (match score: 0.65)

Suggestion: Try the above first. If requirements not met, direct implementation may be faster.
```

---

## Usage Examples

### Example 1: Library Search (L2)

**Input**:
```
I need a Python library to read and write Excel files
```

**Agent Analysis**:
- Complexity: L2 (medium module)
- Intent: library
- Keywords: python, excel, read, write

**Script Call**:
```bash
python scripts/search.py -q "python excel read write" -c L2 -i library -p github,pypi
```

**Output**:
```json
{
  "status": "found",
  "recommendations": [
    {
      "name": "openpyxl/openpyxl",
      "action": "pip install openpyxl",
      "match_score": 0.92,
      "advice": "Recommended, comprehensive features"
    },
    {
      "name": "pandas-dev/pandas",
      "action": "pip install pandas",
      "match_score": 0.88,
      "advice": "Use pandas for data analysis needs"
    }
  ]
}
```

### Example 2: Simple Requirement (L1 - Quick Abandonment)

**Input**:
```
I need to validate email format
```

**Agent Judgment**:
- Complexity: L1 (~10 lines of regex)
- Recommendation: Direct implementation is faster than searching

**Output**:
```json
{
  "status": "not_found",
  "message": "This is an L1 simple requirement. Recommend direct implementation.",
  "code_snippet": "import re\nre.match(r'^[\\w.-]+@[\\w.-]+\\.\\w+$', email)"
}
```

### Example 3: Service Discovery (L3)

**Input**:
```
I need an OCR service that can batch process PDFs via API, supporting Chinese and English
```

**Agent Analysis**:
- Complexity: L3 (complex system)
- Intent: service
- Keywords: ocr, api, pdf, batch, chinese, english

**Output**:
```json
{
  "status": "found",
  "recommendations": [
    {
      "name": "Tesseract OCR",
      "type": "library + CLI",
      "action": "pip install pytesseract or docker run tesseract",
      "match_score": 0.85,
      "warnings": ["Requires self-hosting"]
    },
    {
      "name": "Google Cloud Vision API",
      "type": "cloud service",
      "action": "Apply for API key then call",
      "match_score": 0.90,
      "warnings": ["Paid service"]
    }
  ]
}
```

---

## Implementation Roadmap

| Phase | Features | Status | Value |
|-------|----------|--------|-------|
| **M1** | Complexity + Intent + Search + Hard Filter | ✅ Complete | Core functionality |
| **M2** | Multi-turn clarification + Quick/Deep mode | ⏳ Planned | Reduce ineffective searches |
| **M3** | Result caching + Adaptive thresholds | ⏳ Planned | Lower cost |
| **M4** | Security scanning (OSV API) | ⏳ Planned | Production safety |
| **M5** | Vector pre-filtering (bge-small) | ⏳ Planned | Improve precision |

**Recommendation**: M1 is production-ready. M2-M5 are optional enhancements.

---

## Limitations

| Limitation | Description | Mitigation |
|------------|-------------|------------|
| GitHub API limits | 60 req/hour unauthenticated | Configure GitHub token |
| PyPI search | Exact package names only | Combine with GitHub search |
| No vector pre-filter | Not implemented in current version | Planned for M5 |
| No vulnerability scan | OSV not integrated | Planned for M4 |

---

## Resource Index

| Resource | Location | Description |
|----------|----------|-------------|
| Search script | `scripts/search.py` | Standalone multi-platform search |
| Dependencies | `requirements.txt` | Python package requirements |
| License | `LICENSE` | MIT License |

---

## Best Practices

1. **Extract specific keywords** before calling the script
2. **Classify complexity and intent accurately** - determines search strategy
3. **Check license compatibility** before final recommendation
4. **Provide context** when requirements are ambiguous
5. **Respect early termination** - L1 requirements should self-build if not found

---

## Why WheelSpotter Works

WheelSpotter isn't a "comprehensive search engine" — it's your **wheel-spotting scout**:

- 🎯 **First determines if search is worthwhile** - Complexity grading
- 📍 **Then determines where to search most accurately** - Intent-driven platform selection
- 💰 **Gets decision evidence at lowest cost** - Budget control
- ✅ **Always provides next action** - Closed-loop delivery

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-28 | Renamed to WheelSpotter, added triggers, error handling, standalone script, I/O spec |
