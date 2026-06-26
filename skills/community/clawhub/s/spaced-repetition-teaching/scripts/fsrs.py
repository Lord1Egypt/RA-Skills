#!/usr/bin/env python3
"""
fsrs.py — FSRS-5 core algorithm (FSRS-6 compatible for daily scheduling)

Free Spaced Repetition Scheduler by Jarrett Ye et al.
Reference: open-spaced-repetition/py-fsrs

No external dependencies. Pure Python 3.6+.

Rating scale:
    1 = Again  (forgot)
    2 = Hard   (recalled with serious difficulty)
    3 = Good   (recalled with effort)
    4 = Easy   (instant recall)
"""

import math
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

# ---------------------------------------------------------------------------
# Algorithm constants
# ---------------------------------------------------------------------------

DECAY = -0.5
# FACTOR is chosen so that R(S, S) = 0.9 (at default desired retention)
# FACTOR = desired_retention^(1/DECAY) - 1 = 0.9^(-2) - 1 = 19/81
FACTOR = 19.0 / 81.0  # ≈ 0.2346

# FSRS-5 default weights (21 parameters)
# These encode the average learner's memory dynamics; can be personalized
# via the open-spaced-repetition optimizer on your own review history.
DEFAULT_W = [
    0.4072, 1.1829, 3.1262, 15.4722,   # w[0-3]:  initial stability by rating (Again/Hard/Good/Easy)
    7.2102,                              # w[4]:    initial difficulty base
    0.5316, 1.0651,                      # w[5-6]:  difficulty update: decay rate, scaling
    0.0589,                              # w[7]:    mean reversion weight (alpha)
    1.5330, 0.1544,                      # w[8-9]:  recall stability: exp coeff, stability exponent
    1.0071,                              # w[10]:   retrievability influence on recall stability
    1.9395, 0.1100, 0.2900, 2.2700,     # w[11-14]: forget stability formula
    0.1600, 2.9898,                      # w[15-16]: hard penalty, easy bonus on recall stability
    0.5100, 0.3921, 0.2921, 0.1284,     # w[17-20]: auxiliary parameters
]

# ---------------------------------------------------------------------------
# Card state
# ---------------------------------------------------------------------------

