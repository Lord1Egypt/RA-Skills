---
name: reason
description: Logical reasoning and decision analysis system for clear thinking. Use when user mentions decisions, logic, reasoning, critical thinking, arguments, or problem analysis. Structures decisions with frameworks, evaluates arguments for validity, identifies logical fallacies, analyzes problems systematically, and guides clear thinking. Improves decision quality through structured reasoning.
---

# Reason

Reasoning system. Think clearly, decide wisely.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All reasoning data stored locally only**: `memory/reason/`
- **Personal decisions** remain private
- **No external analysis** tools connected
- **Decision frameworks** customized locally
- User controls all data retention and deletion

### Data Structure
Reasoning data stored locally:
- `memory/reason/decisions.json` - Decision analyses
- `memory/reason/frameworks.json` - Reasoning frameworks
- `memory/reason/arguments.json` - Argument evaluations
- `memory/reason/fallacies.json` - Fallacy detection log

## Core Workflows

### Analyze Decision
```
User: "Should I take the new job offer?"
→ Use scripts/analyze_decision.py --decision "job-offer" --factors "salary,location,growth"
→ Structure decision with pros/cons, weighted factors, trade-off analysis
```

### Evaluate Argument
```
User: "Evaluate this argument for validity"
→ Use scripts/evaluate_argument.py --argument "..." --check-logic --check-evidence
→ Assess premises, reasoning, evidence, and identify weaknesses
```

### Identify Fallacy
```
User: "What fallacy is in this reasoning?"
→ Use scripts/identify_fallacy.py --statement "..."
→ Detect logical fallacies, explain why they are flawed
```

### Structure Problem
```
User: "Help me think through this complex problem"
→ Use scripts/structure_problem.py --problem "..." --approach systematic
→ Break problem into components, identify root causes, generate solutions
```

## Module Reference
- **Decision Frameworks**: See [references/decisions.md](references/decisions.md)
- **Logical Analysis**: See [references/logic.md](references/logic.md)
- **Argument Evaluation**: See [references/arguments.md](references/arguments.md)
- **Problem Structuring**: See [references/structuring.md](references/structuring.md)
- **Cognitive Biases**: See [references/biases.md](references/biases.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `analyze_decision.py` | Structure decision analysis |
| `evaluate_argument.py` | Evaluate argument validity |
| `identify_fallacy.py` | Identify logical fallacies |
| `structure_problem.py` | Structure complex problems |
| `check_bias.py` | Check for cognitive biases |
| `build_framework.py` | Create decision frameworks |
