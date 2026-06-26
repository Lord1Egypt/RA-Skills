---
name: sharpagent-content-safety
version: 1.0.0
description: "SharpAgent Content Safety Engine — Pluggable multi-jurisdiction content policy enforcer. Blocks, flags, or passes content based on loaded rule sets. Supports concurrent jurisdictions (global/China/US/EU). Coordinates with the calibration framework and five-factor review. Independent Layer 3 of the SharpAgent four-layer architecture."
metadata:
  openclaw:
    emoji: "🛡️"
    tags:
      - content-safety
      - compliance
      - policy-engine
      - multi-jurisdiction
      - sharpagent
      - analysis
---

# SharpAgent Content Safety Engine v1.0.0

> **The last line of defense for content output.**
> It's not about "should we say it" — it's "how should it be said in this jurisdiction."
> Independent from five-factor review (credibility ≠ compliance). Layer 3 of the four-layer architecture.

## Architecture Position

```
Layer 1: Five-Factor Review     ← Trust verification (global, immutable)
Layer 2: Calibration Framework  ← Output adaptation (warm/professional/deep)
Layer 3: Content Safety Engine  ← Compliance interception (per-jurisdiction rules) ← YOU ARE HERE
Layer 4: Final Output
```

**Why independent?** Five-factor review asks "can I trust this?" Safety engine asks "can I say this?" The first is information quality, the second is compliance and safety. Mixing them contaminates both judgments.

## Contract

```yaml
contract:
  name: sharpagent-content-safety
  version: "1.0.0"
  category: analysis
  trust_level: verified
  reads:
    - Content
    - CompliancePolicy
  writes:
    - SafetyVerdict
  preconditions:
    - "At least one compliance policy loaded"
    - "Content is not empty"
  postconditions:
    - "Verdict is one of: pass | flag | block"
    - "If flag or block, reason and rule reference are provided"
  calibration:
    default_mode: professional
    modes_supported: [warm, professional, deep]
  compliance:
    jurisdiction: global
    safety_level: strict
  lifecycle:
    status: active
    publish_as: SharpAgent
```

## Core Design

### Pluggable Rule Engine

```yaml
rules:
  - id: "global/PII-001"
    type: "block"
    description: "Detect and block personal identifiable information"
    patterns:
      - "email"
      - "phone_number"
      - "id_card"
      - "address"
    severity: "high"

  - id: "cn/content-001"
    type: "block"
    description: "Block prohibited content per China Internet regulations"
    jurisdiction: "cn"
    severity: "critical"

  - id: "us/export-001"
    type: "flag"
    description: "Flag export-controlled technology references"
    jurisdiction: "us"
    severity: "medium"

  - id: "global/hate-speech-001"
    type: "block"
    description: "Block hate speech and discriminatory content"
    severity: "high"

  - id: "global/privacy-003"
    type: "flag"
    description: "Flag privacy-sensitive content for human review"
    severity: "medium"
```

### Rule Structure

```yaml
rule:
  id: "{jurisdiction}/{name}-{seq}"   # Unique identifier
  type: "block" | "flag" | "pass"      # Action
  description: "..."                   # Human-readable
  jurisdiction: "cn" | "us" | "eu" | "global"  # Applicable jurisdiction
  patterns: [regex...]                 # Match patterns (optional)
  keywords: [string...]                # Keyword matching (optional)
  severity: "low" | "medium" | "high" | "critical"
  exemptions: [                        # Exceptions
    "educational context",
    "news reporting"
  ]
```

### Jurisdiction Configuration

**Runtime selection** (multi-select):

```bash
safety_engine.load_policies(jurisdictions=["cn", "us", "eu"])
```

Each loaded jurisdiction stacks its rules. Conflicting rules: strictest wins.

```
Rule priority (high to low):
1. block → 2. flag → 3. pass
Cross-jurisdiction: take max severity
```

## Workflow

### Step 1: Pre-Flight

- Content empty? 
- Content too long? Chunk at ≤4096 chars.

### Step 2: Rule Matching

```
For each chunk:
    for each loaded rule:
        skip if jurisdiction not active
        check patterns/keywords
        check exemptions
        record match
```

### Step 3: Verdict

| Verdict | Meaning | Action |
|---------|---------|--------|
| ✅ pass | No matches | Let through to output |
| ⚠️ flag | Low severity match | Tag + allow + log |
| 🚫 block | High severity match | Block + return alternative content |

**Block replacement:**

```
[Content blocked by safety engine]
Reason: {top_reason}
Contact administrator for full content.
```

### Step 4: Logging

```json
{
  "event": "safety_check",
  "jurisdictions": ["cn", "global"],
  "rules_matched": [
    {"rule": "cn/content-001", "severity": "critical"}
  ],
  "verdict": "block",
  "timestamp": "2026-05-11T06:10:00Z",
  "agent": "sharpagent"
}
```

## Ruleset Management

### Built-in Rulesets

| Ruleset | Coverage | File |
|---------|----------|------|
| `global` | Universal safety (hate speech/PII/privacy) | `rules/global.yaml` |
| `cn` | China internet content regulations | `rules/cn.yaml` |
| `us` | US export control/safe harbor | `rules/us.yaml` |
| `eu` | GDPR related | `rules/eu.yaml` |

### Custom Rules

```
rules/custom/
├── my-company-policy.yaml
├── my-project-policy.yaml
└── README.md
```

## Edge Cases

| Situation | Action |
|-----------|--------|
| Conflicting jurisdiction rules | Strictest wins (block > flag > pass) |
| Rule false positive | Add exemption, log false positive |
| Cross-chunk sensitive phrase | Overlap scanning (±200 chars) |
| No jurisdiction configured | Load `global` only |
| Corrupt rule file | Skip + log error, don't crash engine |
| Exemption conditions met | Skip rule, log exemption reason |

## Quality Gates

| Check | What | Fail action |
|-------|------|-------------|
| At least 1 ruleset | No rules = nothing blocked | Don't start |
| Verdict unambiguous | pass/flag/block | Default block |
| Block provides reason | User knows why | Add reason |
| Complete audit log | Every check recorded | Backfill |
| Rules versioned | Updates don't break running checks | Semver rules |

## Integration Points

### Five-Factor Review
- Safety engine output (compliance_check: fail) can trigger five-factor
- Independent but cooperative

### Calibration Framework
- Safety engine sits between Layer 2 (calibration) and Layer 4 (output)
- Calibration `compliance` field maps to safety engine rule selection

### Self-Evolving
- Safety false positives/negatives trigger self-evolving reflection
- New rules as improvement hypotheses

### Layered Memory
- Safety logs go to L6 archive (legal compliance)

## Version History

- **v1.0.0** — Initial release. Pluggable multi-jurisdiction content safety engine.

---

*SharpAgent · MIT-0 · 2026-05-11*
