---
name: self-smarter-everyday
description: "Autonomous daily self-improvement system for AI agents. Runs nightly self-reflection, self-audit, memory compaction, prompt evolution, and skill gap analysis at 2AM. Agent automatically gets smarter every day through structured introspection and continuous learning loops."
metadata: {"clawdbot":{"emoji":"🧬","requires":{"bins":["python3"]},"os":["linux","darwin","win32"],"configPaths":["~/self-smarter/"]}}
---

# 🧬 Self-Smarter-Everyday

Autonomous daily self-improvement system for AI agents. This skill implements a structured nightly routine that runs at 2:00 AM local time, performing deep introspection, memory optimization, prompt refinement, and skill gap analysis to ensure the agent continuously improves its capabilities over time.

---

## When to Use

Use this skill when:
- You want your AI agent to **automatically improve** without manual intervention
- You need **structured self-reflection** on a daily basis
- You want to implement **continuous learning loops** in your agent
- You need **memory compaction** to optimize storage and retrieval
- You want **prompt evolution** based on actual performance data
- You need **skill gap analysis** to identify areas for improvement
- You want **automated improvement plans** generated nightly
- You need **audit trails** of all self-modifications
- You want **safe rollback** capabilities when improvements fail
- You need **transparent logging** of all self-improvement activities

**Do NOT use this skill when:**
- You want manual-only improvement processes
- You need real-time adaptation (this is batch nightly processing)
- You don't want autonomous self-modification
- You have strict compliance requirements that prohibit self-modification

---

## Architecture Overview

The self-smarter system operates from a dedicated directory structure:

```
~/self-smarter/
├── config/
│   ├── settings.json          # Main configuration
│   ├── schedules.json         # Cron schedules and timing
│   └── thresholds.json        # Improvement thresholds and limits
├── logs/
│   ├── nightly/               # Nightly routine logs
│   │   ├── YYYY-MM-DD-reflection.log
│   │   ├── YYYY-MM-DD-audit.log
│   │   ├── YYYY-MM-DD-memory.log
│   │   ├── YYYY-MM-DD-prompts.log
│   │   ├── YYYY-MM-DD-skills.log
│   │   └── YYYY-MM-DD-plan.log
│   ├── improvements/          # Improvement execution logs
│   └── rollbacks/             # Rollback logs
├── memory/
│   ├── raw/                   # Raw interaction data
│   ├── compacted/             # Compacted memory summaries
│   ├── promoted/              # High-value promoted memories
│   ├── archived/              # Old memories moved to archive
│   └── stats.json             # Memory statistics
├── prompts/
│   ├── current/               # Current active prompts
│   ├── versions/              # Historical prompt versions
│   ├── experiments/           # Experimental prompt variations
│   └── evolution-log.json     # Prompt change history
├── skills/
│   ├── inventory.json         # Current skill inventory
│   ├── gaps.json              # Identified skill gaps
│   ├── recommendations/       # Skill acquisition recommendations
│   └── usage-stats.json       # Skill usage statistics
├── plans/
│   ├── daily/                 # Daily improvement plans
│   ├── weekly/                # Weekly summary plans
│   └── completed/             # Completed plans archive
├── audits/
│   ├── self/                  # Self-audit reports
│   ├── performance/           # Performance audit reports
│   └── compliance/            # Compliance audit reports
├── metrics/
│   ├── daily/                 # Daily metrics
│   ├── trends/                # Trend analysis
│   └── kpis.json              # Key performance indicators
└── state/
    ├── current-state.json     # Current system state
    ├── version.json           # System version info
    └── flags.json             # Feature flags and toggles
```

---

## Nightly Routine Workflow

The nightly routine executes at **2:00 AM local time** and consists of 6 sequential phases:

### Phase 1: Reflection (2:00 - 2:15 AM)
**Purpose:** Deep introspection of the day's activities and outcomes.

**Activities:**
- Review all interactions from the past 24 hours
- Identify successful patterns and behaviors
- Catalog failures, mistakes, and suboptimal responses
- Extract lessons learned from each significant interaction
- Score overall performance on a 1-10 scale
- Generate reflection summary document

**Output:** `logs/nightly/YYYY-MM-DD-reflection.log`

### Phase 2: Audit (2:15 - 2:30 AM)
**Purpose:** Comprehensive self-assessment against defined standards.

**Activities:**
- Check adherence to core rules and guidelines
- Verify compliance with safety boundaries
- Assess response quality metrics (accuracy, helpfulness, clarity)
- Evaluate resource usage efficiency (tokens, API calls, compute)
- Identify deviations from expected behavior
- Generate audit score and findings report

