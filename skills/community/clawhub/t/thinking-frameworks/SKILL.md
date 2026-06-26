# Skill: Thinking Frameworks

**Location:** `skills/thinking-frameworks/`

**Description:** 20 human thinking frameworks for deep analysis and decision-making. Adapted from Claude Code commands to OpenClaw skills.

## Triggers

Use these thinking frameworks when the user:
- Explicitly requests a thinking mode (e.g., "use critical thinking", "first principles analysis", "red team this")
- Asks for deep analysis of a problem, decision, or plan
- Uses command syntax: `/thinking <framework> <topic>` or `/<framework-name> <topic>`
- Needs structured reasoning for complex decisions

## Available Frameworks

| Framework | Trigger Keywords | Use When |
|-----------|-----------------|----------|
| critical-thinking | critical, critique, analyze assumptions | Questioning assumptions, evaluating evidence, detecting biases |
| first-principles | first principles, first principles thinking, elon musk approach | Strip away assumptions, rebuild from fundamental truths |
| systems-thinking | systems, system thinking, holistic, causal loops | Understanding interconnected systems, feedback loops, emergence |
| design-thinking | design thinking, empathize, prototype | User-centered problem solving, creative iteration |
| lateral-thinking | lateral, creative, outside the box | Breaking conventional patterns, finding novel solutions |
| six-thinking-hats | six hats, de bono, white/red/black/yellow/green/blue | Multi-perspective analysis, group decision framing |
| socratic-method | socratic, questioning, progressive questions | Deep exploration through guided questioning |
| bayesian-thinking | bayesian, update beliefs, prior, evidence | Probabilistic belief updating with new evidence |
| second-order-thinking | second order, "and then what", consequences | Long-term consequence chains, unintended effects |
| inversion-thinking | inversion, invert, reverse, how would this fail | Problem by flipping, finding failure modes |
| dialectical-thinking | dialectical, thesis antithesis synthesis, hegel | Resolving contradictions through synthesis |
| abductive-reasoning | abductive, best explanation, inference | Inferring the most likely explanation from observations |
| mental-models | mental models, munger, multidisciplinary | Cross-disciplinary framework application |
| red-team | red team, adversarial, attack plan | Finding weaknesses through adversarial analysis |
| steelman | steelman, steel man, strongest argument | Strengthening opposing views before countering |
| probabilistic-thinking | probabilistic, probability, uncertainty | Decision-making under uncertainty |
| analogical-reasoning | analogical, analogy, map from known | Learning from parallel domains through mapping |
| counterfactual-thinking | counterfactual, "what if", alternative history | Exploring alternative scenarios and outcomes |
| opportunity-cost | opportunity cost, trade-off, alternative forgone | Evaluating true costs including foregone alternatives |
| premortem | premortem, assume failure,事前验尸 | Proactive failure analysis before implementation |

## Usage

### Direct Command
```
/thinking critical-thinking Should we switch from REST to GraphQL?
/red-team Our plan to launch in 3 markets simultaneously
/premortem The new pricing model we're about to ship
```

### Natural Language
```
"Use first principles to analyze this problem: [problem]"
"Red team this plan for me: [plan]"
"Think about this using second-order thinking: [situation]"
```

## Implementation

1. Detect the requested framework from user input
2. Load the corresponding reference file from `references/`
3. Apply the framework's structured steps to the user's topic
4. Present analysis following the framework's methodology

## Notes

- Frameworks are complementary — combine when appropriate (e.g., critical-thinking + red-team)
- Default to concise output unless user requests depth
- These are thinking aids, not rigid formulas — adapt to context
- All frameworks are MIT licensed from the original thinking-skills repo
