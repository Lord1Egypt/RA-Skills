"""
Utility helpers: delays, amount randomization, retry logic, logging.
"""
import random
import time
import logging
import os
from datetime import datetime, timezone

LOG_FILE = os.path.join(
    os.path.expanduser(os.getenv("WALLET_DATA_DIR", "~/.wallet-mcp")),
    "wallet-mcp.log",
)


def setup_logging(level: str | None = None) -> logging.Logger:
    logger = logging.getLogger("wallet-mcp")
    if logger.handlers:
        return logger
    level_str = level or os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(getattr(logging, level_str.upper(), logging.INFO))
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    fh = logging.FileHandler(LOG_FILE)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    return logger


def random_delay(min_sec: int = 1, max_sec: int = 30) -> None:
    """Sleep a random duration between min and max seconds."""
    delay = random.uniform(min_sec, max_sec)
    setup_logging().debug(f"Sleeping {delay:.2f}s")
    time.sleep(delay)


def random_amount(base: float, variance: float = 0.10) -> float:
    """Return base ± variance*base, rounded to 9 decimal places."""
    delta = base * variance
    return round(random.uniform(base - delta, base + delta), 9)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def retry(fn, attempts: int = 3, delay: int = 5):
    """Retry callable `fn` up to `attempts` times with fixed delay on failure."""
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    last_exc: Exception | None = None
    log = setup_logging()
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            log.warning(f"Attempt {i + 1}/{attempts} failed: {exc}")
            if i < attempts - 1:
                time.sleep(delay)
    assert last_exc is not None
    raise last_exc