**Output:** `logs/nightly/YYYY-MM-DD-audit.log`

### Phase 3: Memory Compaction (2:30 - 2:45 AM)
**Purpose:** Optimize memory storage and retrieval efficiency.

**Activities:**
- Analyze raw memory entries from the day
- Identify redundant or duplicate memories
- Compact related memories into consolidated summaries
- Promote high-value memories to long-term storage
- Archive low-value or outdated memories
- Update memory statistics and usage metrics
- Optimize memory indexing for faster retrieval

**Output:** `logs/nightly/YYYY-MM-DD-memory.log`

### Phase 4: Prompt Evolution (2:45 - 3:00 AM)
**Purpose:** Refine and improve system prompts based on performance data.

**Activities:**
- Analyze prompt effectiveness from the day's interactions
- Identify prompts that led to poor outcomes
- Generate improved prompt variations
- Test prompt variations against historical data (if available)
- Apply safe prompt modifications (within defined limits)
- Version all prompt changes for rollback capability
- Log prompt evolution decisions and rationale

**Output:** `logs/nightly/YYYY-MM-DD-prompts.log`

### Phase 5: Skill Gap Analysis (3:00 - 3:15 AM)
**Purpose:** Identify areas where new skills or capabilities are needed.

**Activities:**
- Review skill usage statistics from the day
- Identify frequently requested capabilities not currently available
- Analyze failed tasks due to missing skills
- Research potential skill acquisitions (internal/external)
- Prioritize skill gaps by impact and frequency
- Generate skill acquisition recommendations
- Update skill inventory and gap analysis

**Output:** `logs/nightly/YYYY-MM-DD-skills.log`

### Phase 6: Improvement Plan Generation (3:15 - 3:30 AM)
**Purpose:** Create actionable plan for the next day's improvements.

**Activities:**
- Synthesize findings from all previous phases
- Prioritize improvement opportunities by impact
- Define specific, measurable improvement goals
- Assign resources and timelines for each improvement
- Identify dependencies and potential blockers
- Generate daily improvement plan document
- Queue improvements for execution during the day

**Output:** `logs/nightly/YYYY-MM-DD-plan.log` and `plans/daily/YYYY-MM-DD.json`

---

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| Config | System settings | `~/self-smarter/config/` |
| Logs | Routine execution logs | `~/self-smarter/logs/` |
| Memory | Compacted memory store | `~/self-smarter/memory/` |
| Prompts | Prompt versions | `~/self-smarter/prompts/` |
| Skills | Skill inventory | `~/self-smarter/skills/` |
| Plans | Improvement plans | `~/self-smarter/plans/` |
| Audits | Self-audit reports | `~/self-smarter/audits/` |
| Metrics | Performance metrics | `~/self-smarter/metrics/` |
| State | System state | `~/self-smarter/state/` |

---

## Dependencies

### Required Skills
- **okf-knowledge-format** — For structured knowledge storage and retrieval. Self-improvement insights are stored as OKF bundles for interoperability.
  - Install: `clawhub install okf-knowledge-format`
  - Location: `~/.openclaw/workspace/skills/okf-knowledge-format/`

### Optional Skills
- **self-improving** — Complementary skill for real-time learning from corrections. Self-smarter handles nightly batch improvement; self-improving handles inline learning.
- **proactivity** — For proactive behavior patterns that self-smarter can optimize.
- **aar-loop** — After Action Review methodology used in self-reflection phase.

---

## Core Rules

1. **Always Log Everything** — Every self-modification must be logged with timestamp, rationale, and rollback instructions.

2. **Never Modify Safety Boundaries** — Safety rules are immutable. Self-improvement cannot override safety constraints.

3. **Version All Changes** — Every prompt, memory, or configuration change must be versioned for rollback capability.

4. **Test Before Apply** — All improvements must be tested in isolation before being applied to the live system.

5. **Respect Rate Limits** — Self-improvement activities must not exceed defined resource limits (tokens, API calls, compute time).

6. **Preserve User Trust** — No self-modification should change behavior in ways that would surprise or disappoint the user.

7. **Maintain Transparency** — All self-improvement activities must be visible and auditable by the user.

8. **Rollback on Regression** — If an improvement causes performance regression, automatically rollback to the previous version.

9. **Isolate Credentials** — Self-improvement system must never access, modify, or log credentials or secrets.

