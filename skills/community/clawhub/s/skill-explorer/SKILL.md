# skill-explorer

A systematic framework for discovering, evaluating, and comparing OpenClaw skills. Use when you need to find the right skill for a specific task, compare multiple options, or assess skill quality and safety.

## Overview

This skill provides a battle-tested workflow for skill exploration:
1. **Demand Analysis** → Clarify what you need
2. **Search & Discovery** → Find relevant skills
3. **Information Gathering** → Collect metrics and details
4. **Lateral Exploration** → Find alternatives and competitors
5. **Deep Dive** → Download and inspect skill files
6. **Safety Assessment** → Security review
7. **Synthesis & Report** → Output comparison and recommendations
8. **Decision Support** → Present options for user approval

---

## When to Use This Skill

Use skill-explorer when:
- You need to find a skill for a specific task
- You want to compare multiple similar skills
- You need to evaluate skill quality before installation
- You're doing security review of a skill
- You want to discover related or complementary skills

---

## The Exploration Workflow

### Phase 1: Demand Analysis

**Clarify the requirements:**
```
What task does the user need to accomplish?
What are the must-have vs nice-to-have features?
Any constraints (budget, platform, language)?
What's the priority: functionality, popularity, or safety?
```

**Document the search criteria:**
- Primary keywords
- Secondary/alternative terms
- Platform constraints (e.g., "must work with Chinese market")
- Safety requirements (e.g., "no network access")

---

### Phase 2: Search & Discovery

**Primary search:**
```bash
clawhub search <primary-keyword>
clawhub search <related-term-1> <related-term-2>
```

**Capture initial results:**
Record top 5-10 results with:
- Skill name
- Relevance score
- First impression of summary

---

### Phase 3: Information Gathering

**For each promising skill, collect:**

```bash
clawhub inspect <skill-name> --json
```

**Extract key metrics:**
| Metric | Why It Matters |
|--------|---------------|
| `stats.stars` | Community quality indicator |
| `stats.downloads` | Popularity/visibility |
| `stats.installsAllTime` | Actual adoption |
| `stats.installsCurrent` | Active usage (low churn = good) |
| `stats.versions` | Maintenance activity |
| `owner.handle` | Developer reputation |
| `updatedAt` | Freshness |

**Read SKILL.md:**
- Core functionality
- Use cases
- Prerequisites
- Integration requirements

---

### Phase 4: Lateral Exploration

**Find alternatives and complements:**

```bash
# Search with related keywords
clawhub search <alternative-keyword-1>
clawhub search <alternative-keyword-2>

# Look for broader/narrower skills
clawhub search <broader-category>
clawhub search <specific-subtask>
```

**Expand the candidate pool:**
- Direct competitors (same function)
- Partial overlaps (related function)
- Complementary skills (work together)
- Domain-specific variants (e.g., "CN" versions)

---

### Phase 5: Deep Dive

**Download and inspect promising skills:**

```bash
# Install to temp directory for inspection
cd /tmp && mkdir skill-check
cd skill-check && clawhub install <skill-name>
```

**File structure analysis:**
```bash
find . -type f | sort
```

**Look for:**
- `SKILL.md` - Main documentation
- `scripts/` - Executable code
- `package.json` / `requirements.txt` - Dependencies
- `_meta.json` - Metadata
- Hidden files or unusual structures

---

### Phase 6: Safety Assessment

**Static code analysis:**

```bash
# Check for suspicious patterns
grep -r -E "(eval\(|exec\(|Function\(|atob\(|btoa\()" .
grep -r -E "(crypto|encrypt|decrypt|base64|0x[0-9a-f]{20,})" .

# Check for network/API calls
grep -r -E "(https?://|api\.|token|key|secret|password)" .

# Check for file system operations
grep -r -E "(fs\.|writeFile|readFile|unlink|chmod)" .
```

**Risk classification:**
| Level | Indicators |
|-------|-----------|
| 🟢 Low | Pure documentation, no scripts, no network |
| 🟡 Medium | Scripts but official APIs only, read-only ops |
| 🔴 High | Obfuscated code, unknown network endpoints, write operations |

