---
name: self-improving-science
description: "Captures learnings, experiment issues, and methodology corrections for continuous improvement in scientific research and ML workflows. Use when: (1) Data leakage detected in train/test split, (2) Model fails to reproduce across seeds or environments, (3) Statistical test misapplied or p-value misinterpreted, (4) Hypothesis test fails or needs revision, (5) Feature distribution shift detected, (6) User corrects methodology or analysis approach, (7) Experiment design flaw discovered. Also review learnings before designing new experiments."
---

# Self-Improving Science Skill

Log learnings, experiment issues, and methodology corrections to markdown files for continuous improvement in scientific research, data science, and ML/AI experimentation. Important findings get promoted to experiment checklists, data governance docs, model cards, and methodology standards.

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n\nMethodology insights, statistical corrections, and knowledge gaps captured during research.\n\n**Categories**: methodology_flaw | data_quality | reproducibility_issue | statistical_error | hypothesis_revision | experiment_design\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/EXPERIMENT_ISSUES.md ] || printf "# Experiment Issues\n\nFailed experiments, data quality problems, and reproducibility failures.\n\n---\n" > .learnings/EXPERIMENT_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nResearch tooling and ML pipeline capabilities requested by the user.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log proprietary datasets, patient identifiers, API keys, or raw data samples unless the user explicitly asks. Prefer summary statistics and redacted excerpts over full data dumps.

If you want automatic reminders or setup assistance, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Data leakage found in pipeline | Log to `.learnings/EXPERIMENT_ISSUES.md` with `data_quality` |
| Model fails to reproduce | Log to `.learnings/EXPERIMENT_ISSUES.md` with `reproducibility_issue` |
| Statistical test misapplied | Log to `.learnings/LEARNINGS.md` with `statistical_error` |
| Hypothesis test fails | Log to `.learnings/LEARNINGS.md` with `hypothesis_revision` |
| Methodology flaw discovered | Log to `.learnings/LEARNINGS.md` with `methodology_flaw` |
| Experiment design improvement | Log to `.learnings/LEARNINGS.md` with `experiment_design` |
| Feature distribution shift | Log to `.learnings/EXPERIMENT_ISSUES.md` with `data_quality` |
| User wants missing ML tool | Log to `.learnings/FEATURE_REQUESTS.md` |
| NaN loss or training divergence | Log to `.learnings/EXPERIMENT_ISSUES.md` |
| Missing data pattern discovered | Log to `.learnings/LEARNINGS.md` with `data_quality` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Broadly applicable finding | Promote to experiment checklist, model card, or methodology standard |
| Data governance insight | Promote to data governance docs |
| Model behavior documentation | Promote to model card |
| Pipeline best practice | Promote to `AGENTS.md` (OpenClaw workspace) |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-science
```

**Manual:**
```bash
git clone https://github.com/jose-compu/self-improving-science.git ~/.openclaw/skills/self-improving-science
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, experiment orchestration
├── SOUL.md            # Research principles, scientific rigor guidelines
├── TOOLS.md           # ML framework gotchas, data tool capabilities
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── EXPERIMENT_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` — methodology corrections, statistical insights, experiment design lessons
- `EXPERIMENT_ISSUES.md` — data quality failures, reproducibility problems, model drift events
- `FEATURE_REQUESTS.md` — requested research tooling and pipeline capabilities

### Promotion Targets

When learnings prove broadly applicable, promote them to research artifacts:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Experiment design patterns | Experiment Checklist | "Always check class balance before training" |
| Data handling rules | Data Governance Docs | "PII must be hashed before feature extraction" |
| Model documentation | Model Card | "Model degrades on inputs > 512 tokens" |
| Pipeline best practices | `AGENTS.md` | "Run distribution check before retraining" |
| ML framework gotchas | `TOOLS.md` | "PyTorch DataLoader workers leak memory on macOS" |
| Research communication | `SOUL.md` | "Report confidence intervals, not just point estimates" |

### Inter-Session Communication

OpenClaw provides tools to share learnings across sessions:

- **sessions_list** — View active/recent sessions
- **sessions_history** — Read another session's transcript
- **sessions_send** — Send a learning to another session
- **sessions_spawn** — Spawn a sub-agent for background work

Use these only in trusted environments and only when the user explicitly wants cross-session sharing. Prefer sending summary statistics and methodology notes, not raw datasets or credentials.

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-science
openclaw hooks enable self-improving-science
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in the project or workspace root:

```bash
mkdir -p .learnings
```

Create the files inline using the headers shown above. Avoid reading templates from the current repo or workspace unless you explicitly trust that path.

### Add reference to agent files to remind yourself to log learnings

#### Self-Improvement Workflow (Science)

When experiment issues or methodology corrections occur:
1. Log to `.learnings/EXPERIMENT_ISSUES.md`, `LEARNINGS.md`, or `FEATURE_REQUESTS.md`
2. Review and promote broadly applicable learnings to:
   - Experiment checklists — pre-run validation steps
   - Model cards — known limitations, performance bounds
   - Data governance docs — handling rules, quality gates
   - `CLAUDE.md` or `AGENTS.md` — project-level conventions

## Logging Format

### Learning Entry

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: data_collection | preprocessing | analysis | modeling | validation | publication

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct.
Include relevant metrics, sample sizes, or statistical values.

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: experiment | peer_review | user_feedback | analysis
- Related Files: path/to/notebook.ipynb, path/to/data.csv
- Tags: tag1, tag2
- See Also: LRN-20260101-001 (if related to existing entry)
- Dataset: dataset_name (optional)
- Model: model_name_or_version (optional)
- Metric-Before: 0.85 (optional)
- Metric-After: 0.91 (optional)
- Pattern-Key: leakage.timestamp | stats.normality_assumption (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2026-01-15 (optional)
- Last-Seen: 2026-01-15 (optional)

---
```

