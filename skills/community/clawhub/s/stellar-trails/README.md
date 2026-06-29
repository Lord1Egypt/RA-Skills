<div align="center">

<img src="chibi.svg" alt="Stellar Trails mascot" width="180">

# Stellar Trails

A structured six-phase workflow for LLM agents — traceability IDs, entry/exit gates, scope commitment, and adaptive complexity. No shell execution, pure markdown data.

</div>

## Quick Start

### Path A — ZAI Platform (recommended)

```bash
curl -sL https://github.com/hoshiyomiX/stellar-trails/releases/latest/download/stellar-trails.zip -o /home/user_skills/stellar-trails.zip && touch /home/user_skills/.stellar-trails.usermark && echo "✓ installed"
```

Next session: ZAI service auto-extracts zip to `/home/z/my-project/skills/stellar-trails/`. Invoke via:

```
Skill(command="stellar-trails")
```

### Path B — Standalone (non-ZAI)

```bash
curl -sL https://github.com/hoshiyomiX/stellar-trails/releases/latest/download/stellar-trails.zip -o /tmp/st.zip && unzip -q /tmp/st.zip -d /tmp/ && cp -a /tmp/stellar-trails /home/z/my-project/skills/ && mkdir -p /home/z/my-project/.zscripts && cp /tmp/stellar-trails/{chibi.svg,index.html,dev.sh} /home/z/my-project/.zscripts/ && chmod +x /home/z/my-project/.zscripts/dev.sh && rm -rf /tmp/stellar-trails /tmp/st.zip && echo "✓ installed"
```

For popup preview: `bash /home/z/my-project/.zscripts/dev.sh` (serves :3000 with no-cache headers).

## Version History

| Version | Date | Summary |
|---------|------|---------|
| 7.9.4 | 2026-06-27 | Solution 2 — Step 2 mandates re-read SKILL.md from disk AFTER clawhub update. Closes cache gap. |
| 7.9.3 | 2026-06-27 | Counter 3 LLM bypass patterns with explicit why arguments. |
| 7.9.2 | 2026-06-27 | Fix Step 2 — add --force to clawhub update. |
| 7.8.1 | 2026-06-27 | skill-creator audit fixes: P0 typo + refactor, P1 Worked Example, P2 evals + topic tags. |
| 7.8.0 | 2026-06-27 | AskUserQuestion gate + SADC subagent delegation. Closes 83% platform underusage gap. |
| 7.7.5 | 2026-06-27 | Banner → vertical checklist + mandatory execution + print mandate (4 places). |
| 7.7.4 | 2026-06-27 | Refactor activation banner layout to tree-style format (├─ / │  ├─ / └─). |
| 7.7.3 | 2026-06-27 | Added 9-step sequence to activation banner (top + Step 8 confirm). |
| 7.7.2 | 2026-06-27 | Corrected frequency guidance — all 9 activation steps run on every Skill() invoke. |
| 7.7.1 | 2026-06-27 | Restructure activation: merged Step 5 (Verify chibi.svg) into Step 4. Added new Step 5: Sync persistent zip. |
| 7.7.0 | 2026-06-27 | Fix 8 bugs causing LLM to skip activation steps. Replaced stale v7.5.0 zip with v7.6.2 zip. Rewrote SKILL.md activation section: added Step 1 (refresh context), imperative framing, expected-output checkpoints, removed dismissive parentheticals, split comment-heavy blocks, added session-frequency guidance. |
| 7.6.2 | 2026-06-27 | Language audit — fixed codeswitching + buzzword + hyperbole. Step numbering cleaned up: 0.5/1/1.5/1.6/2/3/4/5 → 1/2/3/4/5/6/7/8. |
| 7.6.1 | 2026-06-27 | Fix popup mascot cropping — .mascot CSS had border-radius:50% + object-fit:cover + forced square. Replaced with width:200px;height:auto. SVG renders at native aspect ratio, no cropping. |
| 7.6.0 | 2026-06-27 | BREAKING — mascot format change: chibi.png (binary, 1.2 MB) → chibi.svg (text SVG, 757 KB). Solves ClawHub binary-file-filter issue at the source. SVG passes registry filter natively. |
| 7.5.2 | 2026-06-26 | Defensive Step 1.6 — auto-restores chibi.png from local repo clone if missing after clawhub update (ClawHub publish filter workaround). |
| 7.5.1 | 2026-06-26 | Patch — register chibi.png in .checksums manifest (root-cause fix for mascot missing in popup preview). Audit: 6 documentation leftovers cleaned. |
| 7.2.0 | 2026-06-21 | boot.sh deleted (8 red flag patterns), replaced with dev.sh standalone (60 lines, no-cache HTTP server) |
| 7.1.4 | 2026-06-21 | New landing page (cosmic glassmorphism + phase flow diagram), dead code cleanup (386 lines removed) |
| 7.1.3 | 2026-06-20 | One-liner install (agent-friendly, no shell execution) |
| 7.1.2 | 2026-06-20 | Stable asset name `stellar-trails.zip` for releases/latest/download URL |
| 7.1.1 | 2026-06-20 | CI/CD GitHub Actions workflow + simplified install |
| 7.1.0 | 2026-06-20 | Stateless skill — removed bash boot.sh bootstrap from SKILL.md |
| 7.0.0 | 2026-06-19 | Rebrand stellar-frameworks → stellar-trails |
| 6.0.0 | 2026-05-25 | Version reset, chibi mascot, force-sync, co-location, activation fallback |

