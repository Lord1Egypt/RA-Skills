"""
Typosquat detection for npm, PyPI, and crates.io packages.
Uses Levenshtein edit distance against a curated list of high-value targets.

Returns a float 0.0–1.0 (similarity score) and mutates the meta dict
to set `similar_to` when a match is found.
"""

from __future__ import annotations

# High-value targets commonly typosquatted per ecosystem.
# Extend these lists as new targets emerge.
NPM_TARGETS = [
    "axios", "react", "react-dom", "lodash", "express", "moment", "chalk",
    "commander", "webpack", "babel-core", "typescript", "eslint", "prettier",
    "next", "vue", "angular", "svelte", "vite", "rollup", "esbuild",
    "dotenv", "uuid", "crypto", "node-fetch", "cross-fetch", "qs",
    "jsonwebtoken", "bcrypt", "mongoose", "sequelize", "prisma",
    "aws-sdk", "firebase", "supabase", "stripe", "twilio",
    "jest", "mocha", "chai", "sinon", "cypress", "playwright",
    "colors", "debug", "semver", "glob", "minimist", "yargs",
    "socket.io", "ws", "http-server", "cors", "helmet",
    "tar", "archiver", "adm-zip", "node-schedule", "cron",
]

PYPI_TARGETS = [
    "requests", "numpy", "pandas", "flask", "django", "sqlalchemy",
    "fastapi", "uvicorn", "pydantic", "aiohttp", "httpx",
    "boto3", "botocore", "google-cloud", "azure", "paramiko",
    "cryptography", "PyJWT", "passlib", "bcrypt",
    "pytest", "black", "flake8", "mypy", "pylint",
    "pillow", "opencv-python", "matplotlib", "scipy", "sklearn",
    "celery", "redis", "psycopg2", "pymongo", "elasticsearch",
    "click", "typer", "rich", "colorama", "tqdm",
    "setuptools", "pip", "wheel", "twine",
]

CRATES_TARGETS = [
    "tokio", "serde", "serde_json", "reqwest", "hyper", "axum",
    "clap", "anyhow", "thiserror", "log", "tracing", "env_logger",
    "rand", "chrono", "uuid", "regex", "lazy_static",
    "openssl", "rustls", "ring", "sha2", "md5",
    "rayon", "crossbeam", "flume", "parking_lot",
]

TARGETS_BY_ECOSYSTEM = {
    "npm": NPM_TARGETS,
    "pypi": PYPI_TARGETS,
    "crates": CRATES_TARGETS,
}


def levenshtein(a: str, b: str) -> int:
    """Standard dynamic programming Levenshtein distance."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def similarity(a: str, b: str) -> float:
    """Normalized similarity [0, 1] where 1 = identical."""
    dist = levenshtein(a.lower(), b.lower())
    return 1.0 - dist / max(len(a), len(b))


def typosquat_score(name: str, ecosystem: str, meta: dict | None = None) -> float | None:
    """
    Return the highest similarity score against known high-value targets.
    Also mutates meta['similar_to'] if a close match is found.
    Returns None if the name IS one of the targets (not a typosquat).
    """
    targets = TARGETS_BY_ECOSYSTEM.get(ecosystem, [])
    if not targets:
        return None

    name_lower = name.lower()

    # Exact match = this IS a known package, not a typosquat
    if name_lower in [t.lower() for t in targets]:
        return None

    best_score = 0.0
    best_target = None

    for target in targets:
        score = similarity(name_lower, target.lower())
        if score > best_score:
            best_score = score
            best_target = target

    # Only report if the score is above noise floor
    if best_score < 0.6:
        return None

    if meta is not None and best_target:
        meta["similar_to"] = best_target

    return best_score