### Experiment Issue Entry

Append to `.learnings/EXPERIMENT_ISSUES.md`:

```markdown
## [EXP-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: data_collection | preprocessing | analysis | modeling | validation | publication

### Summary
Brief description of what failed or went wrong

### Error
```
Actual error message, unexpected metric, or reproducibility delta
```

### Context
- Experiment/notebook attempted
- Dataset and split used
- Model architecture and hyperparameters (if relevant)
- Hardware/environment details
- Summary of relevant output (avoid full data dumps)

### Root Cause
If identifiable, what caused the issue

### Suggested Fix
How to prevent or resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/notebook.ipynb
- Seeds Tested: 42, 123, 7 (if reproducibility issue)
- See Also: EXP-20260101-001 (if recurring)

---
```

### Feature Request Entry

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: data_collection | preprocessing | analysis | modeling | validation | publication

### Requested Capability
What the user wanted to do

### Research Context
Why they need it — what experiment, analysis, or pipeline step it supports

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what libraries or tools it might use

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_pipeline_step

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `EXP` (experiment issue), `FEAT` (feature request)
- YYYYMMDD: Current date
- XXX: Sequential number or random 3 chars (e.g., `001`, `A7B`)

Examples: `LRN-20260412-001`, `EXP-20260412-A3F`, `FEAT-20260412-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2026-04-13T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Experiment-Run**: run_id_or_notebook_version
- **Notes**: Brief description of what was done
```

Other status values:
- `in_progress` — Actively being investigated
- `wont_fix` — Decided not to address (add reason in Resolution notes)
- `promoted` — Elevated to experiment checklist, model card, or methodology standard
- `promoted_to_skill` — Extracted as a reusable skill

## Promoting to Research Artifacts

When a learning is broadly applicable (not a one-off fix), promote it to permanent research memory.

### When to Promote

