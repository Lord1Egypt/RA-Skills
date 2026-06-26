# OpenClaw Integration

Complete setup and usage guide for integrating the self-improving-supply-chain skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Multi-agent coordination patterns
│   ├── SOUL.md                 # Behavioral guidelines and personality
│   ├── TOOLS.md                # Tool capabilities and gotchas
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-supply-chain/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-supply-chain/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-supply-chain
```

Or copy manually:

```bash
cp -r self-improving-supply-chain ~/.openclaw/skills/
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-supply-chain
openclaw hooks enable self-improving-supply-chain
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Promotion Targets (Supply Chain-Specific)

When supply chain learnings prove broadly applicable, promote them to operational standards:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Supplier performance patterns | Supplier scorecards | "Require dual-source for components >$50K annual spend" |
| Inventory buffer patterns | Safety stock policies | "Ocean-freight SKUs carry 3 weeks safety stock" |
| Routing optimizations | Routing playbooks | "Divert to Nansha port when Yantian queue >5 days" |
| Forecast accuracy patterns | Demand planning models | "Apply seasonal index for gift-category SKUs in Q4" |
| Quality failure patterns | Quality acceptance criteria | "Inspect 100% of first shipment from new suppliers" |
| Workflow improvements | `AGENTS.md` | "Run inventory reconciliation before reorder point calc" |

### Promotion Decision Tree

```
Is the learning project-specific?
├── Yes → Keep in .learnings/
└── No → Is it a supplier performance pattern?
    ├── Yes → Promote to supplier scorecard
    └── No → Is it an inventory/stock pattern?
        ├── Yes → Promote to safety stock policy
        └── No → Is it a logistics/routing pattern?
            ├── Yes → Promote to routing playbook
            └── No → Is it a forecast/demand pattern?
                ├── Yes → Promote to demand planning model
                └── No → Promote to TOOLS.md or AGENTS.md
```

## Supply Chain-Specific Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Stockout or backorder event | Log supply chain issue | SUPPLY_CHAIN_ISSUES.md (inventory_mismatch) |
| Delivery SLA miss | Log supply chain issue | SUPPLY_CHAIN_ISSUES.md (logistics_delay) |
| Quality rejection spike | Log supply chain issue | SUPPLY_CHAIN_ISSUES.md (quality_deviation) |
| Supplier lead time increase | Log learning | LEARNINGS.md (supplier_risk) |
| Forecast MAPE >15% | Log learning | LEARNINGS.md (forecast_error) |
| Demand signal shift | Log learning | LEARNINGS.md (demand_signal_shift) |
| Warehouse capacity >90% | Log supply chain issue | SUPPLY_CHAIN_ISSUES.md (inventory_mismatch) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a supply chain insight with another session:
```
sessions_send(sessionKey="session-id", message="Supplier risk: SMT-4421 lead time increased 75%, begin alternate qualification immediately")
```

### sessions_spawn

Spawn a background agent to analyze supply chain patterns:
```
sessions_spawn(task="Analyze .learnings/SUPPLY_CHAIN_ISSUES.md for recurring delay patterns and promotion candidates", label="scm-review")
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