**Special checks:**
- [ ] VirusTotal warnings (verify if false positive)
- [ ] Hardcoded credentials or tokens
- [ ] External dependencies (npm/pip packages)
- [ ] Permission requirements (camera, microphone, etc.)

---

### Phase 7: Synthesis & Report

**Create comparison table:**

```markdown
| Skill | Stars | Installs | Safety | Best For |
|-------|-------|----------|--------|----------|
| skill-a | ⭐⭐ 25 | 45 | 🟢 | General use |
| skill-b | ⭐ 8 | 12 | 🟢 | Specific niche |
| skill-c | ⭐⭐⭐ 60 | 120 | 🟡 | Power users |
```

**Write detailed analysis:**
1. **Executive Summary** - Top 2-3 recommendations
2. **Detailed Comparison** - Feature-by-feature analysis
3. **Safety Assessment** - Security findings
4. **Use Case Mapping** - Which skill fits which scenario
5. **Installation Guide** - Prerequisites and steps

---

### Phase 8: Decision Support

**Present clear options:**

```
## Recommendation

### Option A: Best Overall → [skill-name]
- Why: Highest quality + safety
- Trade-off: May lack advanced features

### Option B: Most Popular → [skill-name]
- Why: Community validated
- Trade-off: Higher complexity

### Option C: Specific Need → [skill-name]
- Why: Perfect fit for [specific use case]
- Trade-off: Less generalizable
```

**Get user approval:**
- Present options with trade-offs
- Ask for priority (functionality vs safety vs popularity)
- Wait for explicit approval before installation
- Document approved skills for installation queue

---

## Best Practices

### Do's
- ✅ Always check multiple similar skills (don't settle for first result)
- ✅ Download and inspect before recommending installation
- ✅ Document security findings clearly
- ✅ Consider the user's specific context (language, platform, expertise)
- ✅ Update EVOLUTION.md after installation

### Don'ts
- ❌ Don't recommend based on downloads alone
- ❌ Don't skip security checks even for popular skills
- ❌ Don't install without explicit user approval
- ❌ Don't ignore VirusTotal warnings without investigation
- ❌ Don't overlook maintenance status (old updates = risk)

---

## Integration with Evolution System

After completing an exploration:

1. **Update EVOLUTION.md:**
   - Add discovered skills to "待学习" list
   - Note priority and context
   - Link to exploration report

2. **Create exploration report:**
   - Save to `reports/skill-exploration-{topic}.md`
   - Include all findings and recommendations
   - Reference in future decisions

3. **Track decisions:**
   - Document which skills were approved/declined
   - Note reasons for future reference
   - Update after installation and usage

---

## Example Output Template

```markdown
# Skill Exploration Report: [Topic]

## Executive Summary
Recommended: [skill-name] (⭐⭐ 50 stars, 80 installs, 🟢 safe)

## Skills Discovered

### Tier 1: Strong Candidates
| Skill | Stars | Installs | Safety | Verdict |
|-------|-------|----------|--------|---------|
| ... | ... | ... | ... | ... |

### Tier 2: Alternatives
...

## Detailed Analysis

### [skill-name]
**Overview:** ...
**Strengths:** ...
**Weaknesses:** ...
**Safety Review:** ...
**Best For:** ...

## Recommendations

1. **Install:** [skill] - [reason]
2. **Consider:** [skill] - [reason]
3. **Skip:** [skill] - [reason]

## Next Steps
- [ ] User approval for recommended skills
- [ ] Security review for approved skills
- [ ] Installation and testing
- [ ] Update EVOLUTION.md
```

---

## Related Skills

- **marketing-mode** - For go-to-market strategy after skill selection
- **tweet-writer** - For promoting discovered skills
- **skill-creator** - For creating your own skills based on gaps found

---

*This skill helps you make informed decisions about skill adoption, ensuring you find the right tool for the job while maintaining security standards.*
