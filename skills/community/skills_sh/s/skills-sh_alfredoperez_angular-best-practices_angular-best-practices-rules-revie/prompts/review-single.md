# Single Rule Review Prompt

Review this rule file for usefulness to AI agents, validity, accuracy, and format.

## Review Checklist

### 1. Usefulness (Would AI need this?)

| Criteria | ❌ Remove | ⚠️ Improve | ✅ Keep |
|----------|-----------|------------|---------|
| Would AI make this mistake? | AI already knows | Sometimes | AI commonly does this wrong |
| Is this AI-discoverable? | Easy to find in docs | Docs are scattered | Tribal knowledge |
| Is guidance specific enough? | Too vague | Missing thresholds | Clear criteria |
| Does it prevent real bugs? | Style only | Minor issues | Bugs/memory leaks/perf |

### 2. Validity (Is this real?)

| Check | Action |
|-------|--------|
| Search Angular docs | WebSearch "angular.dev {topic}" |
| Community consensus | WebSearch "{pattern} angular best practice" |
| Not contradicting docs | Compare with official guidance |

### 3. Accuracy (Is code correct?)

| Check | Criteria |
|-------|----------|
| Angular version | Works with Angular 17+ |
| No deprecated APIs | No ViewChild static, no ngModules for standalone |
| Compiles | Syntax is valid TypeScript/Angular |

### 4. Format

| Check | Criteria |
|-------|----------|
| File length | Max 50 lines (ideal: 30-40) |
| Description | Single sentence |
| Code blocks | 1-2 blocks max |
| Lines per block | Max 10 lines |

## Output Format

```markdown
## Rule Review: {filename}

### Usefulness Assessment

| Criteria | Rating | Notes |
|----------|--------|-------|
| Would AI make this mistake? | ✅/⚠️/❌ | [explanation] |
| Is this AI-discoverable? | ✅/⚠️/❌ | [explanation] |
| Is guidance specific enough? | ✅/⚠️/❌ | [explanation] |
| Does it prevent real bugs? | ✅/⚠️/❌ | [explanation] |

**Usefulness Score:** X/4

### Validity: ✅ | ⚠️ | ❌
**Evidence:** [links to Angular docs or community sources]

### Accuracy: ✅ | ⚠️ | ❌
**Angular Version:** 17+
**Code Issues:** [any problems]

### Format: ✅ | ⚠️ | ❌
**Lines:** X/50
**Code Blocks:** X

### Verdict: ✅ KEEP | ⚠️ IMPROVE | ❌ REMOVE
**Recommendation:** [specific action or removal reason]
```