See [CHANGELOG.md](CHANGELOG.md) for full history.

## Architecture

```
stellar-trails/                   (repo root)
├── .github/workflows/release.yml # CI/CD: build zip + create release on tag push
├── .checksums                    # SHA-256 verification (21 files)
├── .gitignore
├── README.md                     # Root README (this file's parent)
└── skill/stellar-trails/         # Git-tracked source of truth
    ├── SKILL.md                  # Skill definition (activation + framework reference)
    ├── dev.sh                    # Standalone no-cache HTTP server (60 lines, popup preview)
    ├── index.html                # Landing page (minimalist, v7.5.0+)
    ├── chibi.svg                 # Mascot (SVG, passes ClawHub text-file filter)
    ├── memory-template.md        # Memory system templates & storage rules
    ├── procedure/
    │   ├── phases.md             # 6-phase workflow definitions + gates
    │   ├── templates/            # Output templates (problem-spec, implementation-plan, incident-report, verification-report)
    │   └── decision-trees/       # Error resolution + pivot assessment
    ├── knowledge/
    │   ├── platform/             # Z.ai sandbox constraints
    │   └── universal/            # Architecture, conventions, error patterns
    ├── constraints/              # Code standards + type safety rules
    ├── CHANGELOG.md              # Full version history
    └── README.md                 # This file
```

## What's Inside

- **Phase State Machine**: IDLE → SPECIFY → PLAN → IMPLEMENT → VERIFY → DELIVER (with error recovery loop)
- **Traceability IDs**: IMPL-001, IMPL-002... chain through every phase
- **Adaptive Complexity**: Minimal, Simple, Standard, Complex tiers
- **Source State Verification (SSV)**: git fetch before analysis
- **Source Availability & Documentation Check (SADC)**: research before planning
- **File-based Memory**: evergreen + dated files, bounded budget
- **Error Decision Tree**: 5-step capture → classify → identify → fix → re-verify
- **Stateless by Design**: no shell execution in Skill() invoke, pure markdown data

## Persistence Model (ZAI Platform)

| Layer | Mechanism | Survives reset? |
|---|---|---|
| `/home/user_skills/stellar-trails.zip` | PolarFS persistent mount | ✓ |
| ZAI service auto-extract | `/app/main.py` extracts zip to `skills/stellar-trails/` at session start | ✓ (re-extracted every session) |
| `.stellar-trails.usermark` | Marker "skill approved" in PolarFS | ✓ |

No shell execution in Skill() invoke. No `.zscripts/` persistent backup. No `~/.stellar-trails.log`. Pure markdown data, stateless skill.
