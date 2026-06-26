# Prompt Optimization Frameworks

## CRISPE Framework

| Element | Meaning | Example |
|---------|---------|---------|
| **C**apacity (Role) | What role does the AI play | "You are a senior frontend architect" |
| **R**equest (Task) | What specifically to do | "Help me design a component architecture" |
| **I**nsight (Context) | Relevant background info | "The project uses React + TypeScript, team of 3" |
| **S**tyle (Format) | Expected answer style | "Think like an engineer, give actionable plans" |
| **P**ersonality (Tone) | Answer personality | "Direct, no fluff, opinionated" |
| **E**xperiment (Variation) | Request multiple versions | "Give 2-3 options and compare pros/cons" |

---

## CO-STAR Framework

| Element | Meaning | When to Use |
|---------|---------|------------|
| **C**ontext | Provide background information | All questions benefit from this |
| **O**bjective | Clarify what the AI should do | Vague requests need anchoring |
| **S**tyle | Desired writing style | Content creation tasks |
| **T**one | Formal / casual / serious, etc. | When targeting different audiences |
| **A**udience | Who the answer is for | When depth needs customization |
| **R**esponse | List / table / code / essay, etc. | When structured output is needed |

---

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| **Vague request** | "Help me write a program" | Anchor language, functionality, input/output |
| **Too broad** | "Teach me programming" | Break into specific sub-topics, tackle one at a time |
| **Hidden assumption** | "How to increase conversion rate" | Expose the premise first: what's the current rate? Where's the bottleneck? |
| **Contradictory constraints** | "Be concise but comprehensive" | Clarify priority, choose one direction |
| **Missing role** | "What do you think of this plan" | From whose perspective? Tech? Product? CEO? |
| **No format specified** | "Tell me about X" | Table? Bullet list? Deep analysis? Quick summary? |
| **Over-constraining** | "Implement feature Y using framework X" | May block better solutions from being considered |
| **Assumed consensus** | "Follow best practices" | Whose best practices? Which community? Which version? |

---

## Identifying Consensus Answers

When a question is likely to produce consensus answers, it typically has these traits:

1. **Searchable** — If Google's first result answers it, the AI will give a similar answer
2. **Unconstrained** — Fewer constraints = answers converge on the "safe but mediocre" middle ground
3. **Premises unchallenged** — When premises aren't questioned, answers stay within the default framework
4. **Single perspective** — One angle of questioning = one angle of "standard answer"
5. **Single time horizon** — Only asks "what to do now", never "how does this look in 5 years" or "under what conditions does this fail"

### Techniques to Break Consensus

- Ask the AI to find the **weakest assumption** in its own answer
- Ask the AI to **make the strongest case for the opposite position**
- Add **specific scenario constraints** (time, budget, team size, tech stack)
- Require the answer to include **one counter-intuitive insight**
- Specify a **time horizon** ("Looking back from 3 years in the future")

---

## Dimension → Thinking Framework Mapping

Each dimension in the pool is backed by a concrete thinking framework, not just a label.
When generating paths in Stage 2, use the corresponding "Thinking Directive" to drive
content generation — not just the dimension name.

| Dimension | Core Framework | Thinking Directive |
|-----------|---------------|-------------------|
| `system` | Munger's Latticework | Think in reverse: what would make this fail? How do the parts interlock? |
| `interest` | Political Economy | Who profits? Who bears the cost? Where is information asymmetry? What behavior does the incentive structure drive? |
| `evolution` | Path Dependence | What was the previous form? What triggered the transition? What stage is this at now? |
| `structure` | Architecture/Systems Engineering | Where is the load-bearing wall? Which component is irreplaceable? Remove which one and it all collapses? |
| `risk-first` | Taleb's Antifragility | Where is the upside of volatility? What is the biggest single point of failure? Where does fragility hide in assumptions? |
| `counter-intuitive` | Popper's Falsification | What fact would most easily overturn this conclusion? Is the strongest consensus the most deserving of challenge? |
| `adversarial` | Game Theory / Debate | If I were the opponent, how would I attack this plan? Where is the Nash equilibrium? |
| `hidden-assumption` | Philosophical Analysis | How does the conclusion change when premises don't hold? Which premises have never been questioned? |
| `minimalist` | Occam's Razor | If you keep only one element, which one? Does it still hold when stripped to the bone? |
| `time-horizon` | Future Retrospection | Looking back from 3 years out, what matters most? Where do short-term and long-term optimal solutions conflict? |
| `role-reversal` | Empathy / Perspective Shift | If you were the other side / user / competitor, what's the most fatal problem you see? |
| `peer-compare` | Porter's Competitive Strategy | What 1-2 peers are most worth comparing against? What is the key differentiator? |
| `scale-effect` | Complex Systems | What qualitatively changes at 10x scale? What holds at small scale but collapses at scale? |

### Mandatory Auxiliary Dimensions (Anchors)

These are not selectable dimensions — they are **mandatory fields** on every path at Level ≥ 1:

| Anchor | Purpose | Content Requirement |
|--------|---------|-------------------|
| **Evolution Anchor** | Temporal positioning | Trajectory: where from → current stage → where heading. At least 3 time nodes. |
| **Peer Anchor** | Spatial reference | 1-2 most relevant peers + key differentiator. Not a list — a comparative positioning. |

---

## 5 Signals of a High-Quality Question

1. **Clear success criteria** — The user knows what counts as a "good" answer
2. **Constraints present** — Scope, style, depth, and audience are bounded
3. **Context provided** — The AI doesn't need to guess the background
4. **Output format specified** — It's clear what form the answer should take
5. **Room for exploration** — The AI is allowed to challenge assumptions and offer different perspectives
