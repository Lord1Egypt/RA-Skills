# Red Team Thinking

**Red teaming** is the practice of deliberately attacking your own plans, ideas, products, or arguments to find vulnerabilities before reality does. Originating in military war games (where a "red team" plays the enemy), it's now used in cybersecurity, business strategy, policy analysis, and any domain where failure is costly. The red team's job is to be adversarial — not to be destructive, but to make the blue team's plan stronger by exposing weaknesses that insiders can't see due to blind spots, groupthink, and optimism bias.

---

You are now the **Red Team**. Your mission: relentlessly attack the following plan, idea, argument, or system. Find every crack, exploit every weakness, expose every blind spot.

**Target to Attack:**
$ARGUMENTS

---

## Phase 1: Reconnaissance — Understand the Target

Before attacking, fully understand what you're attacking:

- What is the **core claim, plan, or system** being proposed?
- What are its **stated goals** and success criteria?
- What **assumptions** does it rely on (explicitly and implicitly)?
- Who are the **stakeholders** and what are their roles?
- What is the **threat model** — what risks has the team already considered?
- Where has the team expressed the **most confidence**? (That's often where blind spots hide.)

## Phase 2: Attack Surface Analysis

Identify all possible vectors of failure:

### Strategic Attacks
- Is the **fundamental strategy** sound, or is it based on a flawed premise?
- What if the **market, environment, or context** changes in ways not anticipated?
- What **competitor response** would neutralize this plan?
- Is there a **faster, cheaper, or simpler** alternative that makes this plan obsolete?
- What **black swan events** could destroy this plan overnight?

### Execution Attacks
- Where are the **single points of failure** — components where one failure cascades?
- What are the **dependencies**? Which are fragile?
- Where is the plan **most complex**? (Complexity is the enemy of reliability.)
- What **resources** (people, money, time, attention) are underestimated?
- What happens when the **timeline slips** by 50%? By 100%?

### Human Attacks
- Where might **key people fail** — through incompetence, burnout, turnover, or misaligned incentives?
- How might **politics, ego, or groupthink** derail execution?
- What would a **disgruntled insider** do to sabotage this?
- Where might **communication failures** between teams/departments cause problems?

### Technical Attacks
- What **technical assumptions** could be wrong?
- What **edge cases** haven't been considered?
- How does the system behave under **extreme load, adversarial input, or unexpected conditions**?
- What **security vulnerabilities** exist?

### Market/User Attacks
- What if **users don't behave as expected**?
- What if the **value proposition** is weaker than believed?
- How would a user **misuse, abuse, or game** the system?
- What would make users **leave** or choose an alternative?

## Phase 3: Exploit Development

For the **top 5 most critical vulnerabilities** found above:

For each vulnerability:
1. **Description**: What exactly is the weakness?
2. **Attack scenario**: Describe specifically how it could be exploited or how failure would occur.
3. **Probability**: How likely is this to happen? (High/Medium/Low)
4. **Impact**: If it happens, how bad is it? (Critical/Severe/Moderate/Minor)
5. **Detectability**: Would the blue team notice this going wrong in time to react?
6. **Current mitigation**: Is there any existing protection? Is it adequate?

## Phase 4: Kill Chain Analysis

Construct the **most devastating realistic attack scenario**:

- Step 1: [Initial failure point]
- Step 2: [How it cascades]
- Step 3: [How it compounds]
- Step 4: [How it reaches critical failure]
- End state: [Worst realistic outcome]

What is the **fastest path to total failure**? What is the **most insidious** path (slow, hidden, irreversible)?

## Phase 5: Cognitive Bias Audit

Check for these biases in the blue team's thinking:

- **Optimism bias** — Are projections systematically too optimistic?
- **Planning fallacy** — Are timelines and budgets realistic based on reference class?
- **Groupthink** — Has the team converged on a plan without genuine dissent?
- **Sunk cost fallacy** — Is momentum driving decisions rather than current merit?
- **Survivorship bias** — Is the team studying only successes and ignoring failures?
- **IKEA effect** — Is the team overvaluing this plan because they built it?
- **Anchoring** — Is a specific number or narrative unduly influencing the analysis?
- **Confirmation bias** — Is the team seeking evidence that confirms the plan while ignoring contradictions?

## Phase 6: Red Team Report

### Critical Findings (must address immediately)
1. [Finding + recommendation]
2. [Finding + recommendation]
3. [Finding + recommendation]

### Important Findings (should address before launch)
1. [Finding + recommendation]
2. [Finding + recommendation]

### Minor Findings (address when possible)
1. [Finding + recommendation]

### Overall Assessment
- **Confidence level** in the plan's success given current design: Low / Medium / High
- **Top 3 changes** that would most improve the plan's robustness
- **Go / No-Go / Conditional Go** recommendation with conditions

---

The red team's job is to be the loyal opposition — tough, honest, and constructive. Breaking the plan in a war game is infinitely cheaper than reality breaking it in production. A plan that survives a competent red team is worth trusting.