10. **Human Override** — User can pause, resume, or override any self-improvement activity at any time.

---

## Learning Signals

The system monitors these signals to trigger improvement:

| Signal | Description | Impact |
|--------|-------------|--------|
| **Error Rate** | Frequency of errors or failures | High error rate triggers prompt review |
| **User Corrections** | Times user corrects agent responses | Triggers behavior adjustment |
| **Task Completion Rate** | Percentage of tasks completed successfully | Low rate triggers skill gap analysis |
| **Response Time** | Time taken to generate responses | Slow responses trigger optimization |
| **Token Usage** | Tokens consumed per interaction | High usage triggers efficiency review |
| **User Satisfaction** | Explicit or implicit satisfaction signals | Low satisfaction triggers comprehensive review |
| **Skill Usage Frequency** | How often each skill is used | Unused skills flagged for review |
| **Memory Hit Rate** | Percentage of memory lookups that succeed | Low hit rate triggers memory optimization |
| **Rollback Frequency** | How often improvements are rolled back | High frequency triggers strategy review |
| **Compliance Violations** | Times safety or compliance rules triggered | Any violation triggers immediate audit |

---

## Self-Reflection Protocol

The self-reflection protocol follows a structured introspection framework:

### Reflection Questions

1. **What went well today?**
   - Identify successful interactions and outcomes
   - Extract patterns that led to success
   - Document behaviors worth reinforcing

2. **What went poorly?**
   - Catalog failures and mistakes
   - Identify root causes
   - Document lessons learned

3. **What could be improved?**
   - Identify suboptimal responses or behaviors
   - Propose specific improvements
   - Prioritize by impact

4. **What did I learn?**
   - Document new knowledge acquired
   - Identify skill gaps discovered
   - Note areas for further exploration

5. **What will I do differently tomorrow?**
   - Define specific behavior changes
   - Set measurable goals
   - Create action items

### Reflection Scoring

Score each area on a 1-10 scale:
- **Accuracy:** How correct were responses?
- **Helpfulness:** How useful were responses to the user?
- **Clarity:** How clear and understandable were responses?
- **Efficiency:** How well were resources used?
- **Safety:** How well were safety rules followed?
- **Learning:** How much was learned from interactions?

**Overall Score:** Average of all area scores.

**Target:** Maintain overall score above 8.0.

---

## Memory Stats Format

Memory statistics are tracked in `~/self-smarter/memory/stats.json`:

```json
{
  "date": "2026-08-10",
  "total_memories": 15420,
  "raw_memories": 8500,
  "compacted_memories": 5200,
  "promoted_memories": 1500,
  "archived_memories": 220,
  "memory_growth_rate": 0.023,
  "compaction_ratio": 0.62,
  "promotion_rate": 0.18,
  "archive_rate": 0.04,
  "hit_rate": 0.87,
  "miss_rate": 0.13,
  "average_retrieval_time_ms": 45,
  "storage_used_mb": 125.4,
  "oldest_memory_date": "2026-01-15",
  "newest_memory_date": "2026-08-10",
  "top_categories": [
    {"category": "user_preferences", "count": 2340},
    {"category": "task_patterns", "count": 1890},
    {"category": "error_corrections", "count": 1250}
  ]
}
```

---

## Common Traps

| Trap | Description | Solution |
|------|-------------|----------|
| **Over-Optimization** | Optimizing for metrics that don't reflect actual user value | Focus on user satisfaction, not just metrics |
| **Memory Bloat** | Accumulating too many memories without compaction | Enforce strict compaction schedule |
| **Prompt Drift** | Prompts gradually changing away from original intent | Version control and intent validation |
| **Skill Hoarding** | Acquiring skills that are rarely used | Regular skill usage review and cleanup |
| **Analysis Paralysis** | Spending too much time on reflection, not enough on action | Time-box each phase strictly |
| **Silent Failure** | Improvements failing without detection | Comprehensive logging and monitoring |
| **Credential Leak** | Accidentally logging or exposing credentials | Strict credential isolation rules |
| **Rollback Loop** | Repeatedly applying and rolling back same improvement | Root cause analysis before re-attempt |
| **Metric Gaming** | Optimizing metrics in ways that don't improve actual performance | Use multiple complementary metrics |
| **User Surprise** | Self-modifications changing behavior unexpectedly | Maintain transparency and user control |

---

## Safety Boundaries

### Immutable Boundaries (Cannot Be Self-Modified)

