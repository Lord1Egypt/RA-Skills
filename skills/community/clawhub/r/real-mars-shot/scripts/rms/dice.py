"""Deterministic d100 from the save seed, turn index, and a salt."""

from __future__ import annotations

import hashlib


def roll_d100(seed: int, turn: int, salt: str) -> int:
    digest = hashlib.sha256(f"{seed}:{turn}:{salt}".encode()).hexdigest()
    return int(digest[:8], 16) % 100 + 1


def pick_weighted(seed: int, turn: int, salt: str, weights: list[tuple[str, float]]) -> str:
    total = sum(weight for _key, weight in weights)
    if total <= 0:
        raise ValueError("no weights")
    roll = roll_d100(seed, turn, salt)
    # Map 1..100 onto the weight line. Use a finer hash so equal weights don't clump.
    digest = hashlib.sha256(f"{seed}:{turn}:{salt}:fine".encode()).hexdigest()
    point = (int(digest[:8], 16) / 0xFFFFFFFF) * total
    cursor = 0.0
    chosen = weights[-1][0]
    for key, weight in weights:
        cursor += weight
        if point <= cursor:
            chosen = key
            break
    return chosen
