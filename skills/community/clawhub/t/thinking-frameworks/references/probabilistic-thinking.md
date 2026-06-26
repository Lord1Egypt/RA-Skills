# Probabilistic Thinking

**Probabilistic thinking** replaces the false certainty of "will this work?" with the honest question "what are the odds, and what's the expected value?" It embraces uncertainty as fundamental, not as a failure of analysis. Used by the best poker players, investors, military strategists, and forecasters (like Superforecasters in Philip Tetlock's research), it separates the quality of a decision from the quality of its outcome — because even good decisions can have bad outcomes, and vice versa.

---

Analyze the following problem using **probabilistic thinking**. Quantify uncertainty, compute expected values, and make decisions that are robust under uncertainty.

**Problem / Topic:**
$ARGUMENTS

---

## Step 1: Define the Decision and Possible Outcomes

- What is the **decision** to be made?
- What are the **possible outcomes**? List them exhaustively:
  - Best case
  - Likely case(s)
  - Worst case
  - Black swan / tail risk scenarios
- Are there **binary outcomes** (yes/no) or a **distribution** of possibilities?
- What is the **time horizon** for these outcomes?

## Step 2: Estimate Probabilities

For each outcome, estimate the probability:

- Use **reference classes**: How often does this type of thing happen historically?
- Use **base rates**: What is the general frequency before considering specifics?
- Use **decomposition**: Break the event into sub-events and estimate each.
  - P(A and B) = P(A) × P(B|A) — for dependent events
  - P(A or B) = P(A) + P(B) - P(A and B) — for overlapping events
- **Calibrate** your estimates:
  - If you say 90% confident, are you right 9 out of 10 times?
  - Most people are overconfident. Widen your ranges.
  - Use the "surprise index": if the opposite happened, how surprised would you be?
- Present probabilities explicitly:
  - Outcome A: __% probability
  - Outcome B: __% probability
  - Outcome C: __% probability
  - (Must sum to ~100%)

## Step 3: Assess Payoffs and Costs

For each outcome:

| Outcome | Probability | Payoff (if good) | Cost (if bad) | Notes |
|---|---|---|---|---|
| A | | | | |
| B | | | | |
| C | | | | |

- Quantify payoffs and costs in concrete terms (dollars, time, reputation, opportunity).
- Consider **asymmetry**: Is the upside/downside symmetric?
  - **Positive asymmetry** (limited downside, unlimited upside) → favor action
  - **Negative asymmetry** (limited upside, unlimited downside) → favor caution
- Are there any outcomes that are **existential/irreversible** (ruin risk)?

## Step 4: Compute Expected Value

**EV = Σ (Probability × Value) for all outcomes**

- Calculate the expected value of each option.
- Compare against the **expected value of inaction** (the default path also has an EV).
- Consider **risk-adjusted expected value**:
  - For decisions where you only get one shot (no retry), variance matters as much as EV.
  - A high-EV gamble with high variance may be worse than a lower-EV option with lower variance.
  - Kelly Criterion: never bet more than the edge/odds ratio.

## Step 5: Consider the Distribution, Not Just the Average

- What does the **full distribution** of outcomes look like?
  - Thin-tailed (normal distribution) → Average is informative
  - Fat-tailed (power law, Pareto) → Extremes dominate, average is misleading
- What is the **median** outcome? (Often more informative than the mean)
- What are the **tail risks** — low-probability, high-impact scenarios?
- Apply the **barbell strategy** where appropriate:
  - Protect against catastrophic downside (insurance, hedging)
  - Expose to asymmetric upside (optionality, experiments)

## Step 6: Decision-Making Under Uncertainty

Apply the appropriate framework:

- **Maximize expected value** — When you have many tries and outcomes are not existential.
- **Minimax regret** — When you want to minimize the worst-case regret ("Which decision would I regret least if it went wrong?")
- **Maximin** — When protecting against the worst case is paramount (survival situations).
- **Value of information** — Would gathering more data significantly change the decision? Is the cost of gathering info less than the expected improvement in decision quality?
- **Reversibility test** — Is this decision easily reversible? If yes, lower the bar for action. If no, require higher confidence.
- **Optionality** — Does this decision preserve or eliminate future options? Prefer actions that keep options open.

## Step 7: Pre-Register Your Predictions

Before the outcome is known:

- State your **probability estimate** clearly.
- Define what **evidence would update** your estimate (and in which direction).
- Set **tripwires**: specific future observations that would trigger a change in strategy.
- Distinguish between **being wrong** (probability was poorly calibrated) and **bad luck** (probability was right, just got an unlikely outcome).

## Step 8: Recommendation

- What is the **probabilistically optimal decision**?
- What is the **confidence interval** around your recommendation?
- What are the **key uncertainties** that most affect the outcome?
- What **cheap experiments** could reduce uncertainty before committing?
- State explicitly: "I recommend X with approximately Y% confidence, primarily because Z. The biggest risk is W."

---

The core discipline: separate the **quality of the decision** from the **quality of the outcome**. A good decision can have a bad outcome (bad luck). A bad decision can have a good outcome (good luck). Over time, good decision-making dominates. Think in probabilities, decide with expected values, and review with calibration.
