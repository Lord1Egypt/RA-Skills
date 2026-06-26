# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-ai skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Multi-agent coordination, model routing
│   ├── SOUL.md                 # Model behavior guidelines, personality
│   ├── TOOLS.md                # Model/tool configuration, parameters
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-ai/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-ai/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-ai
```

Or copy manually:

```bash
cp -r self-improving-ai ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-ai
openclaw hooks enable self-improving-ai
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (AI-Specific)

When AI/model learnings prove broadly applicable, promote them to workspace files:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Model behavior patterns | `SOUL.md` | "Claude 4 tends to over-qualify, use direct prompting" |
| Model selection and routing | `AGENTS.md` | "Use fast model for triage, capable model for code gen" |
| Model/tool configuration | `TOOLS.md` | "Set temperature 0.1 for code, 0.7 for creative" |
| Model selection insights | Model selection matrix | "Sonnet for code gen, Opus for complex reasoning" |
| Prompt patterns | Prompt library | "Chain-of-thought improves code quality by 35%" |
| Fine-tuning lessons | Fine-tuning runbook | "Always include replay data to prevent forgetting" |
| RAG improvements | RAG architecture doc | "Chunk by content type, not fixed token size" |
| Inference optimizations | Performance tuning guide | "Cache system prompts, batch similar requests" |
| Evaluation findings | Benchmark suite docs | "HumanEval + internal eval for code gen models" |
| Guardrail tuning | Guardrail policy doc | "Lower toxicity threshold for customer-facing" |

### Promotion Decision Tree

```
Is it about which model to use?
├── Yes → Model selection matrix
└── No → Is it about how to prompt?
    ├── Yes → Prompt library
    └── No → Is it about model behavior/personality?
        ├── Yes → SOUL.md
        └── No → Is it about model workflow/routing?
            ├── Yes → AGENTS.md
            └── No → Is it about model configuration?
                ├── Yes → TOOLS.md
                └── No → Is it about fine-tuning?
                    ├── Yes → Fine-tuning runbook
                    └── No → Is it about RAG?
                        ├── Yes → RAG architecture doc
                        └── No → Is it about evaluation?
                            ├── Yes → Benchmark suite
                            └── No → Keep in .learnings/
```

## AI-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Model quality dropped after update | Log model issue | MODEL_ISSUES.md |
| Inference latency spike | Log model issue | MODEL_ISSUES.md |
| RAG retrieval returned irrelevant chunks | Log model issue | MODEL_ISSUES.md |
| Embedding quality degraded | Log model issue | MODEL_ISSUES.md |
| Multimodal input failed | Log model issue | MODEL_ISSUES.md |
| Guardrail misfire | Log model issue | MODEL_ISSUES.md |
| Better model discovered for a task | Log learning | LEARNINGS.md (model_selection) |
| Prompt pattern improved output | Log learning | LEARNINGS.md (prompt_optimization) |
| Hallucination detected | Log learning | LEARNINGS.md (hallucination_rate) |
| Context window overflow | Log learning | LEARNINGS.md (context_management) |
| Fine-tuned model regressed on eval | Log learning | LEARNINGS.md (fine_tune_regression) |
| Token cost exceeded budget | Log learning | LEARNINGS.md (cost_efficiency) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share an AI/model insight with another session:
```
sessions_send(sessionKey="session-id", message="Model insight: Claude Sonnet 23% better than GPT-4o on multi-file edits, 40% cheaper")
```

### sessions_spawn

Spawn a background agent to analyze model performance patterns:
```
sessions_spawn(task="Analyze .learnings/MODEL_ISSUES.md for recurring model failures and promotion candidates", label="model-review")
```

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Verification

```bash
openclaw hooks list        # Check hook is registered
openclaw status            # Check skill is loaded
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
