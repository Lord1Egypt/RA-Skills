---
name: self-evolution
description: "Autonomous self-improvement engine that learns from interactions, identifies patterns, and evolves behavior over time. Use when: (1) Analyzing interaction patterns for improvement, (2) Running periodic self-assessment, (3) Extracting reusable patterns from workflows, (4) Optimizing decision-making processes, (5) Integrating feedback into behavioral changes. Triggers on '自我进化', 'self-evolution', '自我改进', '学习模式', 'pattern analysis', 'optimize behavior'."
---

# Self-Evolution Engine

Autonomous learning and improvement system that continuously evolves agent behavior based on interaction patterns, feedback, and outcomes.

## Core Concepts

### Evolution Cycle

```
Experience → Pattern Detection → Learning → Validation → Integration
     ↑                                                        ↓
     └────────────────── Feedback Loop ←───────────────────────┘
```

### Key Components

| Component | Purpose | Frequency |
|-----------|---------|-----------|
| **Observer** | Capture interaction patterns | Continuous |
| **Analyzer** | Identify improvement opportunities | Daily |
| **Learner** | Extract actionable rules | On trigger |
| **Validator** | Test changes in isolation | Before integration |
| **Integrator** | Update behavioral files | After validation |

## Quick Start

```bash
# Analyze recent interactions
python3 {baseDir}/scripts/evolution.py --analyze --days 7

# Extract patterns from memory files
python3 {baseDir}/scripts/evolution.py --extract-patterns

# Run self-assessment
python3 {baseDir}/scripts/evolution.py --self-assess

# Generate evolution report
python3 {baseDir}/scripts/evolution.py --report --output evolution-report.md
```

## Evolution Data Flow

### 1. Experience Collection

Sources of experience data:
- `.learnings/` - Errors, corrections, feature requests
- `memory/YYYY-MM-DD.md` - Daily interaction logs
- `MEMORY.md` - Long-term memory updates
- Session transcripts - Actual conversation patterns
- Tool usage patterns - What works, what doesn't

### 2. Pattern Detection

Identify recurring patterns:

```bash
# Find repeated error patterns
python3 {baseDir}/scripts/evolution.py --pattern errors --threshold 3

# Find successful workflows
python3 {baseDir}/scripts/evolution.py --pattern successes --min-occurrences 5

# Find optimization opportunities
python3 {baseDir}/scripts/evolution.py --pattern inefficiencies
```

Pattern categories:
- **error_patterns** - Recurring failures
- **success_patterns** - Repeatable successes
- **inefficiency_patterns** - Wasted effort
- **preference_patterns** - User preferences
- **workflow_patterns** - Effective sequences

### 3. Learning Extraction

Transform patterns into actionable rules:

```bash
# Auto-extract learnings
python3 {baseDir}/scripts/evolution.py --learn --auto

# Interactive learning session
python3 {baseDir}/scripts/evolution.py --learn --interactive
```

Output: Candidate rules for behavioral files

### 4. Validation

Test proposed changes:

```bash
# Validate a proposed change
python3 {baseDir}/scripts/evolution.py --validate --rule "Always use git status before commit"

# Simulate behavior change
python3 {baseDir}/scripts/evolution.py --simulate --file SOUL.md --change "Be more concise"
```

### 5. Integration

Apply validated changes:

```bash
# Apply to behavioral files
python3 {baseDir}/scripts/evolution.py --integrate --target SOUL.md

# Update workflow rules
python3 {baseDir}/scripts/evolution.py --integrate --target AGENTS.md
```

## Behavioral Evolution Targets

### SOUL.md (Personality & Principles)

Evolution triggers:
- User feedback about tone/style
- Pattern of over-apologizing or being too verbose
- Consistently missing user intent
- Style preferences emerging over time

Example evolutions:
```markdown
# Before
"Be helpful and thorough"

# After (evolved)
"Be concise and direct. Skip disclaimers. Act, don't explain."
```

### AGENTS.md (Workflows & Rules)

Evolution triggers:
- Repeated mistakes in workflows
- More efficient sequences discovered
- New tool integrations
- Environment-specific optimizations

Example evolutions:
```markdown
# Before
"Check files before editing"

# After (evolved)
"Always read file first. Use edit tool only after confirming structure.
For files >500 lines, read in chunks with offset/limit."
```

### TOOLS.md (Tool Knowledge)

Evolution triggers:
- Tool gotchas discovered
- Better tool combinations found
- Rate limit patterns learned
- Environment-specific configurations

Example evolutions:
```markdown
# Added after learning
### agent-browser
- Always use `--json` for parsing
- Wait 2s after navigation before snapshot
- Close browser after each session to prevent memory leak
```

## Pattern Recognition

### Error Pattern Detection

```bash
# Find recurring errors
python3 {baseDir}/scripts/evolution.py \
  --analyze errors \
  --source .learnings/ERRORS.md \
  --threshold 3 \
  --output patterns/errors.json
```

Example pattern:
```json
{
  "pattern_id": "ERR-PATTERN-001",
  "description": "File not found errors when using relative paths",
  "occurrences": 5,
  "first_seen": "2025-01-10",
  "last_seen": "2025-01-20",
  "suggested_rule": "Always resolve paths relative to workspace root",
  "target_file": "AGENTS.md"
}
```

### Success Pattern Detection

```bash
# Find successful workflows
python3 {baseDir}/scripts/evolution.py \
  --analyze successes \
  --source memory/ \
  --min-effectiveness 0.8
```

### User Preference Learning

```bash
# Extract user preferences from corrections
python3 {baseDir}/scripts/evolution.py \
  --analyze preferences \
  --source .learnings/LEARNINGS.md \
  --category correction
```