- Learning applies across multiple experiments or datasets
- Knowledge any researcher (human or AI) working on this project should know
- Prevents recurring methodology mistakes
- Documents data constraints or model limitations

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Experiment Checklist | Pre-run validation: data checks, split verification, seed logging |
| Model Card | Known limitations, performance bounds, failure modes, training data description |
| Data Governance Docs | PII handling, data quality gates, provenance requirements |
| Methodology Standards | Statistical test selection, sample size requirements, reporting conventions |
| `CLAUDE.md` / `AGENTS.md` | Project-level facts, pipeline conventions, automation rules |
| `TOOLS.md` | ML framework gotchas, library version constraints (OpenClaw) |
| `SOUL.md` | Research communication style, rigor principles (OpenClaw) |

### How to Promote

1. **Distill** the learning into a concise rule or checklist item
2. **Add** to appropriate section in target document (create if needed)
3. **Update** original entry:
   - Change `**Status**: pending` → `**Status**: promoted`
   - Add `**Promoted**: experiment-checklist.md` (or target doc)

### Promotion Examples

**Learning** (verbose):
> Used t-test on highly skewed revenue data. User pointed out normality
> assumption was violated. Switched to Mann-Whitney U test. P-value changed
> from 0.03 to 0.12 — original conclusion was invalid.

**In Methodology Standards** (concise):
```markdown
## Statistical Test Selection
- Check normality (Shapiro-Wilk) before parametric tests
- Skewed data → use non-parametric alternatives (Mann-Whitney U, Kruskal-Wallis)
- Report both test choice rationale and assumption checks
```

**Learning** (verbose):
> Timestamp feature in training data was leaking the target. Model had 0.99
> AUC in validation but 0.52 in production. The timestamp encoded when the
> label was assigned, not when the event occurred.

**In Experiment Checklist** (actionable):
```markdown
## Pre-Training Checks
- [ ] Verify no temporal leakage: features must predate the label event
- [ ] Check feature-target correlation for suspiciously high values (>0.95)
- [ ] Validate that train/test split respects time ordering if data is temporal
```

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: EXP-20260101-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**: Recurring issues often indicate:
   - Missing experiment checklist item (→ promote to checklist)
   - Missing data validation step (→ add to pipeline)
   - Architectural problem (→ create tech debt ticket)

## Detection Triggers

Automatically log when you notice:

**Data Quality Issues** (→ experiment issue with `data_quality`):
- Data leakage between train and test sets
- Feature-target correlation > 0.95
- Missing data patterns (MNAR, MAR, MCAR) not accounted for
- Distribution shift between training and serving data
- Class imbalance not addressed
- Duplicate records in dataset

**Statistical Errors** (→ learning with `statistical_error`):
- P-value reported without effect size
- Multiple comparisons without correction (Bonferroni, FDR)
- Parametric test on non-normal data
- Confidence interval misinterpreted
- Sample size too small for chosen test
- P-hacking signals: many tested hypotheses, only significant ones reported

**Methodology Flaws** (→ learning with `methodology_flaw`):
- No holdout set for hyperparameter tuning
- Validation set used for both tuning and evaluation
- Feature engineering on full dataset before splitting
- Cross-validation leaking preprocessing steps
- Evaluation metric misaligned with business objective

**Reproducibility Issues** (→ experiment issue with `reproducibility_issue`):
- Different results across random seeds
- Results differ between local and cloud environments
- Notebook cells executed out of order
- Missing dependency versions in requirements
- GPU non-determinism not documented

**Hypothesis Revisions** (→ learning with `hypothesis_revision`):
- Hypothesis test fails to reject null
- Effect size smaller than expected
- Confounding variable discovered
- Causal assumption violated

**Model/Training Errors** (→ experiment issue):
- NaN loss during training
- Gradient explosion or vanishing
- CUDA out of memory
- Shape mismatch in tensors
- Model accuracy degradation after data update
- Convergence failure