@dataclass
class FSRSState:
    """Mutable per-card scheduling state."""
    difficulty: float = 5.0    # [1, 10] — card intrinsic difficulty
    stability: float = 1.0     # days until R drops to ~90%
    reps: int = 0              # total review count (including lapses)
    lapses: int = 0            # times forgotten (Again)
    last_review: Optional[date] = None
    next_review: Optional[date] = None

    def to_dict(self) -> dict:
        return {
            "difficulty": round(self.difficulty, 4),
            "stability": round(self.stability, 4),
            "reps": self.reps,
            "lapses": self.lapses,
            "last_review": self.last_review.isoformat() if self.last_review else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "FSRSState":
        s = cls(
            difficulty=float(d.get("difficulty", 5.0)),
            stability=float(d.get("stability", 1.0)),
            reps=int(d.get("reps", 0)),
            lapses=int(d.get("lapses", 0)),
        )
        lr = d.get("last_review")
        nr = d.get("next_review")
        s.last_review = date.fromisoformat(lr) if lr else None
        s.next_review = date.fromisoformat(nr) if nr else None
        return s

# ---------------------------------------------------------------------------
# Core FSRS-5 formulas
# ---------------------------------------------------------------------------

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def initial_stability(rating: int, w: list = DEFAULT_W) -> float:
    """
    First-review stability, based on grade.
    Maps rating 1-4 to w[0]-w[3]: [0.4, 1.2, 3.1, 15.5] days approximately.
    """
    assert 1 <= rating <= 4
    return w[rating - 1]


def initial_difficulty(rating: int, w: list = DEFAULT_W) -> float:
    """
    First-review difficulty, based on grade. Range [1, 10].
    Again → high difficulty (~8.5), Easy → low difficulty (~1.7).
    """
    assert 1 <= rating <= 4
    d = w[4] - math.exp(w[5] * (rating - 1)) + 1
    return _clamp(d, 1.0, 10.0)


def retrievability(stability: float, days_elapsed: float) -> float:
    """
    Probability of recall after `days_elapsed` days given `stability`.

    Formula: R = (1 + FACTOR * t/S) ^ DECAY

    Properties:
    - R(0) = 1.0 (perfect recall right after review)
    - R(S) ≈ 0.9 at default desired retention
    - Monotonically decreasing with time
    """
    if days_elapsed <= 0:
        return 1.0
    return (1.0 + FACTOR * days_elapsed / stability) ** DECAY


def next_interval(stability: float, desired_retention: float = 0.9) -> int:
    """
    Next review interval in days to achieve `desired_retention` at review time.

    Derived by inverting the forgetting curve:
        I = S / FACTOR * (r^(1/DECAY) - 1)

    At r=0.9 (default): I = S (interval equals stability).
    At r=0.85: I ≈ 1.64 * S (lower bar → longer interval).
    At r=0.95: I ≈ 0.46 * S (higher bar → shorter interval).
    """
    assert 0.0 < desired_retention < 1.0
    interval = stability / FACTOR * (desired_retention ** (1.0 / DECAY) - 1.0)
    return max(1, round(interval))


def update_difficulty(d: float, rating: int, w: list = DEFAULT_W) -> float:
    """
    Update card difficulty after a review.

    Two-part update:
    1. Shift by ΔD = -w[6]*(rating-3), scaled by headroom from 10.
       - Easy (4): decreases difficulty
       - Good (3): no change
       - Hard (2): increases difficulty
       - Again (1): increases difficulty most
    2. Mean reversion toward the Easy-grade initial difficulty (prevents drift).
    """
    d0_easy = initial_difficulty(4, w)
    delta_d = -w[6] * (rating - 3)
    d_raw = d + delta_d * (10.0 - d) / 9.0
    # Mean reversion: pull toward initial difficulty at "Easy" rating
    d_new = w[7] * d0_easy + (1.0 - w[7]) * d_raw
    return _clamp(d_new, 1.0, 10.0)


def stability_after_recall(
    d: float, s: float, r: float, rating: int, w: list = DEFAULT_W
) -> float:
    """
    New stability after a successful recall (rating ≥ 2).

    S' = S * (exp(w[8]) * (11-D) * S^(-w[9]) * (exp(w[10]*(1-R)) - 1)
             * hard_penalty * easy_bonus + 1)

    The multiplier > 1 means stability always grows on recall.
    Hard penalty (w[15] < 1) dampens growth for Hard ratings.
    Easy bonus (w[16] > 1) boosts growth for Easy ratings.
    """
    assert rating in (2, 3, 4), "Use stability_after_forget for rating=1"
    hard_penalty = w[15] if rating == 2 else 1.0
    easy_bonus = w[16] if rating == 4 else 1.0

    multiplier = (
        math.exp(w[8])
        * (11.0 - d)
        * s ** (-w[9])
        * (math.exp(w[10] * (1.0 - r)) - 1.0)
        * hard_penalty
        * easy_bonus
        + 1.0
    )
    return max(s * multiplier, 0.1)  # stability can't go below 0.1 days


def stability_after_forget(
    d: float, s: float, r: float, w: list = DEFAULT_W
) -> float:
    """
    New stability after forgetting (rating == 1, Again).

    S' = w[11] * D^(-w[12]) * ((S+1)^w[13] - 1) * exp(w[14]*(1-R))

    Properties:
    - Low difficulty → higher post-lapse stability (easier cards recover faster)
    - Recent review (high R) → lower post-lapse stability (shouldn't have forgotten)
    - High prior stability → slightly higher post-lapse stability (some retention preserved)
    """
    new_s = (
        w[11]
        * d ** (-w[12])
        * ((s + 1.0) ** w[13] - 1.0)
        * math.exp(w[14] * (1.0 - r))
    )
    return max(new_s, 0.1)


# ---------------------------------------------------------------------------
# High-level review processor
# ---------------------------------------------------------------------------

def process_review(
    state: FSRSState,
    rating: int,
    review_date: Optional[date] = None,
    desired_retention: float = 0.9,
    w: list = DEFAULT_W,
) -> FSRSState:
    """
    Apply a review with the given rating to a card state. Returns updated state.

    Args:
        state:             Current FSRS state of the card.
        rating:            1=Again, 2=Hard, 3=Good, 4=Easy.
        review_date:       Date of review (defaults to today).
        desired_retention: Target recall probability. Default 0.9.
        w:                 Algorithm weights. Default FSRS-5 weights.

    Returns:
        New FSRSState with updated difficulty, stability, reps, lapses,
        last_review, and next_review.
    """
    assert 1 <= rating <= 4
    today = review_date or date.today()

    new_state = FSRSState(
        difficulty=state.difficulty,
        stability=state.stability,
        reps=state.reps + 1,
        lapses=state.lapses,
        last_review=today,
    )

    if state.reps == 0:
        # --- First review: initialize from rating ---
        new_state.stability = initial_stability(rating, w)
        new_state.difficulty = initial_difficulty(rating, w)
    else:
        # --- Subsequent review ---
        days_elapsed = (today - state.last_review).days if state.last_review else 1
        r = retrievability(state.stability, max(1, days_elapsed))

        new_state.difficulty = update_difficulty(state.difficulty, rating, w)

        if rating == 1:
            # Lapse: card forgotten
            new_state.stability = stability_after_forget(state.difficulty, state.stability, r, w)
            new_state.lapses = state.lapses + 1
        else:
            new_state.stability = stability_after_recall(
                state.difficulty, state.stability, r, rating, w
            )

    interval = next_interval(new_state.stability, desired_retention)
    new_state.next_review = today + timedelta(days=interval)

    return new_state


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("FSRS-5 self-test")
    print("=" * 50)

    # New card, first review rated Good (3)
    state = FSRSState()
    state = process_review(state, rating=3, review_date=date(2026, 3, 11))
    print(f"After Good on new card: S={state.stability:.2f}, D={state.difficulty:.2f}, next={state.next_review}")
    assert state.stability == DEFAULT_W[2], f"Expected {DEFAULT_W[2]}, got {state.stability}"

    # Second review rated Good
    state = process_review(state, rating=3, review_date=date(2026, 3, 14))
    print(f"After Good (day 3): S={state.stability:.2f}, D={state.difficulty:.2f}, next={state.next_review}")
    assert state.stability > DEFAULT_W[2], "Stability should grow after recall"

    # Lapse (Again)
    state2 = FSRSState(difficulty=6.0, stability=10.0, reps=3,
                       last_review=date(2026, 3, 1))
    state2 = process_review(state2, rating=1, review_date=date(2026, 3, 11))
    print(f"After Again (lapsed): S={state2.stability:.2f}, D={state2.difficulty:.2f}, lapses={state2.lapses}")
    assert state2.lapses == 1
    assert state2.stability < 5.0, "Stability should drop after lapse"

    # Interval calculation
    i90 = next_interval(10.0, desired_retention=0.9)
    i85 = next_interval(10.0, desired_retention=0.85)
    i95 = next_interval(10.0, desired_retention=0.95)
    print(f"Interval for S=10: r=0.9→{i90}d, r=0.85→{i85}d, r=0.95→{i95}d")
    assert i90 == 10, f"At default retention, interval should equal stability, got {i90}"
    assert i85 > i90, "Lower retention target → longer interval"
    assert i95 < i90, "Higher retention target → shorter interval"

    print("\nAll assertions passed.")