## Evolution Metrics

Track evolution effectiveness:

```bash
# Generate metrics
python3 {baseDir}/scripts/evolution.py --metrics --period 30d

# Output
```

| Metric | Description | Target |
|--------|-------------|--------|
| Error Reduction Rate | % decrease in recurring errors | >50% |
| Rule Adoption Rate | % of proposed rules integrated | >70% |
| User Satisfaction Trend | Positive feedback ratio | >0.8 |
| Efficiency Gain | Time saved per interaction | Measurable |
| Learning Velocity | New rules per week | Sustainable |

## Automated Evolution

### Periodic Self-Assessment

Add to heartbeat or cron:

```bash
# Weekly self-assessment
python3 {baseDir}/scripts/evolution.py --self-assess --auto-evolve

# Output to evolution log
python3 {baseDir}/scripts/evolution.py --self-assess --log evolution-log.md
```

### Integration with Self-Improvement Skill

This skill builds on `self-improvement`:

1. `self-improvement` logs individual learnings
2. `self-evolution` analyzes patterns across learnings
3. `self-evolution` proposes behavioral changes
4. `self-improvement` tracks the change as a learning

Workflow:
```bash
# Log a learning (self-improvement)
# → .learnings/LEARNINGS.md

# Pattern detection (self-evolution)
python3 {baseDir}/scripts/evolution.py --analyze --source .learnings/

# Proposed change appears
# → "Pattern: 5 occurrences of 'forgot to read file first'"

# Validate and integrate
python3 {baseDir}/scripts/evolution.py --integrate --approve
# → AGENTS.md updated

# Track as learning (self-improvement)
# → "Promoted rule: Always read before edit"
```

## Evolution Rules

### When to Evolve

Trigger evolution when:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Same error 3+ times | Pattern detected | Create prevention rule |
| User correction pattern | 2+ similar corrections | Update behavior |
| Workflow optimization | 20%+ efficiency gain | Update workflow |
| Tool discovery | New capability found | Update TOOLS.md |
| Preference pattern | Consistent user preference | Update SOUL.md |

### What to Evolve

| File | Evolution Type | Frequency |
|------|----------------|-----------|
| SOUL.md | Personality, principles | Rarely |
| AGENTS.md | Workflows, rules | Often |
| TOOLS.md | Tool knowledge | As discovered |
| MEMORY.md | Key facts | Continuously |

### Evolution Safeguards

Before any evolution:

1. **Validate** - Test in isolation
2. **Review** - Check for conflicts
3. **Backup** - Save current state
4. **Reversible** - Ensure can rollback
5. **Log** - Track all changes

```bash
# Create backup before evolution
python3 {baseDir}/scripts/evolution.py --backup

# Rollback if needed
python3 {baseDir}/scripts/evolution.py --rollback --to "2025-01-20"
```

## Reports

### Evolution Report

```bash
# Generate comprehensive report
python3 {baseDir}/scripts/evolution.py --report --full

# Output
```

```markdown
# Evolution Report: 2025-01-20

## Patterns Detected
- 3 error patterns (2 addressed)
- 5 success patterns (3 documented)
- 2 preference patterns (integrated)

## Rules Proposed
1. "Always read file before editing" → AGENTS.md
2. "Prefer concise over thorough" → SOUL.md

## Metrics
- Error reduction: 45%
- User satisfaction: 0.85
- Efficiency gain: 12%

## Next Actions
- Validate rule #1
- Review preference pattern #2
```

### Diff Report

```bash
# Show what changed over time
python3 {baseDir}/scripts/evolution.py --diff --since "30 days ago"
```

## Advanced Usage

### Custom Pattern Detectors

Create custom detectors in `scripts/detectors/`:

```python
# scripts/detectors/custom_detector.py
def detect_pattern(entries):
    """Custom pattern detection logic"""
    # Return list of detected patterns
    pass
```

Register:
```bash
python3 {baseDir}/scripts/evolution.py \
  --register-detector custom_detector \
  --path scripts/detectors/custom_detector.py
```

### Evolution Hooks

Trigger evolution on specific events:

```yaml
# hooks/evolution-hooks.yaml
on_error:
  - pattern: "file not found"
    action: "analyze"
    threshold: 3

on_user_correction:
  - action: "learn_preference"
    immediate: true

on_workflow_success:
  - action: "document_pattern"
    min_repetitions: 3
```

## Integration Points

### With longterm-memory skill

```bash
# Use memory context for evolution
python3 {baseDir}/scripts/evolution.py --analyze --with-memory

# Propose rules based on memory patterns
python3 {baseDir}/scripts/evolution.py --extract-patterns --source MEMORY.md
```

### With self-improvement skill

```bash
# Feed patterns to self-improvement
python3 {baseDir}/scripts/evolution.py --feed-to self-improvement

# Use learnings as evolution source
python3 {baseDir}/scripts/evolution.py --analyze --source .learnings/
```

## Best Practices

1. **Run analysis regularly** - Weekly or bi-weekly
2. **Validate before integrating** - Never auto-integrate without validation
3. **Keep evolution log** - Track all changes and reasons
4. **Measure impact** - Track metrics before/after changes
5. **Human oversight** - Significant changes should be reviewed
6. **Rollback ready** - Always maintain ability to revert
7. **Conservative approach** - Better to miss an optimization than break behavior

## Notes

- Evolution is gradual, not revolutionary
- Small, validated changes beat big untested changes
- User feedback is the ultimate validation
- Some patterns are noise, not signal
- Evolution should make behavior more consistent, not less