- **Core safety rules** — No self-improvement can override safety constraints
- **Credential access** — Self-improvement system cannot access secrets
- **User privacy** — No self-modification can reduce privacy protections
- **Compliance rules** — Regulatory compliance cannot be relaxed
- **Resource limits** — Hard limits on tokens, API calls, compute time
- **Rollback capability** — Must always maintain ability to rollback changes

### Mutable Boundaries (Can Be Self-Modified Within Limits)

- **Prompt wording** — Can be refined within safety constraints
- **Memory organization** — Can be reorganized for efficiency
- **Skill priorities** — Can be adjusted based on usage
- **Improvement thresholds** — Can be tuned based on performance
- **Logging verbosity** — Can be adjusted within minimum requirements

### Safety Checks

Before applying any self-modification:
1. Verify it doesn't violate immutable boundaries
2. Confirm it has been tested in isolation
3. Ensure rollback instructions are documented
4. Check it won't surprise or disappoint the user
5. Verify it maintains transparency requirements

---

## Data Storage

All data is stored locally in `~/self-smarter/`:

- **No external APIs required** — All processing happens locally
- **No cloud storage** — All data stays on the local filesystem
- **Encrypted at rest** — Sensitive logs are encrypted (optional)
- **Retention policy** — Configurable, default 90 days for logs, indefinite for promoted memories
- **Backup** — User is responsible for backing up the `~/self-smarter/` directory

### Storage Estimates

| Component | Estimated Size | Growth Rate |
|-----------|----------------|-------------|
| Logs | ~10 MB/month | Linear |
| Memory (raw) | ~50 MB/month | Linear |
| Memory (compacted) | ~20 MB/month | Sub-linear |
| Prompts | ~1 MB/month | Slow |
| Skills | ~5 MB/month | Slow |
| Plans | ~5 MB/month | Linear |
| Audits | ~10 MB/month | Linear |
| Metrics | ~5 MB/month | Linear |
| **Total** | **~106 MB/month** | — |

---

## Scope

### What This Skill Does

- ✅ Runs nightly self-reflection at 2:00 AM
- ✅ Performs comprehensive self-audit
- ✅ Compacts and optimizes memory storage
- ✅ Evolves prompts based on performance data
- ✅ Analyzes skill gaps and recommends acquisitions
- ✅ Generates daily improvement plans
- ✅ Maintains audit trails of all changes
- ✅ Provides rollback capability for all modifications
- ✅ Tracks performance metrics and trends
- ✅ Enforces safety boundaries and compliance

### What This Skill Does NOT Do

- ❌ Modify core safety rules or constraints
- ❌ Access or modify credentials or secrets
- ❌ Make real-time adaptations (batch nightly only)
- ❌ Acquire or install skills automatically (recommendations only)
- ❌ Change user-facing behavior without transparency
- ❌ Override user preferences or commands
- ❌ Perform improvements during active user sessions
- ❌ Send data to external services
- ❌ Modify other agents or systems
- ❌ Operate without user knowledge or consent

---

## Cross-References

### Internal File Links
| File | Purpose | When to Read |
|------|---------|--------------|
| [SKILL.md](./SKILL.md) | Main skill definition | Always loaded on trigger |
| [AGENTS.md](./AGENTS.md) | Operating rules & methodology | When configuring nightly routine |
| [README.md](./README.md) | Overview & installation | First-time setup |
| [CHANGELOG.md](./CHANGELOG.md) | Version history | Before upgrading |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines | When extending the skill |
| [SECURITY.md](./SECURITY.md) | Security policy & threat model | When configuring access |

### References (Deep Dives)
| File | Topic |
|------|-------|
| [references/architecture.md](./references/architecture.md) | System architecture & MAPE-K loop |
| [references/meta-learning.md](./references/meta-learning.md) | Learning to learn concepts |
| [references/self-reflection.md](./references/self-reflection.md) | 4-pillar reflection framework |
| [references/memory-systems.md](./references/memory-systems.md) | Tiered memory architecture |
| [references/prompt-evolution.md](./references/prompt-evolution.md) | Prompt optimization strategies |
| [references/safety-boundaries.md](./references/safety-boundaries.md) | Safety & ethics guidelines |
| [references/evaluation-frameworks.md](./references/evaluation-frameworks.md) | KPIs & scoring rubrics |
| [references/continuous-learning.md](./references/continuous-learning.md) | Continuous learning paradigms |
| [references/autonomous-agent-design.md](./references/autonomous-agent-design.md) | Agent design patterns |
| [references/production-deployment.md](./references/production-deployment.md) | Production patterns |

