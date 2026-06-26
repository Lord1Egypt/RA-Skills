# Structuring Frameworks

## MECE (Mutually Exclusive, Collectively Exhaustive)

### What It Is
A decomposition principle: every element belongs to exactly one category (ME) and all categories together cover the full scope (CE).

### How to Apply
1. Define the scope — what is being decomposed? ("Revenue sources" is different from "profit drivers")
2. Choose a cutting dimension — by customer segment, by geography, by product line, by value chain stage
3. Draft categories and test:
   - **ME test**: Can any item fall into two categories? If yes, redefine boundaries
   - **CE test**: Is anything missing? Name one plausible item — does it fit? If not, add a category or widen an existing one
4. Validate depth — each category should be roughly equal in weight. A category containing 80% of the answer paired with four containing 5% each is structurally MECE but analytically useless

### Common Cuts
- **Revenue**: By segment, geography, product, channel, customer type, contract type
- **Costs**: Fixed vs. variable, direct vs. indirect, by function, by activity
- **Market**: By end-use, by region, by price tier, by buyer type
- **Organization**: By function, by business unit, by process, by capability

### Quality Check
- No overlaps between categories at any level
- No gaps — a "catch-all" or "other" bucket exceeding 15% signals a structural problem
- Consistent cutting logic within each level (don't mix geography and product in the same tier)
- Maximum 3 levels deep for most analyses; 4+ levels signal over-decomposition

---

## Issue Trees

### What It Is
A hierarchical decomposition of a question into sub-questions, where answering all sub-questions answers the parent. The root is the governing question; leaves are testable hypotheses or data-gathering tasks.

### How to Build
1. State the root question as a yes/no or "what should we do" question
   - Good: "Should Client X enter the European cold chain market?"
   - Bad: "European cold chain market" (topic, not question)
2. Decompose into 3-5 Level 1 branches (must be MECE)
3. Each branch decomposes into 2-4 sub-questions
4. Stop when you reach questions that can be answered with a single analysis or data point

### Standard Issue Tree Patterns

**Go/No-Go Decision**:
```
Should we do X?
├── Is the market attractive?
│   ├── Is it large enough?
│   ├── Is it growing?
│   └── Is the competitive structure favorable?
├── Can we win?
│   ├── Do we have the required capabilities?
│   ├── Can we differentiate?
│   └── Can we achieve target economics?
└── Is it worth it?
    ├── What is the expected return?
    ├── What are the risks?
    └── What is the opportunity cost?
```

**Profitability Diagnosis**:
```
Why are profits declining?
├── Revenue problem?
│   ├── Volume decline?
│   └── Price/mix deterioration?
└── Cost problem?
    ├── Variable cost increase?
    └── Fixed cost increase?
```

**Growth Strategy**:
```
How should we grow?
├── Organic growth
│   ├── Expand existing customers
│   ├── Win new customers
│   └── Enter new segments
├── Inorganic growth
│   ├── Acquisitions
│   └── Partnerships/JVs
└── New business models
    ├── Adjacent products/services
    └── Platform/ecosystem play
```

### Quality Check
- Root question is precise and answerable
- Every branch is MECE with its siblings
- Answering all children fully answers the parent
- Leaf nodes are specific enough to assign as research tasks
- Tree is balanced — no branch has 8 children while another has 1

---

## Hypothesis-Driven Analysis

### What It Is
Start with a proposed answer (the hypothesis), then design analyses to prove or disprove it. This inverts the natural instinct to "gather data first, then conclude" — which wastes time on unfocused research.

### How to Apply
1. **Form the hypothesis**: State a complete, falsifiable answer to the governing question
   - Good: "Client X should enter the European cold chain market through acquisition of a mid-sized player because organic entry would take 5+ years and the market window is closing"
   - Bad: "The market looks interesting" (not falsifiable)
2. **Identify key assumptions**: What must be true for the hypothesis to hold? List 3-5 critical assumptions
3. **Design analyses**: For each assumption, define what data or analysis would confirm or refute it
4. **Execute and update**: Run the analyses. If an assumption fails, revise the hypothesis — don't force the data to fit
5. **Synthesize**: State whether the hypothesis is confirmed, modified, or rejected, with evidence

### The Hypothesis Stack
```
Governing hypothesis: "We should acquire Target X at up to €200M"
├── Assumption 1: Market will grow >5% CAGR → Analysis: Market sizing
├── Assumption 2: Target holds defensible position → Analysis: Competitive assessment
├── Assumption 3: Integration costs < €30M → Analysis: Operational DD
├── Assumption 4: Synergies exceed €15M/year → Analysis: Financial model
└── Assumption 5: No regulatory blockers → Analysis: Regulatory screening
```

### Quality Check
- Hypothesis is a complete sentence, not a topic
- Each assumption is independently testable
- You have actively looked for disconfirming evidence, not just confirming data
- You can articulate what would change your mind
