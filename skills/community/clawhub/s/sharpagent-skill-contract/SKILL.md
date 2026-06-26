---
name: sharpagent-skill-contract
version: 1.0.0
description: "SharpAgent Skill Contract — Schema-driven skill scaffolding tool. Generates, validates, and packages SharpAgent-compliant skills with five-factor trust verification, calibration framework hooks, and content safety integration."
metadata:
  openclaw:
    emoji: "📋"
    tags:
      - scaffolding
      - schema
      - validation
      - skill-creation
      - sharpagent
      - five-factor
---

# SharpAgent Skill Contract v1.0.0

> **Foundation shovel** — Generate, validate, and package all SharpAgent skills.
> Fusion of Ontology Schema + Skill Creator + Skill Oracle.

## When to Use

Use this skill when:

- Creating a **new SharpAgent-compliant Skill** from scratch
- **Validating** an existing Skill for contract compliance
- **Packaging** a Skill for ClawHub publication under `SharpAgent`
- **Upgrading** a legacy Skill to SharpAgent standards

## What Is a Skill Contract

Every SharpAgent Skill must declare a **contract** — a YAML block that states:

```yaml
contract:
  name: sharpagent-five-factor-review
  version: "1.0.0"
  category: analysis
  trust_level: verified            # draft | verified | audited
  reads:
    - InformationSource
    - LearningEntry
  writes:
    - FiveFactorResult
  preconditions:
    - "Must have at least one InformationSource to analyze"
    - "Must have access to web_search or memory_search tool"
  postconditions:
    - "Output contains overall_confidence score (0-10)"
    - "Each of 5 factors has a value"
  calibration:
    default_mode: professional     # warm | professional | deep
    modes_supported: [warm, professional, deep]
  compliance:
    jurisdiction: global           # cn | us | eu | global
    safety_level: standard         # minimal | standard | strict
  lifecycle:
    status: active
    publish_as: SharpAgent
```

## Workflow

### Step 1: Scaffold a New Skill

```bash
sharpagent scaffold --name sharpagent-five-factor-review --category analysis
```

Generates:

```
/sharpagent-skills/sharpagent-five-factor-review/
├── SKILL.md            # Contract + documentation
├── contract.yaml       # Machine-readable contract (auto-derived)
├── scripts/            # Runtime scripts (optional)
├── references/         # Supporting docs (optional)
└── test/               # Validation tests (optional)
```

### Step 2: Validate Contract

```bash
sharpagent validate --path ./sharpagent-five-factor-review/SKILL.md
```

Checks:
- **Structural**: All required YAML fields present
- **Semantic**: reads/writes match known ontology types
- **Integrity**: preconditions reference real capabilities
- **Naming**: snake_case, no spaces, max 40 chars

```json
{
  "valid": true,
  "warnings": [],
  "errors": [],
  "score": 100,
  "missing_optional": ["scripts/ directory missing"]
}
```

### Step 3: Package for Publication

```bash
sharpagent package --name sharpagent-five-factor-review --output ./dist/
```

Produces:

```
./dist/sharpagent-five-factor-review.tar.gz
├── SKILL.md
├── contract.yaml
├── scripts/
└── references/
```

## Contract YAML Schema Reference

### Top-Level Fields

| Field | Type | Required | Default |
|-------|------|----------|---------|
| `contract.name` | string | ✅ | - |
| `contract.version` | semver | ✅ | "0.0.1" |
| `contract.category` | enum | ✅ | - |
| `contract.trust_level` | enum | ✅ | "draft" |
| `contract.reads` | string[] | ✅ | [] |
| `contract.writes` | string[] | ✅ | [] |
| `contract.preconditions` | string[] | ✅ | [] |
| `contract.postconditions` | string[] | ❌ | [] |
| `contract.calibration` | object | ✅ | default |
| `contract.compliance` | object | ✅ | default |
| `contract.lifecycle` | object | ✅ | default |

### Contract Categories

| Category | Description | Example Skills |
|----------|-------------|----------------|
| `analysis` | Analyzes input, produces structured output | Five-factor review |
| `workflow` | Multi-step process with gates | Engineering lifecycle |
| `monitor` | Periodic scanning and alerting | Intelligence briefing |
| `memory` | Storage, retrieval, consolidation | Memory management |
| `scaffold` | Code/file generation | Skill creation |
| `integration` | External service bridging | API clients |

### Trust Levels

| Level | Meaning | When |
|-------|---------|------|
| `draft` | Work in progress, unverified | Initial creation |
| `verified` | Contract structure validated | After validation |
| `audited` | Full five-factor trust audit passed | Community verified |

### Calibration Modes

```yaml
calibration:
  default_mode: professional
  modes_supported: [warm, professional, deep]
```

| Mode | Warm | Professional | Deep |
|------|------|-------------|------|
| Tone | Friendly, supportive | Neutral, precise | Analytical, detailed |
| Detail | Concise | Balanced | Exhaustive |
| Use case | User-facing | Internal reports | Research analysis |

## Integration Points

### With Five-Factor Review
- `writes: [FiveFactorResult]` → Contract schema is consumed by the five-factor review skill
- Contract trust_level is validated using FiveFactorResult as part of skill audit

### With Calibration Framework
- `contract.calibration` block defines which modes are supported
- At runtime, the calibration engine checks `contract.calibration.modes_supported`

### With Content Safety Engine
- `contract.compliance` block sets safety policies
- `safety_level: standard` is the minimum for ClawHub publication

## Quality Gates

| Check | What | Fail action |
|-------|------|-------------|
| Schema valid | All required YAML fields present | Block packaging |
| Type consistency | reads/writes reference known types | Warn |
| Naming convention | snake_case, ≤40 chars | Warn |
| Calibration declared | At least default_mode set | Warn |
| Preconditions non-empty | preconditions list ≥1 item | Warn |
| Version format | valid semver | Block packaging |

## Edge Cases

| Situation | Action |
|-----------|--------|
| No reads (standalone) | Allow with warning |
| reads = writes | Warn (likely mistake) |
| Type cross-reference fails | Warn + list unknown types |
| Calibration missing | Set default: professional + standard |
| Draft trust_level | Allow creation, warn on packaging |
| SKILL.md has no contract block | Fail validation |

## Dependencies

- **YAML parser** (for reading contract blocks)
- **jq** or Python 3 (for validation scripts)
- **tar** (for packaging)

## Version History

- **v1.0.0** — Initial release. Skill Contract scaffolding + validation + packaging.

---

*SharpAgent · MIT-0 · 2026-05-11*
