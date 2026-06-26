# FSRS-5 Algorithm Reference
## (FSRS-6 compatible for daily scheduling)

Source: open-spaced-repetition project (Jarrett Ye et al.)
Paper: "A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling"

---

## Core Concepts

| Concept | Symbol | Description |
|---------|--------|-------------|
| **Stability** | S | Days until retrievability drops to 90%. If S=10, you have a 90% recall chance after 10 days. |
| **Difficulty** | D | Intrinsic card difficulty [1, 10]. Higher = harder to retain. |
| **Retrievability** | R | Probability of recall at time t given stability S. |
| **Desired Retention** | r | Target recall probability at review. Default: 0.9 (90%). |

---

## Forgetting Curve

```
R(t, S) = (1 + FACTOR * t / S) ^ DECAY
```

Constants:
- `DECAY = -0.5`
- `FACTOR = 19/81 ≈ 0.2346`  (chosen so that R(S, S) = 0.9 at default retention)

This is a power-law forgetting curve. When `t = S`, retrievability is ~90%.

---

## Interval Formula

To schedule the next review at a given desired retention `r`:

```
I(S, r) = S / FACTOR * (r ^ (1/DECAY) - 1)
        = S * 81/19 * (r^(-2) - 1)
```

At default `r = 0.9`: `I = S` (interval equals stability).
At `r = 0.85`: `I ≈ 1.64 * S` (longer interval for lower retention bar).
At `r = 0.95`: `I ≈ 0.46 * S` (shorter interval for higher retention bar).

---

## Default Parameters (FSRS-5, 21 weights)

```python
W = [
    0.4072, 1.1829, 3.1262, 15.4722,  # w[0-3]: init stability for Again/Hard/Good/Easy
    7.2102,                             # w[4]:   initial difficulty base
    0.5316, 1.0651,                     # w[5-6]: difficulty update coefficients
    0.0589,                             # w[7]:   mean reversion weight (alpha)
    1.5330, 0.1544,                     # w[8-9]: stability recall formula
    1.0071,                             # w[10]:  retrievability influence on recall
    1.9395, 0.1100, 0.2900, 2.2700,    # w[11-14]: forget stability formula
    0.1600, 2.9898,                     # w[15-16]: hard penalty, easy bonus
    0.5100, 0.3921, 0.2921, 0.1284,    # w[17-20]: auxiliary params
]
```

---

## State Transitions

### First Review (reps == 0): Initialize

```
S₀ = W[rating - 1]            # w[0]=Again, w[1]=Hard, w[2]=Good, w[3]=Easy
D₀ = W[4] - exp(W[5] * (rating - 1)) + 1   # clamped to [1, 10]
```

### Subsequent Reviews

**Retrievability at review time:**
```
R = (1 + FACTOR * days_since_last / S) ^ DECAY
```

**Difficulty update** (after every review):
```
ΔD = -W[6] * (rating - 3)
D_raw = D + ΔD * (10 - D) / 9           # scales delta by remaining headroom
D' = W[7] * D₀(Easy) + (1 - W[7]) * D_raw   # mean reversion toward Easy difficulty
D' = clamp(D', 1, 10)
```

**Stability update — recall (rating ≥ 2):**
```
hard_penalty = W[15] if rating == 2 else 1.0
easy_bonus   = W[16] if rating == 4 else 1.0

S' = S * (exp(W[8]) * (11 - D) * S^(-W[9]) * (exp(W[10] * (1 - R)) - 1)
         * hard_penalty * easy_bonus + 1)
```

**Stability update — lapse (rating == 1, Again):**
```
S' = W[11] * D^(-W[12]) * ((S + 1)^W[13] - 1) * exp(W[14] * (1 - R))
```

---

## Rating Scale

| Rating | Label | Meaning |
|--------|-------|---------|
| 1 | Again | Forgot entirely. Card is a lapse. |
| 2 | Hard | Recalled with serious difficulty. |
| 3 | Good | Correct recall with some effort. |
| 4 | Easy | Instant, effortless recall. |

---

## FSRS-6 vs FSRS-5

FSRS-6 (Nov 2024) adds a **short-term stability** (STS) model for same-day re-reviews
(e.g., learning steps in Anki). For daily scheduling (one review per card per day),
FSRS-5 and FSRS-6 behave identically. This implementation uses FSRS-5 formulas which
are FSRS-6 compatible for daily use.

Full FSRS-6 short-term formula (for completeness):
```
S_ST = W[17] * S^(-W[18]) * ((R + 1)^W[19] - 1) * exp(W[20] * (1 - R))
```
This only activates when elapsed time < 1 day.

---

## Key Properties

- **Difficulty is card-intrinsic**: Easy cards converge to low difficulty over time.
- **Stability grows multiplicatively**: Each successful review multiplies stability.
- **Lapses reset stability sharply**: Forgetting compresses stability back toward 1-3 days.
- **Desired retention trades off load**: Higher retention = shorter intervals = more reviews.

---

## Worked Example

Card: "Two Sum" | Difficulty: 5.5 | Stability: 8.2 | Days elapsed: 10

```
R = (1 + 0.2346 * 10 / 8.2) ^ (-0.5)
  = (1 + 0.2861)^(-0.5)
  = 1.2861^(-0.5)
  ≈ 0.882  (88.2% recall probability)

If rated Good (3):
  ΔD = -W[6] * (3 - 3) = 0  → difficulty unchanged
  S' = 8.2 * (exp(1.533) * (11 - 5.5) * 8.2^(-0.1544) * (exp(1.0071 * (1 - 0.882)) - 1) + 1)
     ≈ 8.2 * (4.63 * 5.5 * 0.726 * 0.125 + 1)
     ≈ 8.2 * (2.31 + 1)
     ≈ 27.1 days

Next interval: 27 days
```