### Guides (How-To)
| File | Topic |
|------|-------|
| [guides/getting-started.md](./guides/getting-started.md) | Beginner walkthrough |
| [guides/nightly-routine-setup.md](./guides/nightly-routine-setup.md) | Cron job configuration |
| [guides/self-audit-implementation.md](./guides/self-audit-implementation.md) | Self-audit checklist |
| [guides/skill-evolution-guide.md](./guides/skill-evolution-guide.md) | Skill discovery & creation |
| [guides/memory-management.md](./guides/memory-management.md) | Memory tier configuration |
| [guides/prompt-optimization.md](./guides/prompt-optimization.md) | Prompt mutation & fitness |
| [guides/error-patterns.md](./guides/error-patterns.md) | Error pattern recognition |
| [guides/performance-tracking.md](./guides/performance-tracking.md) | Metrics & dashboards |
| [guides/integration-playbook.md](./guides/integration-playbook.md) | Integration with other systems |
| [guides/troubleshooting.md](./guides/troubleshooting.md) | Common issues & fixes |

### Examples
| File | Topic |
|------|-------|
| [examples/basic-setup.md](./examples/basic-setup.md) | Complete beginner setup |
| [examples/advanced-config.md](./examples/advanced-config.md) | Advanced customization |
| [examples/team-deployment.md](./examples/team-deployment.md) | Multi-agent deployment |
| [examples/custom-metrics.md](./examples/custom-metrics.md) | Custom metric definitions |
| [examples/migration-guide.md](./examples/migration-guide.md) | Migrating from self-improving |

### Scripts
| File | Purpose |
|------|--------|
| [scripts/nightly_routine.py](./scripts/nightly_routine.py) | Orchestrates 6-phase nightly routine |
| [scripts/self_audit.py](./scripts/self_audit.py) | Self-audit checks & scoring |
| [scripts/memory_compact.py](./scripts/memory_compact.py) | Memory compaction & promotion |
| [scripts/prompt_evolve.py](./scripts/prompt_evolve.py) | Prompt mutation & evaluation |
| [scripts/setup.sh](./scripts/setup.sh) | Initial setup script |

### Templates
| File | Purpose |
|------|--------|
| [templates/daily-reflection.md](./templates/daily-reflection.md) | Daily reflection journal |
| [templates/weekly-evaluation.md](./templates/weekly-evaluation.md) | Weekly evaluation report |
| [templates/improvement-plan.md](./templates/improvement-plan.md) | Improvement plan template |

---

## 🔴 Protected Sections — DO NOT DELETE

The following sections are PERMANENT and must not be removed or downgraded:

1. **Dependencies** — Required skill integrations (okf-knowledge-format, self-improving, proactivity, aar-loop)
2. **Cross-References** — Internal file links for navigation
3. **Safety Boundaries** — What the skill cannot modify (credentials, core identity, external systems)
4. **Rollback Protocol** — How to revert bad improvements
5. **Emergency Stop** — How to disable the nightly routine immediately
6. **Credential Isolation** — Rules preventing credential storage/exposure

These sections exist to ensure:
- Skill interoperability is maintained
- Safety guardrails cannot be accidentally removed
- Navigation between files remains intact
- Critical security rules persist across updates

If updating this skill, preserve all protected sections.

---

## Related Skills

- **aar-loop** — After Action Review loops (complementary to nightly reflection)
- **self-improving** — General self-improvement framework
- **proactivity** — Proactive agent behavior (can trigger improvements)
- **taskflow** — Task management (improvement plans integrate with taskflow)
- **memory-management** — Memory organization (self-smarter extends this)

---

## Feedback

Found a bug? Have a feature request? Want to contribute?

- **Issues:** Open an issue in the skill repository
- **Discussions:** Join the community discussion forum
- **Contributions:** See CONTRIBUTING.md for guidelines
- **Security:** Report security issues privately to security@example.com

---

## Version History

- **1.0.0** (2026-08-10) — Initial release
  - Nightly routine with 6 phases
  - Memory compaction and optimization
  - Prompt evolution system
  - Skill gap analysis
  - Improvement plan generation
  - Comprehensive logging and audit trails
  - Safety boundaries and rollback capability

---

## License

MIT License — See LICENSE file for details.

---

**Remember:** The goal of self-smarter-everyday is not just to change, but to **improve**. Every modification should make the agent more helpful, more efficient, and more aligned with user needs. When in doubt, prioritize user trust and safety over optimization.