**Feature Requests** (→ feature request):
- "Can you add automated leakage detection?"
- "I need a data drift monitoring pipeline"
- "Is there a way to version datasets?"
- "Why can't we do A/B test analysis here?"

## Priority Guidelines

| Priority | When to Use | Example |
|----------|-------------|---------|
| `critical` | Data leakage in production model, results published with error | Target leakage shipped to production scoring |
| `high` | Irreproducible published result, major statistical error | T-test on non-normal data changing conclusion |
| `medium` | Methodology improvement, better experiment design | Adding stratified splitting to pipeline |
| `low` | Documentation of approach, minor analysis note | Noting which random seed was used |

## Area Tags

Use to filter learnings by research phase:

| Area | Scope |
|------|-------|
| `data_collection` | Surveys, scraping, APIs, sensor data, database queries |
| `preprocessing` | Cleaning, imputation, encoding, normalization, feature engineering |
| `analysis` | EDA, statistical tests, hypothesis testing, visualization |
| `modeling` | Model selection, training, hyperparameter tuning, architecture |
| `validation` | Cross-validation, holdout testing, A/B tests, model evaluation |
| `publication` | Reports, papers, model cards, dashboards, presentations |

## Best Practices

1. **Log immediately** — context and metric values are freshest right after the issue
2. **Include metrics** — always note before/after values, sample sizes, p-values
3. **Record seeds and versions** — library versions, random seeds, GPU type
4. **Link notebooks** — reference the exact notebook and cell where the issue occurred
5. **Suggest concrete fixes** — not just "investigate further"
6. **Use consistent categories** — enables filtering by issue type
7. **Promote aggressively** — if a mistake could recur, add to experiment checklist
8. **Review before experiments** — check past learnings for the dataset/method you're about to use

## Gitignore Options

**Keep learnings local** (per-researcher):
```gitignore
.learnings/
```

This repo uses that default to avoid committing sensitive data or noisy local logs.

**Track learnings in repo** (team-wide):
Don't add to .gitignore — learnings become shared research knowledge.

**Hybrid** (track templates, ignore entries):
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Hook Integration

Enable automatic reminders through agent hooks. This is **opt-in** — you must explicitly configure hooks.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-science/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a science-specific learning evaluation reminder after each prompt (~60-120 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-science/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-science/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if you want error-pattern reminders from ML training output and data pipeline commands.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate experiment learnings |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Triggers on ML/data errors |

See `references/hooks-setup.md` for detailed configuration and troubleshooting.

## Automatic Skill Extraction

When a learning is valuable enough to become a reusable skill, extract it:

```bash
./skills/self-improving-science/scripts/extract-skill.sh skill-name --dry-run
./skills/self-improving-science/scripts/extract-skill.sh skill-name
```

**Extraction criteria** — any of: recurring (2+ See Also links), verified (resolved status), non-obvious (required investigation), broadly applicable, or user-flagged.

After extraction: set status to `promoted_to_skill`, add `Skill-Path`, verify in fresh session.

## Periodic Review

Review `.learnings/` before new experiments, after training runs, and before publication.

```bash
grep -h "Status\*\*: pending" .learnings/*.md | wc -l
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["
```

## Multi-Agent Support

| Agent | Activation | Setup |
|-------|-----------|-------|
| Claude Code / Codex | Hooks (UserPromptSubmit, PostToolUse) | `.claude/settings.json` |
| GitHub Copilot | Manual | `.github/copilot-instructions.md` |
| OpenClaw | Workspace injection | See OpenClaw Setup above |

Apply self-improvement when you: discover data leakage, get irreproducible results, misapply a statistical test, find methodology flaws, hit training errors, or learn dataset quirks.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/science/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: science
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (science)
Only trigger this skill automatically for science signals such as:
- `experiment|hypothesis|p-value|confidence interval|reproducibility`
- `dataset shift|data leakage|methodology flaw|benchmark drift`
- explicit science intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/science/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
