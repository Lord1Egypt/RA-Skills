# Quorum — Reference Implementation

A working Python implementation of the [Quorum](../SPEC.md) multi-critic quality validation system.

Quorum evaluates artifacts (agent configurations, research documents, code) against domain-specific rubrics using specialized critics that are **required to provide grounded evidence** for every finding.

---

## Quick Start

### 1. Install

```bash
cd reference-implementation
pip install -e .
```

Or without installing:
```bash
pip install -r requirements.txt
python -m quorum --help
```

### 2. Configure API Keys

Quorum uses [LiteLLM](https://docs.litellm.ai/) as its universal provider, supporting Anthropic, OpenAI, Mistral, Groq, and 100+ others.

```bash
# Anthropic (Claude)
export ANTHROPIC_API_KEY=your-key-here

# OpenAI
export OPENAI_API_KEY=your-key-here
```

### 3. Run Your First Validation

```bash
# Validate the included example research document
quorum run --target examples/sample-research.md --depth quick

# Validate the example agent config
quorum run --target examples/sample-agent-config.yaml --rubric agent-config

# Use a specific rubric
quorum run --target my-research.md --rubric research-synthesis --depth standard

# Batch: validate all markdown files in a directory
quorum run --target ./docs/ --pattern "*.md" --rubric research-synthesis

# Cross-artifact: validate with a relationships manifest
quorum run --target my-spec.md --relationships quorum-relationships.yaml
```

---

## Usage

```
Usage: quorum [OPTIONS] COMMAND [ARGS]...

  Quorum — Multi-critic quality validation.

Options:
  --version  Show the version and exit.
  -v         Enable debug logging
  --help     Show this message and exit.

Commands:
  run            Validate an artifact against a rubric
  rubrics list   List available built-in rubrics
  rubrics show   Show criteria for a specific rubric
  config init    Interactive first-run setup
```

### `quorum run`

```bash
quorum run \
  --target <file-or-dir>              # required: artifact, directory, or glob to validate
  --depth quick|standard|thorough     # depth profile (default: quick)
  --rubric <name-or-path>             # rubric to use (auto-detected if omitted)
  --pattern "*.md"                    # filter files when --target is a directory
  --relationships <manifest.yaml>     # cross-artifact manifest for Phase 2 consistency checks
  --output-dir ./my-runs              # where to write outputs (default: ./quorum-runs/)
  --verbose                           # show full evidence for all findings
```

**Exit codes:**
- `0` — PASS or PASS_WITH_NOTES (no blocking issues)
- `1` — Error (bad arguments, missing file, API failure)
- `2` — REVISE or REJECT (validation failed; artifact needs work)

---

## Depth Profiles

| Depth | Critics | Fix Loops | Use For |
|-------|---------|-----------|---------|
| `quick` | correctness, completeness | 0 | Fast feedback, drafts |
| `standard` | correctness, completeness, security, code_hygiene | 0 | Most work, PR reviews |
| `thorough` | all 4 shipped critics (more as they land) | 1 (Fixer proposals) | Critical decisions, production changes |

All depth profiles include the deterministic **pre-screen** (10 checks, no LLM cost) before any critics run.

Edit `quorum/configs/*.yaml` to customize model assignments and critic panels.

---

## Rubrics

Rubrics define what "good" looks like for a domain. Built-in rubrics:

| Name | Domain | Criteria |
|------|--------|----------|
| `research-synthesis` | Research documents | Citations, logic, completeness, causation |
| `agent-config` | Agent configurations | Model assignments, permissions, error handling |
| `python-code` | Python source files | 25 criteria (PC-001–PC-025); auto-detected on `.py` files |

```bash
# List available rubrics
quorum rubrics list

# Show rubric criteria
quorum rubrics show research-synthesis
```

### Custom Rubrics

Create a JSON file matching this schema:

```json
{
  "name": "My Custom Rubric",
  "domain": "my-domain",
  "version": "1.0",
  "criteria": [
    {
      "id": "CR-001",
      "criterion": "What to check",
      "severity": "HIGH",
      "evidence_required": "What proof must be shown",
      "why": "Why this matters"
    }
  ]
}
```

Then: `quorum run --target my-file.txt --rubric ./my-rubric.json`

---

## Outputs

Each `quorum run` creates a timestamped directory:

```
quorum-runs/
└── 20260223-143022-sample-research/
    ├── run-manifest.json              # Run parameters, flags, model config
    ├── artifact.txt                   # The artifact (copy)
    ├── rubric.json                    # Rubric used
    ├── prescreen.json                 # Deterministic pre-screen results (PS-001–PS-010)
    ├── critics/
    │   ├── correctness-findings.json
    │   ├── completeness-findings.json
    │   ├── security-findings.json
    │   ├── code_hygiene-findings.json
    │   └── cross_consistency-findings.json  # Phase 2 (if --relationships used)
    ├── verdict.json                   # Machine-readable verdict
    └── report.md                      # Human-readable report
```

For batch runs, each file gets its own timestamped sub-directory. A top-level `batch-verdict.json` summarizes the full run.

---

## Architecture

```
quorum run --target file --relationships manifest.yaml
  ↓
pipeline.py          load config, rubric, artifact
  ↓
prescreen.py         10 deterministic checks (PS-001–PS-010)
                     → prescreen.json (no LLM, runs instantly)
  ↓
supervisor.py        Phase 1: classify domain, dispatch critics concurrently
                     (ThreadPoolExecutor, max 4 critics in parallel;
                      batch files run concurrently max 3)
  ↓
correctness.py    }
completeness.py   }  each critic → LLM → structured findings (parallel)
security.py       }  (framework-grounded: OWASP ASVS, CWE, NIST SA-11,
code_hygiene.py   }   ISO 25010:2023, CISQ)
  ↓
fixer.py             Phase 1.5: proposes text replacements for CRITICAL/HIGH
                     (only if max_fix_loops > 0; thorough depth default: 1)
  ↓
cross_artifact.py    Phase 2: cross-artifact consistency critic
                     (only if --relationships provided)
                     receives Phase 1 findings as context — NOT verdicts
  ↓
aggregator.py        deduplicate, resolve conflicts, assign verdict
  ↓
output.py            terminal report + write run directory
```

**The core principle:** Every finding must have evidence (a quote, a tool result, a rubric citation). The Aggregator rejects ungrounded claims. This prevents LLM hand-waving.

**Phase 1 vs Phase 2:** Phase 1 critics evaluate each file independently. Phase 2 (Cross-Artifact Consistency) receives Phase 1 *findings* — not verdicts — as context and evaluates declared relationships between files. This keeps phases independent: Phase 2 sees what was found, not a judgment.

---

## Configuration

Quorum uses YAML config files for depth profiles. See `quorum/configs/`:

```yaml
# quorum/configs/quick.yaml
critics:
  - correctness
  - completeness

model_tier1: claude-opus-4     # Strong model (judgment-heavy roles)
model_tier2: claude-sonnet-4   # Efficient model (critic execution)

max_fix_loops: 0
depth_profile: quick
temperature: 0.1
max_tokens: 4096
```

Model names follow [LiteLLM conventions](https://docs.litellm.ai/docs/providers) — any provider LiteLLM supports works here.

---

## Cross-Artifact Validation

When your project has multiple files that should agree with each other — a spec and its implementation, an API contract and its consumers, a config and its schema — use `--relationships` to declare those relationships and let Quorum check them.

### Relationship Manifest

Create `quorum-relationships.yaml`:

```yaml
version: "1.0"
relationships:
  - source: src/api_handler.py
    target: docs/api-spec.md
    type: implements
    description: "Handler must implement all endpoints declared in spec"

  - source: docs/api-spec.md
    target: src/api_handler.py
    type: documents
    description: "Spec must document all public endpoints in handler"

  - source: quorum/critics/security.py
    target: quorum/configs/standard.yaml
    type: delegates
    description: "Security critic is enabled in standard depth profile"

  - source: data/output-schema.json
    target: src/pipeline.py
    type: schema_contract
    description: "Pipeline output must conform to declared schema"
```

**Relationship types:** `implements`, `documents`, `delegates`, `schema_contract`

### Running with Relationships

```bash
quorum run \
  --target ./src/ \
  --relationships quorum-relationships.yaml \
  --depth standard
```

The Cross-Artifact Consistency critic evaluates each declared relationship, looking for mismatches, undocumented behavior, and broken contracts. Findings use a **Locus model** — each finding references both files with role annotations (`source_role`, `target_role`) and a `source_hash` to ensure the finding is pinned to the artifact version that was evaluated.

---

## Extending Quorum

### Adding a New Critic

1. Create `quorum/critics/my_critic.py` inheriting from `BaseCritic`
2. Implement `name`, `system_prompt`, and `build_prompt()`
3. Register it in `quorum/agents/supervisor.py` → `CRITIC_REGISTRY`
4. Add the name to your config's `critics` list

See `quorum/critics/correctness.py` for a complete example.

### Adding a Cross-Artifact Critic

The Cross-Artifact Consistency critic does **not** inherit from `BaseCritic` — it uses a separate `CrossArtifactCritic` base class with a different interface, because it operates on pairs/groups of files rather than a single artifact. It also receives Phase 1 findings as additional context via `build_prompt()`.

Supported relationship types for manifest declarations: `implements`, `documents`, `delegates`, `schema_contract`. New types can be added by extending the relationship type registry.

---

## License

MIT — see [LICENSE](../LICENSE) for details.
