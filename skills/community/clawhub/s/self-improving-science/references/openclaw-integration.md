# OpenClaw Integration (Science)

Complete setup and usage guide for integrating the self-improving science skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Experiment orchestration, pipeline patterns
│   ├── SOUL.md                 # Research rigor principles, communication style
│   ├── TOOLS.md                # ML framework gotchas, data tool capabilities
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-science/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-science/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-science
```

Or copy manually:

```bash
cp -r self-improving-science ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

Copy the hook to OpenClaw's hooks directory:

```bash
mkdir -p .openclaw/hooks
cp -r hooks/openclaw .openclaw/hooks/self-improving-science
```


### 3. Create Learning Files

Create the `.learnings/` directory in your workspace:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Injected Prompt Files

### AGENTS.md (Science-Oriented)

Purpose: Experiment orchestration and ML pipeline patterns.

```markdown
# Experiment Orchestration

## Pipeline Rules
- Run data validation before any training step
- Log all hyperparameters and random seeds
- Use experiment tracking (MLflow, W&B) for all runs

## Delegation Rules
- Do not spawn sub-agents or read other sessions from this skill
- Log a redacted note in this workspace only
- Do not send cross-session messages
```

### SOUL.md (Science-Oriented)

Purpose: Research rigor and communication guidelines.

```markdown
# Research Principles

## Scientific Rigor
- Report confidence intervals, not just point estimates
- Distinguish correlation from causation
- Acknowledge limitations explicitly

## Scope

This skill does not read other sessions, send cross-session messages, spawn background agents, or read other installed skills. Log redacted notes in this workspace only.

## PyTorch
- DataLoader workers leak memory on macOS — use num_workers=0 for debugging
- torch.use_deterministic_algorithms(True) for reproducibility

## scikit-learn
- Pipeline must wrap preprocessing for proper CV
- StratifiedKFold for imbalanced classes

## pandas
- .copy() after slicing to avoid SettingWithCopyWarning
- Use .astype("category") for memory efficiency on categoricals
```

## Learning Workflow

### Capturing Learnings

1. **In-session**: Log to `.learnings/` as usual
2. **Cross-session**: Promote to workspace files or research artifacts

### Promotion Decision Tree

```
Is the learning project-specific?
├── Yes → Keep in .learnings/
└── No → Is it a methodology/statistics pattern?
    ├── Yes → Promote to Methodology Standards
    └── No → Is it about data handling?
        ├── Yes → Promote to Data Governance Docs
        └── No → Is it about model behavior?
            ├── Yes → Promote to Model Card
            └── No → Is it an ML tool gotcha?
                ├── Yes → Promote to TOOLS.md
                └── No → Promote to AGENTS.md (pipeline pattern)
```

### Promotion Format Examples

**From learning:**
> PyTorch DataLoader with num_workers > 0 causes memory leak on macOS during long training runs

**To TOOLS.md:**
```markdown
## PyTorch
- DataLoader num_workers > 0 leaks memory on macOS — set to 0 for debugging, or use persistent_workers=True
```

**From learning:**
> Model silently predicts majority class when class ratio exceeds 20:1

**To Model Card:**
```markdown
## Known Limitations
- Performance degrades when minority class ratio < 5% — use class weights or SMOTE
```

## Scope

This skill does not read other sessions, send cross-session messages, spawn background agents, or read other installed skills. Log redacted notes in this workspace only.

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Science-Specific Detection Triggers

| Trigger | Action |
|---------|--------|
| Data quality issue found | Log to `.learnings/EXPERIMENT_ISSUES.md` with `data_quality` |
| Methodology flaw | Log to `.learnings/LEARNINGS.md` with `methodology_flaw` |
| Statistical test misapplied | Log to `.learnings/LEARNINGS.md` with `statistical_error` |
| Model reproducibility failure | Log to `.learnings/EXPERIMENT_ISSUES.md` with `reproducibility_issue` |
| Hypothesis revision needed | Log to `.learnings/LEARNINGS.md` with `hypothesis_revision` |
| ML framework issue | Log to `TOOLS.md` with framework name |
| Pipeline pattern discovered | Log to `AGENTS.md` with pipeline step |

## Verification

Check hook is registered:

```bash
openclaw hooks list
```

Check skill is loaded:

```bash
openclaw status
```

## Troubleshooting

### Hook not firing

1. Ensure hooks enabled in config
2. Restart gateway after config changes
3. Check gateway logs for errors

### Learnings not persisting

1. Verify `.learnings/` directory exists
2. Check file permissions
3. Ensure workspace path is configured correctly

### Skill not loading

1. Check skill is in skills directory
2. Verify SKILL.md has correct frontmatter
3. Run `openclaw status` to see loaded skills
