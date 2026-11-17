# skill-engineer

Design, test, review, and maintain agent skills for OpenClaw systems. Provides comprehensive lifecycle management for agent skills, including validation, quality assurance, integration testing, and — new in v3.1.1 — README sync to ensure documentation reflects the actual shipped skill.

## Overview

This skill enables systematic development and maintenance of agent skills following Anthropic's best practices. It includes:

- **Progressive disclosure** design patterns (YAML frontmatter → SKILL.md → references/)
- **Quality scoring system** for skill evaluation (completeness, clarity, balance, integration)
- **Tool selection validation** to prevent common execution errors
- **Self-play testing** protocols for skill validation
- **Agent kit audit** procedures for maintaining skill ecosystem health
- **README sync step** — after quality gates pass, README is regenerated from the final implementation to ensure accuracy before push

## Requirements

This skill uses a **multi-agent architecture** with three roles: Designer, Reviewer, and Tester. The orchestrating agent must be able to **spawn subagents** (e.g., via `sessions_spawn` in OpenClaw).

**Minimum setup:**
- An OpenClaw agent with subagent spawning capability (main session or top-level agent)
- At least 3 subagent sessions available per skill design cycle

**Single-agent fallback:** If subagent spawning is unavailable, the skill can run in role-based mode where one agent switches between Designer/Reviewer/Tester phases sequentially.

## Workflow

```
Requirements gathering
    ↓
Designer → Reviewer ──pass──→ Tester ──pass──→ README Sync → Push to GitHub
               │                   │
              fail                fail
               └──── Designer revises (max 3 iterations) ────┘
```

### Step Summary

| # | Step | Who | When to proceed |
|---|------|-----|----------------|
| 1-4 | Gather requirements, spawn Designer | Orchestrator | Always |
| 5-6 | Review artifacts | Reviewer | After Designer output |
| 7-9 | Test artifacts | Tester | After Reviewer passes |
| 10 | Add quality scorecard to README | Orchestrator | After Tester passes |
| 10.5 | **Sync README to final implementation** | Orchestrator | After all gates pass |
| 11 | Push to GitHub | Orchestrator | After README sync |

### README Sync (Step 10.5)

After all quality gates pass, the orchestrator regenerates the README to match the **actual shipped skill** — not the original design brief. Skills often evolve during iteration; the README must reflect what was actually built.

**What gets synced:**

| Section | Source of Truth |
|---------|----------------|
| Commands / triggers | `skill.yml` triggers block |
| Pipeline steps | Final `SKILL.md` |
| Configuration schema | `references/` or `SKILL.md` config section |
| File layout | Actual generated files (`find <skill-dir> -type f`) |
| Known Issues | Tester non-blocking issues + production lessons |
| Quality scorecard | Final Reviewer scores |

**Checks before committing README:**
- [ ] Version matches `skill.yml`
- [ ] All commands exist in `skill.yml` triggers
- [ ] No internal paths or organization-specific details (OPSEC)
- [ ] Known Issues section populated (even if "None known")
- [ ] Quality scorecard present with final scores

## Installation

```bash
cp -r skill-engineer ~/.openclaw/skills/
```

Or install via [ClawHub](https://clawhub.com).

## Usage

See [SKILL.md](SKILL.md) for detailed documentation on:
- Multi-agent architecture and orchestration loop
- Designer / Reviewer / Tester role guides (in `references/`)
- README sync protocol
- Quality standards and scoring rubric (33 checks)
- Agent kit audit procedures

## Structure

```
skill-engineer/
├── SKILL.md          — Main skill documentation
├── skill.yml         — Triggers and metadata
├── README.md         — This file (synced to final implementation)
├── CHANGELOG.md      — Version history
├── references/
│   ├── designer-guide.md    — Full Designer instructions
│   ├── reviewer-rubric.md   — 33-check quality rubric
│   └── tester-protocol.md   — Self-play test protocol
└── tests/
    └── test-triggers.json   — Trigger accuracy test cases
```

## Quality Scorecard

| Category | Score | Details |
|----------|-------|---------|
| Completeness (SQ-A) | 8/8 | Full lifecycle coverage, README sync step added |
| Clarity (SQ-B) | 5/5 | Unambiguous instructions, examples, edge cases addressed |
| Balance (SQ-C) | 5/5 | Appropriate workload distribution |
| Integration (SQ-D) | 5/5 | Standard formats, compatible with OpenClaw agent kit |
| Scope (SCOPE) | 3/3 | Clean boundaries, no scope creep |
| OPSEC | 2/2 | No violations |
| References (REF) | 3/3 | Anthropic guide cited, all claims traceable |
| Architecture (ARCH) | 2/2 | Designer/Reviewer/Tester separation enforced |
| **Total** | **33/33** | |

*Scored by skill-engineer Reviewer (iteration 3, self-review pipeline)*

## Known Issues

None known.

## License

MIT
